#!/bin/bash
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

# Simple Bind9 health probe for DebVisor

set -euo pipefail

if ! command -v dig >/dev/null 2>&1; then
	echo "chk-bind: dig command not found, skipping check" >&2
	exit 0
fi

if dig +time=1 +tries=1 @127.0.0.1 SOA debvisor.local >/dev/null 2>&1; then
	exit 0
else
	logger "DebVisor: Bind9 health check failed for debvisor.local SOA on 127.0.0.1"
	exit 1
fi
