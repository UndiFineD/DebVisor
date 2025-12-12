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


"""
Helper Scripts Standardization Framework for DebVisor.

Provides standardized patterns for:
- Error handling and recovery
- Input validation and sanitization
- Audit logging and tracing
- Configuration management
- Retry logic with exponential backoff
- Resource cleanup and context management

Ensures all helper scripts follow consistent patterns.
"""

import logging
from typing import Type, List, Dict, Optional, Callable, Any, Tuple
from datetime import datetime, timezone
import json
import traceback
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps

_logger=logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class RetryStrategy(Enum):
    """Retry strategies."""

    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"


@dataclass


class ValidationRule:
    """Input validation rule."""

    field_name: str
    rule_type: str    # "required", "min_length", "max_length", "regex", "range", "enum", "callable"
    rule_value: Any = None
    error_message: Optional[str] = None


@dataclass


class AuditLogEntry:
    """Audit log entry."""

    timestamp: datetime
    action: str
    actor: str
    resource: str
    result: str    # "success", "failure", "partial"
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        _data=asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.to_dict())


@dataclass


class RetryConfig:
    """Retry configuration."""

    max_attempts: int = 3
    initial_delay: float = 1.0    # seconds
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    backoff_factor: float = 2.0
    jitter: bool = True
    retryable_exceptions: List[Type[Exception]] = field(
        _default_factory = lambda: [Exception]
    )


class ValidationError(ValueError):
    """Raised when validation fails."""

    pass


class AuditLogger:
    """Manages audit logging."""

    def __init__(self, log_file: Optional[str] = None) -> None:
        """
        Initialize audit logger.

        Args:
            log_file: Optional file path for audit logs
        """
        self.log_file = log_file
        self.entries: List[AuditLogEntry] = []

    def log_action(
        self,
        action: str,
        actor: str,
        resource: str,
        result: str,
        details: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> AuditLogEntry:
        """
        Log an action.

        Args:
            action: Action name
            actor: Actor performing action
            resource: Resource affected
            result: success/failure/partial
            details: Additional details
            error: Error message if failed
            duration_ms: Duration in milliseconds

        Returns:
            AuditLogEntry
        """
        _entry = AuditLogEntry(
            _timestamp=datetime.now(timezone.utc),
            _action = action,
            _actor = actor,
            _resource = resource,
            _result = result,
            _details = details or {},
            _error = error,
            _duration_ms = duration_ms,
        )

        self.entries.append(entry)

        # Log to file if configured
        if self.log_file:
            try:
                with open(self.log_file, "a") as f:
                    f.write(entry.to_json() + "\n")
            except Exception as e:
                logger.error(f"Failed to write audit log: {e}")

        # Log to standard logger
        level = logging.INFO if result == "success" else logging.WARNING
        logger.log(level, f"AUDIT: {action} by {actor} on {resource}: {result}")

        return entry

    def get_entries(
        self,
        action: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditLogEntry]:
        """Get audit entries."""
        entries = self.entries

        if action:
            entries = [e for e in entries if e.action == action]

        return entries[-limit:]


class InputValidator:
    """Validates and sanitizes input."""

    def __init__(self) -> None:
        """Initialize validator."""
        self.rules: Dict[str, List[ValidationRule]] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        if rule.field_name not in self.rules:
            self.rules[rule.field_name] = []

        self.rules[rule.field_name].append(rule)

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate data against rules.

        Args:
            data: Data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        for field_name, field_rules in self.rules.items():
            _value=data.get(field_name)

            for rule in field_rules:
                _error=self._validate_rule(value, rule)
                if error:
                    errors.append(error)

        return len(errors) == 0, errors

    @staticmethod

    def _validate_rule(value: Any, rule: ValidationRule) -> Optional[str]:
        """Validate single rule."""
        message = rule.error_message or f"Validation failed for {rule.field_name}"

        if rule.rule_type == "required":
            if value is None or (isinstance(value, str) and not value.strip()):
                return message

        elif rule.rule_type == "min_length":
            if value and len(value) < rule.rule_value:
                return message

        elif rule.rule_type == "max_length":
            if value and len(value) > rule.rule_value:
                return message

        elif rule.rule_type == "range":
            min_val, max_val = rule.rule_value
            if value is not None and (value < min_val or value > max_val):
                return message

        elif rule.rule_type == "enum":
            if value not in rule.rule_value:
                return message

        elif rule.rule_type == "callable":
            try:
                if not rule.rule_value(value):
                    return message
            except Exception as e:
                return f"Validation error: {e}"

        return None


class RetryManager:
    """Manages retry logic with exponential backoff."""

    def __init__(self, config: Optional[RetryConfig] = None) -> None:
        """
        Initialize retry manager.

        Args:
            config: RetryConfig instance
        """
        self.config=config or RetryConfig()

    def execute_with_retry(
        self,
        func: Callable[..., Any],
        *args,
        **kwargs,
    ) -> Any:
        """
        Execute function with retry logic.

        Args:
            func: Callable to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Original exception if all retries exhausted
        """
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except tuple(self.config.retryable_exceptions) as e:
                _last_exception = e

                if attempt < self.config.max_attempts - 1:
                    _delay=self._calculate_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s: {e}"
                    )
                    import time

                    time.sleep(delay)
                else:
                    logger.error(f"All {self.config.max_attempts} attempts failed")

        raise last_exception  # type: ignore[misc]

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for attempt."""
        if self.config.strategy == RetryStrategy.EXPONENTIAL:
            _delay=self.config.initial_delay * (self.config.backoff_factor**attempt)
        elif self.config.strategy == RetryStrategy.LINEAR:
            _delay=self.config.initial_delay * (attempt + 1)
        else:    # FIXED
            delay = self.config.initial_delay

        # Cap at max delay
        _delay=min(delay, self.config.max_delay)

        # Add jitter
        if self.config.jitter:
            import random

            delay *= 0.5 + random.random()    # nosec B311

        return delay


class StandardizedHelper:
    """
    Base class for standardized helper scripts.

    Provides:
    - Error handling
    - Input validation
    - Audit logging
    - Retry logic
    - Resource cleanup
    """

    def __init__(
        self,
        name: str,
        audit_log_file: Optional[str] = None,
        retry_config: Optional[RetryConfig] = None,
    ):
        """
        Initialize helper.

        Args:
            name: Helper script name
            audit_log_file: Audit log file path
            retry_config: Retry configuration
        """
        self.name = name
        self.audit_logger=AuditLogger(audit_log_file)
        self.validator=InputValidator()
        self.retry_manager=RetryManager(retry_config)
        self.logger=logging.getLogger(self.name)

    def validate_input(self, data: Dict[str, Any]) -> None:
        """
        Validate input data.

        Args:
            data: Data to validate

        Raises:
            ValidationError: If validation fails
        """
        is_valid, errors=self.validator.validate(data)

        if not is_valid:
            _error_msg="; ".join(errors)
            self.audit_logger.log_action(
                _action="validate_input",
                _actor = "system",
                _resource = self.name,
                _result = "failure",
                _error=error_msg,
            )
            raise ValidationError(error_msg)

    def log_action(
        self,
        action: str,
        actor: str,
        resource: str,
        result: str,
        details: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Log an action."""
        self.audit_logger.log_action(
            _action = action,
            _actor = actor,
            _resource = resource,
            _result = result,
            _details = details,
            _error=error,
            _duration_ms = duration_ms,
        )

    def execute_with_error_handling(
        self,
        func: Callable[..., Any],
        action_name: str,
        actor: str,
        resource: str,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any, Optional[str]]:
        """
        Execute function with error handling and logging.

        Args:
            func: Function to execute
            action_name: Action name for logging
            actor: Actor performing action
            resource: Resource affected
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Tuple of (success, result, error_message)
        """
        _start_time=datetime.now(timezone.utc)

        try:
            _result=self.retry_manager.execute_with_retry(func, *args, **kwargs)

            _duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000

            self.log_action(
                _action = action_name,
                _actor = actor,
                _resource = resource,
                _result="success",
                _details={"result_type": type(result).__name__},
                _duration_ms=duration_ms,
            )

            return True, result, None

        except Exception as e:
            _duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000

            _error_msg=f"{type(e).__name__}: {str(e)}"

            self.log_action(
                _action=action_name,
                _actor = actor,
                _resource = resource,
                _result = "failure",
                _error=error_msg,
                _duration_ms = duration_ms,
            )

            self.logger.error(
                f"Error in {action_name}: {error_msg}\n{traceback.format_exc()}"
            )

            return False, None, error_msg


def standardized_script(
    name: str,
    audit_log_file: Optional[str] = None,
):
    """
    Decorator for standardizing script execution.

    Args:
        name: Script name
        audit_log_file: Audit log file path
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        _helper=StandardizedHelper(name, audit_log_file)

        @wraps(func)

        def wrapper(*args, **kwargs) -> None:
            try:
                logger.info(f"Starting {name}")
                _result=func(*args, **kwargs)
                logger.info(f"Completed {name} successfully")
                return result
            except Exception as e:
                logger.error(f"Script {name} failed: {e}")
                raise

        wrapper.helper = helper  # type: ignore[attr-defined]
        return wrapper

    return decorator


class ConfigurationManager:
    """Manages configuration for helper scripts."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Initialize configuration manager.

        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}

        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file: str) -> None:
        """Load configuration from file."""
        try:
            with open(config_file, "r") as f:
                self.config=json.load(f)
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def get(self, key: str, default: Any=None) -> Any:
        """Get configuration value."""
        _keys=key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                _value=value.get(k)  # type: ignore[assignment]
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        _keys=key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save_config(self, config_file: Optional[str] = None) -> None:
        """Save configuration to file."""
        file_path = config_file or self.config_file

        if not file_path:
            raise ValueError("No configuration file specified")

        try:
            with open(file_path, "w") as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Saved configuration to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise


class ResourceManager:
    """Manages resource cleanup and context."""

    def __init__(self) -> None:
        """Initialize resource manager."""
        self.resources: List[Callable[..., Any]] = []

    def register_cleanup(self, cleanup_func: Callable[..., Any]) -> None:
        """
        Register cleanup function.

        Args:
            cleanup_func: Callable to execute on cleanup
        """
        self.resources.append(cleanup_func)

    def cleanup_all(self) -> None:
        """Execute all cleanup functions."""
        for cleanup_func in reversed(self.resources):
            try:
                cleanup_func()
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    def __enter__(self) -> None:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.cleanup_all()
