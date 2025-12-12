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


"""Validation schemas package."""

from .schemas import (
    # Authentication
    LoginSchema,
    RegisterSchema,
    ChangePasswordSchema,
    # Nodes
    NodeCreateSchema,
    NodeUpdateSchema,
    # Storage
    StoragePoolCreateSchema,
    VolumeCreateSchema,
    # Network
    NetworkCreateSchema,
    # VM/Container
    VMCreateSchema,
    # Backup
    BackupCreateSchema,
    BackupScheduleSchema,
    # Jobs
    JobCreateSchema,
    # Search/Pagination
    PaginationSchema,
    SearchSchema,
    # Helpers
    validate_request_data,
    get_validation_errors,
    # Decorators
    validate_json,
    validate_query_params,
)

__all__ = [
    "LoginSchema",
    "RegisterSchema",
    "ChangePasswordSchema",
    "NodeCreateSchema",
    "NodeUpdateSchema",
    "StoragePoolCreateSchema",
    "VolumeCreateSchema",
    "NetworkCreateSchema",
    "VMCreateSchema",
    "BackupCreateSchema",
    "BackupScheduleSchema",
    "JobCreateSchema",
    "PaginationSchema",
    "SearchSchema",
    "validate_request_data",
    "get_validation_errors",
    "validate_json",
    "validate_query_params",
]
