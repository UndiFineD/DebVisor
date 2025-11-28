"""Authentication Routes - User Login/Logout/Register

Provides Flask Blueprint for user authentication flows including
login, logout, registration, password reset, and session management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from datetime import datetime
from app import db
from models.user import User
from models.audit_log import AuditLog

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint.
    
    GET: Display login form
    POST: Authenticate user and create session
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') is not None
        
        # Validate input
        if not username or not password:
            flash('Username and password required', 'error')
            return redirect(url_for('auth.login'))
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        # Verify user exists and password is correct
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'error')
            
            # Log failed login attempt
            AuditLog.log_operation(
                user_id=None,
                operation='read',
                resource_type='user',
                action=f'Failed login attempt for {username}',
                status='failure',
                status_code=401,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
            )
            return redirect(url_for('auth.login'))
        
        # Check if user is active
        if not user.is_active:
            flash('Account is disabled', 'error')
            return redirect(url_for('auth.login'))
        
        # Login successful
        login_user(user, remember=remember_me)
        user.update_last_login()
        
        # Log successful login
        AuditLog.log_operation(
            user_id=user.id,
            operation='read',
            resource_type='user',
            action=f'User {user.username} logged in',
            status='success',
            status_code=200,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
        )
        
        flash(f'Welcome back, {user.full_name or user.username}!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint.
    
    Clears session and invalidates login token.
    """
    user = current_user
    logout_user()
    
    # Log logout
    AuditLog.log_operation(
        user_id=user.id,
        operation='read',
        resource_type='user',
        action=f'User {user.username} logged out',
        status='success',
        ip_address=request.remote_addr,
    )
    
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint.
    
    GET: Display registration form
    POST: Create new user account
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        full_name = request.form.get('full_name', '').strip()
        
        # Validate input
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if not email or '@' not in email:
            errors.append('Valid email address required')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        if password != password_confirm:
            errors.append('Passwords do not match')
        
        # Check for existing user
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log registration
        AuditLog.log_operation(
            user_id=user.id,
            operation='create',
            resource_type='user',
            action=f'New user account created: {username}',
            status='success',
            ip_address=request.remote_addr,
        )
        
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management endpoint.
    
    GET: Display user profile
    POST: Update user information
    """
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        new_password_confirm = request.form.get('new_password_confirm', '')
        
        # Update profile fields
        if full_name:
            current_user.full_name = full_name
        
        if email and email != current_user.email:
            # Check if email already in use
            if User.query.filter_by(email=email).first():
                flash('Email already in use', 'error')
            else:
                current_user.email = email
        
        # Update password if provided
        if new_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return redirect(url_for('auth.profile'))
            
            if new_password != new_password_confirm:
                flash('New passwords do not match', 'error')
                return redirect(url_for('auth.profile'))
            
            if len(new_password) < 8:
                flash('New password must be at least 8 characters', 'error')
                return redirect(url_for('auth.profile'))
            
            current_user.set_password(new_password)
        
        db.session.commit()
        
        # Log profile update
        AuditLog.log_operation(
            user_id=current_user.id,
            operation='update',
            resource_type='user',
            action='User updated their profile',
            status='success',
            ip_address=request.remote_addr,
        )
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    """List all user accounts (admin only).
    
    GET: Display paginated user list
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    users = pagination.items
    
    return render_template('auth/users.html', users=users, pagination=pagination)


@auth_bp.route('/users/<int:user_id>/disable', methods=['POST'])
@login_required
@admin_required
def disable_user(user_id):
    """Disable user account (admin only).
    
    POST: Set is_active to False
    """
    if user_id == current_user.id:
        flash('Cannot disable your own account', 'error')
        return redirect(url_for('auth.list_users'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.list_users'))
    
    user.is_active = False
    db.session.commit()
    
    # Log user disable
    AuditLog.log_operation(
        user_id=current_user.id,
        operation='update',
        resource_type='user',
        action=f'Disabled user account: {user.username}',
        status='success',
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )
    
    flash(f'User {user.username} has been disabled', 'success')
    return redirect(url_for('auth.list_users'))


@auth_bp.route('/users/<int:user_id>/enable', methods=['POST'])
@login_required
@admin_required
def enable_user(user_id):
    """Enable user account (admin only).
    
    POST: Set is_active to True
    """
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.list_users'))
    
    user.is_active = True
    db.session.commit()
    
    # Log user enable
    AuditLog.log_operation(
        user_id=current_user.id,
        operation='update',
        resource_type='user',
        action=f'Enabled user account: {user.username}',
        status='success',
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )
    
    flash(f'User {user.username} has been enabled', 'success')
    return redirect(url_for('auth.list_users'))


@auth_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user account (admin only).
    
    POST: Permanently remove user
    """
    if user_id == current_user.id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('auth.list_users'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.list_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    # Log user deletion
    AuditLog.log_operation(
        user_id=current_user.id,
        operation='delete',
        resource_type='user',
        action=f'Deleted user account: {username}',
        status='success',
        resource_id=str(user_id),
        ip_address=request.remote_addr,
    )
    
    flash(f'User {username} has been deleted', 'success')
    return redirect(url_for('auth.list_users'))
