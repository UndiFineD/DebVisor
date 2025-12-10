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

"""Core Package - Shared Utilities

Provides RPC client, validators, and other shared functionality.
"""

from .rpc_client import get_rpc_client, close_rpc_client, RPCClientError

__all__ = ["get_rpc_client", "close_rpc_client", "RPCClientError"]
