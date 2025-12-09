"""
Flask Extensions Module.

This module initializes Flask extensions to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from opt.web.panel.socketio_server import SocketIOServer
from typing import Any

db: Any = SQLAlchemy()
migrate: Any = Migrate()
login_manager: Any = LoginManager()
csrf: Any = CSRFProtect()
limiter: Any = Limiter(key_func=get_remote_address)
socketio_server: SocketIOServer = SocketIOServer()
