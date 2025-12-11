# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Authentication Routes - User Login/Logout/Register

Provides Flask Blueprint for user authentication flows including
login, logout, registration, password reset, and session management.
"""

from opt.web.panel.extensions import db, limiter
from typing import Any
# import time

from opt.web.panel.rbac import require_permission, Resource, Action
from opt.helpers.mail import send_password_reset
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from opt.web.panel.models.audit_log import AuditLog
from opt.web.panel.models.user import User
from opt.helpers.rate_limit import sliding_window_limiter
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
)
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin


def is_safe_url(target: str) -> bool:
    """Ensure a URL is safe for redirection (prevents open redirects)."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# Create blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"], key_func=lambda: request.remote_addr)    # type: ignore
@sliding_window_limiter(
    lambda: f"user:{request.form.get('username', 'anonymous')}",
    limit=20,
    window_seconds=60,
)
def login() -> Any:
    """User login endpoint.

    GET: Display login form
    POST: Authenticate user and create session
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember_me = request.form.get("remember_me") is not None

        # Validate input
        if not username or not password:
            flash("Username and password required", "error")
            return redirect(url_for("auth.login"))

        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        # Verify user exists and password is correct
        if not user or not user.check_password(password):
            flash("Invalid username or password", "error")

            # Log failed login attempt
            AuditLog.log_operation(
                user_id=None,
                operation="read",
                resource_type="user",
                action=f"Failed login attempt for {username}",
                status="failure",
                status_code=401,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
            )
            # Exponential backoff: impose a delay based on recent failures for this IP
            # Sliding window approximation via limiter; add small sleep to deter brute force
            try:
                failure_count = int(session.get("login_failures", 0)) + 1
                session["login_failures"] = failure_count
                delay_seconds = min(8, 2 ** min(3, failure_count - 1))
                time.sleep(delay_seconds / 10.0)
            except Exception as e:
                current_app.logger.debug(f"Delay calculation error: {e}")
            return redirect(url_for("auth.login"))

        # Check if user is active
        if not user.is_active:
            flash("Account is disabled", "error")
            return redirect(url_for("auth.login"))

        # Login successful
        login_user(user, remember=remember_me)
        user.update_last_login()

        # Log successful login
        AuditLog.log_operation(
            user_id=user.id,
            operation="read",
            resource_type="user",
            action=f"User {user.username} logged in",
            status="success",
            status_code=200,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
        )

        flash(f"Welcome back, {user.full_name or user.username}!", "success")
        next_page = request.args.get("next")

        # Validate next_page to prevent open redirects
        if not next_page or not is_safe_url(next_page):
            next_page = url_for("main.dashboard")

        return redirect(next_page)

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required    # type: ignore
@limiter.limit(    # type: ignore
    "60 per 10 minutes", methods=["POST"], key_func=lambda: request.remote_addr
)
def logout() -> Any:
    """User logout endpoint.

    Clears session and invalidates login token.
    """
    user = current_user
    logout_user()

    # Log logout
    AuditLog.log_operation(
        user_id=user.id,
        operation="read",
        resource_type="user",
        action=f"User {user.username} logged out",
        status="success",
        ip_address=request.remote_addr,
    )

    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"], key_func=lambda: request.remote_addr)    # type: ignore
@sliding_window_limiter(
    lambda: f"email:{request.form.get('email', 'unknown')}",
    limit=10,
    window_seconds=3600,
)
def register() -> Any:
    """User registration endpoint.

    GET: Display registration form
    POST: Create new user account
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        full_name = request.form.get("full_name", "").strip()

        # Validate input
        errors = []

        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters")

        if not email or "@" not in email:
            errors.append("Valid email address required")

        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters")

        if password != password_confirm:
            errors.append("Passwords do not match")

        # Check for existing user
        if User.query.filter_by(username=username).first():
            errors.append("Username already taken")

        if User.query.filter_by(email=email).first():
            errors.append("Email already registered")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("auth.register"))

        # Create new user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Log registration
        AuditLog.log_operation(
            user_id=user.id,
            operation="create",
            resource_type="user",
            action=f"New user account created: {username}",
            status="success",
            ip_address=request.remote_addr,
        )

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required    # type: ignore
@sliding_window_limiter(
    lambda: f"user:{getattr(current_user, 'id', 'anon')}", limit=30, window_seconds=600
)
def profile() -> Any:
    """User profile management endpoint.

    GET: Display user profile
    POST: Update user information
    """
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        new_password_confirm = request.form.get("new_password_confirm", "")

        # Update profile fields
        if full_name:
            current_user.full_name = full_name

        if email and email != current_user.email:
            # Check if email already in use
            if User.query.filter_by(email=email).first():
                flash("Email already in use", "error")
            else:
                current_user.email = email

        # Update password if provided
        if new_password:
            if not current_user.check_password(current_password):
                flash("Current password is incorrect", "error")
                return redirect(url_for("auth.profile"))

            if new_password != new_password_confirm:
                flash("New passwords do not match", "error")
                return redirect(url_for("auth.profile"))

            if len(new_password) < 8:
                flash("New password must be at least 8 characters", "error")
                return redirect(url_for("auth.profile"))

            current_user.set_password(new_password)

        db.session.commit()

        # Log profile update
        AuditLog.log_operation(
            user_id=current_user.id,
            operation="update",
            resource_type="user",
            action="User updated their profile",
            status="success",
            ip_address=request.remote_addr,
        )

        flash("Profile updated successfully", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", user=current_user)


@auth_bp.route("/users", methods=["GET"])
@login_required    # type: ignore
@require_permission(Resource.USER, Action.READ)
def list_users() -> Any:
    """List all user accounts (admin only).

    GET: Display paginated user list
    """
    page = request.args.get("page", 1, type=int)
    per_page = 20

    pagination = User.query.paginate(page=page, per_page=per_page)
    users = pagination.items

    return render_template("auth/users.html", users=users, pagination=pagination)


@auth_bp.route("/reset", methods=["GET", "POST"])
@limiter.limit(    # type: ignore
    "10 per 10 minutes", methods=["POST"], key_func=lambda: request.remote_addr
)
@sliding_window_limiter(
    lambda: f"email:{request.form.get('email', 'unknown')}",
    limit=5,
    window_seconds=1800,
)
def password_reset() -> Any:
    """Password reset request endpoint.

    GET: Show reset form
    POST: Accept email and enqueue reset instructions (placeholder implementation)
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or "@" not in email:
            flash("Valid email address required", "error")
            return redirect(url_for("auth.password_reset"))

        user = User.query.filter_by(email=email).first()
        if not user:
            # Avoid user enumeration: respond success regardless
            AuditLog.log_operation(
                user_id=None,
                operation="read",
                resource_type="user",
                action=f"Password reset requested for {email} (no account)",
                status="success",
                ip_address=request.remote_addr,
            )
            flash("If an account exists, reset instructions have been sent.", "info")
            return redirect(url_for("auth.login"))

        # Generate time-limited reset token and enqueue email (placeholder)
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = s.dumps({"uid": user.id, "email": user.email}, salt="reset")

        send_password_reset(email=user.email, token=token)

        AuditLog.log_operation(
            user_id=user.id,
            operation="update",
            resource_type="user",
            action="Password reset requested",
            status="success",
            ip_address=request.remote_addr,
        )
        flash("If an account exists, reset instructions have been sent.", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset.html")


@auth_bp.route("/reset/verify", methods=["GET", "POST"])
@limiter.limit(    # type: ignore
    "10 per 10 minutes", methods=["POST"], key_func=lambda: request.remote_addr
)
def reset_verify() -> Any:
    """Verify reset token and set new password."""
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = (
        request.args.get("token")
        if request.method == "GET"
        else request.form.get("token")
    )

    if request.method == "GET":
        # Render form to set new password
        return render_template("auth/reset_verify.html", token=token)

    # POST: apply new password
    new_password = request.form.get("password", "")
    confirm = request.form.get("password_confirm", "")
    if not new_password or new_password != confirm or len(new_password) < 8:
        flash("Invalid password or mismatch", "error")
        return redirect(url_for("auth.reset_verify", token=token))

    if not token:
        flash("Missing reset token", "error")
        return redirect(url_for("auth.password_reset"))

    try:
        data = s.loads(token, salt="reset", max_age=3600)
    except SignatureExpired:
        flash("Reset link expired", "error")
        return redirect(url_for("auth.password_reset"))
    except BadSignature:
        flash("Invalid reset link", "error")
        return redirect(url_for("auth.password_reset"))

    user = User.query.get(int(data.get("uid")))
    if not user or user.email != data.get("email"):
        flash("Invalid reset link", "error")
        return redirect(url_for("auth.password_reset"))

    user.set_password(new_password)
    db.session.commit()

    AuditLog.log_operation(
        user_id=user.id,
        operation="update",
        resource_type="user",
        action="User password reset via token",
        status="success",
        ip_address=request.remote_addr,
    )

    flash("Password updated. Please log in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/users/<int:user_id>/disable", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.USER, Action.UPDATE)
@sliding_window_limiter(
    lambda: f"admin:{getattr(current_user, 'id', 'anon')}", limit=20, window_seconds=600
)
def disable_user(user_id: int) -> Any:
    """Disable user account (admin only).

    POST: Set is_active to False
    """
    if user_id == current_user.id:
        flash("Cannot disable your own account", "error")
        return redirect(url_for("auth.list_users"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for("auth.list_users"))

    user.is_active = False
    db.session.commit()

    # Log user disable
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="update",
        resource_type="user",
        action=f"Disabled user account: {user.username}",
        status="success",
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )

    flash(f"User {user.username} has been disabled", "success")
    return redirect(url_for("auth.list_users"))


@auth_bp.route("/users/<int:user_id>/enable", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.USER, Action.UPDATE)
@sliding_window_limiter(
    lambda: f"admin:{getattr(current_user, 'id', 'anon')}", limit=20, window_seconds=600
)
def enable_user(user_id: int) -> Any:
    """Enable user account (admin only).

    POST: Set is_active to True
    """
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for("auth.list_users"))

    user.is_active = True
    db.session.commit()

    # Log user enable
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="update",
        resource_type="user",
        action=f"Enabled user account: {user.username}",
        status="success",
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )

    flash(f"User {user.username} has been enabled", "success")
    return redirect(url_for("auth.list_users"))


@auth_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required    # type: ignore
@require_permission(Resource.USER, Action.DELETE)
@sliding_window_limiter(
    lambda: f"admin:{getattr(current_user, 'id', 'anon')}", limit=20, window_seconds=600
)
def delete_user(user_id: int) -> Any:
    """Delete user account (admin only).

    POST: Permanently remove user
    """
    if user_id == current_user.id:
        flash("Cannot delete your own account", "error")
        return redirect(url_for("auth.list_users"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for("auth.list_users"))

    username = user.username
    db.session.delete(user)
    db.session.commit()

    # Log user deletion
    AuditLog.log_operation(
        user_id=current_user.id,
        operation="delete",
        resource_type="user",
        action=f"Deleted user account: {username}",
        status="success",
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )

    flash(f"User {username} has been deleted", "success")
    return redirect(url_for("auth.list_users"))
