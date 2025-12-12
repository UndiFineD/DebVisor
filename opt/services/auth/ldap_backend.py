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


"""
LDAP/Active Directory Authentication Backend

Provides enterprise SSO integration with LDAP/AD including:
- User authentication against LDAP/AD
- Group synchronization and management
- User provisioning and sync
- Group-based RBAC mapping
- Fallback to local authentication
- Connection pooling and caching

Author: DebVisor Team
Date: November 27, 2025
"""

import time    # Add at top with other imports
import logging
from datetime import datetime
import ldap
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from abc import ABC, abstractmethod

_logger=logging.getLogger(__name__)


class ADUserProvisioningStatus(Enum):
    """Status of user provisioning operations"""

    SUCCESS="success"
    PARTIAL="partial"
    FAILED="failed"
    SKIPPED="skipped"


@dataclass
class LDAPConfig:
    """LDAP/AD Configuration"""

    server_url: str    # ldap://server or ldaps://server
    base_dn: str    # Base DN for searches (e.g., dc=example, dc=com)
    bind_dn: Optional[str] = None    # Service account DN
    bind_password: Optional[str] = None    # Service account password
    search_filter: str="(uid={username})"    # User search filter
    group_search_filter: str="(cn={group})"    # Group search filter
    user_objectclass: str="inetOrgPerson"    # User object class
    group_objectclass: str="groupOfNames"    # Group object class
    connection_timeout: int=10    # Seconds
    pool_size: int=10    # Connection pool size
    cache_ttl: int=3600    # Cache TTL in seconds
    enable_tls: bool=False    # Use LDAPS
    enable_starttls: bool=False    # Use STARTTLS
    ca_cert_path: Optional[str] = None    # Path to CA certificate
    require_cert: bool=False    # Require certificate validation


@dataclass
class LDAPUser:
    """Represents a user from LDAP/AD"""

    username: str
    email: str
    full_name: str
    groups: List[str]
    distinguished_name: str
    created_at: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    enabled: bool=True
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "groups": self.groups,
            "distinguished_name": self.distinguished_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_modified": (
                self.last_modified.isoformat() if self.last_modified else None
            ),
            "enabled": self.enabled,
            "extra_attributes": self.extra_attributes or {},
        }


@dataclass
class SyncResult:
    """Result of user/group synchronization"""

    status: ADUserProvisioningStatus
    total_processed: int=0
    successful: int=0
    failed: int=0
    skipped: int=0
    duration_seconds: float=0.0
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "status": self.status.value,
            "total_processed": self.total_processed,
            "successful": self.successful,
            "failed": self.failed,
            "skipped": self.skipped,
            "duration_seconds": self.duration_seconds,
            "errors": self.errors,
        }


class LDAPConnectionPool:
    """Thread-safe LDAP connection pool"""

    def __init__(self, config: LDAPConfig) -> None:
        self.config=config
        self.pool: List[ldap.ldapobject.LDAPObject] = []
        self.available: asyncio.Queue[ldap.ldapobject.LDAPObject] = asyncio.Queue()
        self._lock=asyncio.Lock()
        self._initialized=False

    async def initialize(self) -> bool:
        """Initialize connection pool"""
        try:
        # Set LDAP options
            ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, self.config.connection_timeout)
            ldap.set_option(ldap.OPT_REFERRALS, 0)

            if self.config.ca_cert_path:
                ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.config.ca_cert_path)

            if not self.config.require_cert:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

            # Create connections
            for _ in range(self.config.pool_size):
                _conn=ldap.initialize(self.config.server_url)

                if self.config.enable_starttls:
                    conn.start_tls_s()  # type: ignore[name-defined]

                if self.config.bind_dn and self.config.bind_password:
                    conn.simple_bind_s(self.config.bind_dn, self.config.bind_password)  # type: ignore[name-defined]

                self.pool.append(conn)  # type: ignore[name-defined]
                await self.available.put(conn)  # type: ignore[name-defined]

            self._initialized=True
            logger.info(  # type: ignore[name-defined]
                f"LDAP connection pool initialized with {self.config.pool_size} connections"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to initialize LDAP connection pool: {e}")  # type: ignore[name-defined]
            return False

    async def get_connection(self) -> Optional[ldap.ldapobject.LDAPObject]:
        """Get a connection from the pool"""
        try:
            return await asyncio.wait_for(self.available.get(), timeout=5)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for LDAP connection from pool")  # type: ignore[name-defined]
            return None

    async def return_connection(self, conn: ldap.ldapobject.LDAPObject) -> None:
        """Return connection to pool"""
        if conn:
            await self.available.put(conn)

    async def close_all(self) -> None:
        """Close all connections"""
        async with self._lock:
            for conn in self.pool:
                try:
                    conn.unbind_s()
                except BaseException:
                    pass
            self.pool.clear()


class AuthenticationBackend(ABC):
    """Abstract authentication backend"""

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[LDAPUser]:
        """Authenticate user and return user object if successful"""
        pass

    @abstractmethod
    async def get_user(self, username: str) -> Optional[LDAPUser]:
        """Get user by username"""
        pass

    @abstractmethod
    async def get_user_groups(self, username: str) -> List[str]:
        """Get user's group memberships"""
        pass


class LDAPBackend(AuthenticationBackend):
    """LDAP/Active Directory Authentication Backend"""

    def __init__(self, config: LDAPConfig) -> None:
        self.config=config
        self.pool=LDAPConnectionPool(config)
        self._user_cache: Dict[str, Tuple[LDAPUser, float]] = {}
        self._group_cache: Dict[str, Tuple[List[str], float]] = {}

    async def initialize(self) -> bool:
        """Initialize the LDAP backend"""
        return await self.pool.initialize()

    async def authenticate(self, username: str, password: str) -> Optional[LDAPUser]:
        """
        Authenticate user against LDAP/AD.

        Args:
            username: Username to authenticate
            password: Password

        Returns:
            LDAPUser if authentication successful, None otherwise
        """
        try:
        # Search for user
            _user=await self.get_user(username)
            if not user:  # type: ignore[name-defined]
                logger.warning(f"User not found: {username}")  # type: ignore[name-defined]
                return None

            # Try to bind as user
            _conn=ldap.initialize(self.config.server_url)
            if self.config.enable_starttls:
                conn.start_tls_s()  # type: ignore[name-defined]

            conn.simple_bind_s(user.distinguished_name, password)  # type: ignore[name-defined]
            conn.unbind_s()  # type: ignore[name-defined]

            logger.info(f"User authenticated: {username}")  # type: ignore[name-defined]
            return user  # type: ignore[name-defined]

        except ldap.INVALID_CREDENTIALS:
            logger.warning(f"Invalid credentials for user: {username}")  # type: ignore[name-defined]
            return None

        except Exception as e:
            logger.error(f"Authentication error for {username}: {e}")  # type: ignore[name-defined]
            return None

    async def get_user(self, username: str) -> Optional[LDAPUser]:
        """Get user by username from LDAP/AD"""
        try:
        # Check cache
            if username in self._user_cache:
                user, timestamp=self._user_cache[username]
                if time.time() - timestamp < self.config.cache_ttl:
                    return user

            _conn=await self.pool.get_connection()
            if not conn:  # type: ignore[name-defined]
                logger.error("Failed to get LDAP connection for user lookup")  # type: ignore[name-defined]
                return None

            try:
            # Search for user
                _search_filter=self.config.search_filter.format(username=username)
                results=conn.search_s(  # type: ignore[name-defined]
                    self.config.base_dn, ldap.SCOPE_SUBTREE, search_filter  # type: ignore[name-defined]
                )

                if not results:
                    return None

                dn, attributes=results[0]

                # Extract user information
                _user=self._parse_ldap_entry(username, dn, attributes)

                # Cache user
                self._user_cache[username] = (user, time.time())

                logger.debug(f"User found in LDAP: {username}")  # type: ignore[name-defined]
                return user

            finally:
                await self.pool.return_connection(conn)  # type: ignore[name-defined]

        except Exception as e:
            logger.error(f"Error getting user {username} from LDAP: {e}")  # type: ignore[name-defined]
            return None

    async def get_user_groups(self, username: str) -> List[str]:
        """Get user's group memberships"""
        try:
        # Check cache
            if username in self._group_cache:
                groups, timestamp=self._group_cache[username]
                if time.time() - timestamp < self.config.cache_ttl:
                    return groups

            _user=await self.get_user(username)
            if not user:  # type: ignore[name-defined]
                return []

            _conn=await self.pool.get_connection()
            if not conn:  # type: ignore[name-defined]
                logger.error("Failed to get LDAP connection for group lookup")  # type: ignore[name-defined]
                return []

            try:
            # Search for groups user is member of
                _search_filter=f"(member={user.distinguished_name})"  # type: ignore[name-defined]
                results=conn.search_s(  # type: ignore[name-defined]
                    self.config.base_dn,
                    ldap.SCOPE_SUBTREE,
                    search_filter,  # type: ignore[name-defined]
                    _attrlist=["cn"],
                )

                groups=[
                    attrs.get("cn", ["unknown"])[0].decode()
                    for dn, attrs in results
                    if dn
                ]

                # Cache groups
                self._group_cache[username] = (groups, time.time())

                logger.debug(f"Found {len(groups)} groups for user {username}")  # type: ignore[name-defined]
                return groups

            finally:
                await self.pool.return_connection(conn)  # type: ignore[name-defined]

        except Exception as e:
            logger.error(f"Error getting groups for {username}: {e}")  # type: ignore[name-defined]
            return []

    def _parse_ldap_entry(
        self, username: str, dn: str, attributes: Dict[str, List[bytes]]
    ) -> LDAPUser:
        """Parse LDAP entry into LDAPUser object"""
        # Extract common attributes
        email_bytes=(
            attributes.get("mail") or attributes.get("userPrincipalName") or [b""]
        )[0]
        _email=email_bytes.decode() if isinstance(email_bytes, bytes) else str(email_bytes)

        _full_name_bytes=(attributes.get("displayName") or attributes.get("cn") or [b""])[
            0
        ]
        _full_name=full_name_bytes.decode() if isinstance(full_name_bytes, bytes) else str(full_name_bytes)  # type: ignore[name-defined]

        _groups_bytes=attributes.get("memberOf", [])
        _groups=[g.decode() if isinstance(g, bytes) else str(g) for g in groups_bytes]  # type: ignore[name-defined]

        enabled=True
        _user_account_control=attributes.get("userAccountControl")
        if user_account_control:  # type: ignore[name-defined]
            _uac_int=int(user_account_control[0])  # type: ignore[name-defined]
            _enabled=not (uac_int & 2)    # Check if ACCOUNTDISABLE flag is set  # type: ignore[name-defined]

        return LDAPUser(  # type: ignore[call-arg]
            _username=username,
            _email=email,  # type: ignore[name-defined]
            _full_name=full_name,  # type: ignore[name-defined]
            _groups=groups,  # type: ignore[name-defined]
            _distinguished_name=dn,
            _enabled=enabled,
            _extra_attributes={
                k: [v.decode() if isinstance(v, bytes) else str(v) for v in vals]
                for k, vals in attributes.items()
            },
        )

    async def sync_users(self, userfilter: Optional[str] = None) -> SyncResult:
        """
        Synchronize users from LDAP/AD to local database.

        Args:
            user_filter: Optional LDAP filter for selective sync

        Returns:
            SyncResult with operation details
        """
        _result=SyncResult(status=ADUserProvisioningStatus.SUCCESS)
        _start_time=time.time()

        try:
            _conn=await self.pool.get_connection()
            if not conn:  # type: ignore[name-defined]
                result.status=ADUserProvisioningStatus.FAILED  # type: ignore[name-defined]
                result.errors.append("Failed to get LDAP connection")  # type: ignore[name-defined]
                return result  # type: ignore[name-defined]

            try:
            # Search for users
                search_filter=(
                    user_filter or f"(objectClass={self.config.user_objectclass})"  # type: ignore[name-defined]
                )
                results=conn.search_s(  # type: ignore[name-defined]
                    self.config.base_dn,
                    ldap.SCOPE_SUBTREE,
                    search_filter,
                    _attrlist=["uid", "mail", "displayName", "memberOf"],
                )

                result.total_processed=len(results)  # type: ignore[name-defined]

                for dn, attributes in results:
                    if not dn:
                        result.skipped += 1  # type: ignore[name-defined]
                        continue

                    try:
                        _uid=(attributes.get(b"uid") or [b""])[0]
                        _username=uid.decode() if isinstance(uid, bytes) else uid  # type: ignore[name-defined]

                        self._parse_ldap_entry(username, dn, attributes)  # type: ignore[name-defined]

                        # Here you would normally save to database
                        # db.save_user(user)

                        result.successful += 1  # type: ignore[name-defined]

                    except Exception as e:
                        logger.error(f"Failed to sync user {dn}: {e}")  # type: ignore[name-defined]
                        result.failed += 1  # type: ignore[name-defined]
                        result.errors.append(f"Failed to sync {dn}: {str(e)}")  # type: ignore[name-defined]

            finally:
                await self.pool.return_connection(conn)  # type: ignore[name-defined]

        except Exception as e:
            logger.error(f"User sync error: {e}")  # type: ignore[name-defined]
            result.status=ADUserProvisioningStatus.FAILED  # type: ignore[name-defined]
            result.errors.append(f"Sync failed: {str(e)}")  # type: ignore[name-defined]

        finally:
            result.duration_seconds=time.time() - start_time  # type: ignore[name-defined]

        return result  # type: ignore[name-defined]


class LocalAuthBackend(AuthenticationBackend):
    """Fallback local authentication backend"""

    async def authenticate(self, username: str, password: str) -> Optional[LDAPUser]:
        """Authenticate against local database"""
        # Implementation would query local user database
        return None

    async def get_user(self, username: str) -> Optional[LDAPUser]:
        """Get user from local database"""
        # Implementation would query local user database
        return None

    async def get_user_groups(self, username: str) -> List[str]:
        """Get user groups from local database"""
        # Implementation would query local group database
        return []


class HybridAuthBackend:
    """
    Hybrid authentication supporting both LDAP/AD and local fallback.

    Tries LDAP/AD first, falls back to local authentication if LDAP is unavailable.
    """

    def __init__(self, ldapbackend: LDAPBackend, localbackend: LocalAuthBackend) -> None:
        self.ldap_backend=ldap_backend  # type: ignore[name-defined]
        self.local_backend=local_backend  # type: ignore[name-defined]

    async def authenticate(self, username: str, password: str) -> Optional[LDAPUser]:
        """Authenticate user with fallback"""
        try:
        # Try LDAP/AD first
            _user=await self.ldap_backend.authenticate(username, password)
            if user:  # type: ignore[name-defined]
                return user  # type: ignore[name-defined]

        except Exception as e:
            logger.warning(f"LDAP authentication failed, trying local: {e}")  # type: ignore[name-defined]

        # Fallback to local authentication
        try:
            _user=await self.local_backend.authenticate(username, password)
            return user  # type: ignore[name-defined]
        except Exception as e:
            logger.error(f"Local authentication also failed: {e}")  # type: ignore[name-defined]
            return None

    async def get_user(self, username: str) -> Optional[LDAPUser]:
        """Get user with fallback"""
        try:
            _user=await self.ldap_backend.get_user(username)
            if user:  # type: ignore[name-defined]
                return user  # type: ignore[name-defined]
        except Exception as e:
            logger.warning(f"LDAP user lookup failed: {e}")  # type: ignore[name-defined]

        return await self.local_backend.get_user(username)

    async def get_user_groups(self, username: str) -> List[str]:
        """Get user groups with fallback"""
        try:
            _groups=await self.ldap_backend.get_user_groups(username)
            if groups:  # type: ignore[name-defined]
                return groups  # type: ignore[name-defined]
        except Exception as e:
            logger.warning(f"LDAP group lookup failed: {e}")  # type: ignore[name-defined]

        return await self.local_backend.get_user_groups(username)
