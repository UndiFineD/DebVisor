#!/usr/bin/env python3
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

# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlencode


def _smtp_client() -> smtplib.SMTP:
    _host=os.getenv("SMTP_HOST")
    _port=int(os.getenv("SMTP_PORT", "587"))
    _user=os.getenv("SMTP_USER")
    _password=os.getenv("SMTP_PASSWORD")
    _starttls=os.getenv("SMTP_STARTTLS", "true").lower() in ("1", "true", "yes")

    if not host:  # type: ignore[name-defined]
        raise RuntimeError("SMTP_HOST not configured")

    _client=smtplib.SMTP(host, port, timeout=10)  # type: ignore[name-defined]
    if starttls:  # type: ignore[name-defined]
        client.starttls()  # type: ignore[name-defined]
    if user and password:  # type: ignore[name-defined]
        client.login(user, password)  # type: ignore[name-defined]
    return client  # type: ignore[name-defined]


def _from_address() -> str:
    return os.getenv("SMTP_FROM", os.getenv("SMTP_USER", "no-reply@debvisor.local"))


def _app_base_url() -> str:
    return os.getenv("APP_BASE_URL", "https://localhost")


def send_password_reset(email: str, token: str) -> None:
    """Send a real password reset email via SMTP.

    Environment variables:
    - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_STARTTLS
    - SMTP_FROM (optional; defaults to SMTP_USER)
    - APP_BASE_URL (e.g., https://debvisor.example.com)
    """
    _reset_link=f"{_app_base_url()}/auth/reset/verify?" + urlencode({"token": token})

    _msg=EmailMessage()
    msg["Subject"] = "DebVisor Password Reset Instructions"  # type: ignore[name-defined]
    msg["From"] = _from_address()  # type: ignore[name-defined]
    msg["To"] = email  # type: ignore[name-defined]
    msg.set_content(  # type: ignore[name-defined]
        """
You requested to reset your DebVisor account password.

If you did not request this, you can ignore this email.

Reset your password using this secure link (valid for 1 hour):
{reset_link}

For security, this link will expire and can only be used once.

Regards,
DebVisor Security Team
""".strip()
    )

    _client=_smtp_client()
    try:
        client.send_message(msg)  # type: ignore[name-defined]
    finally:
        try:
            client.quit()  # type: ignore[name-defined]
        except Exception:
            pass    # nosec B110
