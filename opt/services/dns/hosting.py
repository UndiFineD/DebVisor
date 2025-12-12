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


"""
DebVisor DNS Hosting Service.

Provides management of customer DNS zones, record validation, and zone file generation.
Supports standard record types (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA).
"""

from __future__ import annotations
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import ipaddress
import re
import logging


import uuid

logger = logging.getLogger(__name__)


class DNSRecordType(Enum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"
    SRV = "SRV"
    CAA = "CAA"


@dataclass
class DNSRecord:
    name: str    # Subdomain or @
    type: DNSRecordType
    value: str
    ttl: int = 3600
    priority: Optional[int] = None    # For MX and SRV
    weight: Optional[int] = None    # For SRV
    port: Optional[int] = None      # For SRV
    flags: Optional[int] = None     # For CAA
    tag: Optional[str] = None       # For CAA
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_bind_line(self, zone_origin: str) -> str:
        """Convert record to BIND zone file format line."""
        name = self.name
        if name == "@":
            name = zone_origin
        elif not name.endswith("."):
            name = f"{name}.{zone_origin}" if zone_origin and not zone_origin.endswith(".") else f"{name}.{zone_origin}"

        # Ensure trailing dot for origin if not present in output logic,
        # but standard BIND usually handles relative names.
        # Let's stick to relative names if possible, or FQDN.
        # Simpler: Use the name as provided if it doesn't end with dot, else treat as FQDN.

        display_name = self.name

        if self.type == DNSRecordType.MX:
            return f"{display_name}\t{self.ttl}\tIN\tMX\t{self.priority}\t{self.value}"
        elif self.type == DNSRecordType.SRV:
            return f"{display_name}\t{self.ttl}\tIN\tSRV\t{self.priority}\t{self.weight}\t{self.port}\t{self.value}"
        elif self.type == DNSRecordType.CAA:
            return f"{display_name}\t{self.ttl}\tIN\tCAA\t{self.flags}\t{self.tag}\t\"{self.value}\""
        elif self.type == DNSRecordType.TXT:
            return f"{display_name}\t{self.ttl}\tIN\tTXT\t\"{self.value}\""
        else:
            return f"{display_name}\t{self.ttl}\tIN\t{self.type.value}\t{self.value}"


@dataclass
class DNSZone:
    domain: str
    customer_id: str
    records: List[DNSRecord] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    soa_email: str = "hostmaster.debvisor.com"
    soa_refresh: int = 14400
    soa_retry: int = 3600
    soa_expire: int = 1209600
    soa_minimum: int = 3600
    serial: int = field(default_factory=lambda: int(datetime.now().strftime("%Y%m%d01")))

    def increment_serial(self) -> None:
        """Increment SOA serial number."""
        today_prefix = int(datetime.now().strftime("%Y%m%d"))
        current_prefix = int(str(self.serial)[:8])

        if today_prefix > current_prefix:
            self.serial = int(f"{today_prefix}01")
        else:
            self.serial += 1
        self.updated_at = datetime.now(timezone.utc)


class DNSHostingService:
    """Service for managing customer DNS zones."""

    def __init__(self) -> None:
        self._zones: Dict[str, DNSZone] = {}
        self._lock = logging.getLogger("DNSLock")    # Placeholder for actual locking if needed

    def create_zone(self, domain: str, customer_id: str, soa_email: Optional[str] = None) -> DNSZone:
        """Create a new DNS zone."""
        if domain in self._zones:
            raise ValueError(f"Zone {domain} already exists.")

        # Basic domain validation
        if not self._is_valid_domain(domain):
            raise ValueError(f"Invalid domain name: {domain}")

        zone = DNSZone(domain=domain, customer_id=customer_id)
        if soa_email:
            zone.soa_email = soa_email

        # Add default NS records
        zone.records.append(DNSRecord(name="@", type=DNSRecordType.NS, value="ns1.debvisor.com."))
        zone.records.append(DNSRecord(name="@", type=DNSRecordType.NS, value="ns2.debvisor.com."))

        self._zones[domain] = zone
        logger.info(f"Created DNS zone {domain} for customer {customer_id}")
        return zone

    def get_zone(self, domain: str) -> Optional[DNSZone]:
        return self._zones.get(domain)

    def delete_zone(self, domain: str) -> None:
        if domain in self._zones:
            del self._zones[domain]
            logger.info(f"Deleted DNS zone {domain}")
        else:
            raise ValueError(f"Zone {domain} not found.")

    def add_record(self, domain: str, record: DNSRecord) -> DNSRecord:
        zone = self.get_zone(domain)
        if not zone:
            raise ValueError(f"Zone {domain} not found.")

        self._validate_record(record)

        zone.records.append(record)
        zone.increment_serial()
        logger.info(f"Added {record.type.value} record to {domain}: {record.name} -> {record.value}")
        return record

    def remove_record(self, domain: str, record_id: str) -> None:
        zone = self.get_zone(domain)
        if not zone:
            raise ValueError(f"Zone {domain} not found.")

        original_count = len(zone.records)
        zone.records = [r for r in zone.records if r.id != record_id]

        if len(zone.records) < original_count:
            zone.increment_serial()
            logger.info(f"Removed record {record_id} from {domain}")
        else:
            raise ValueError(f"Record {record_id} not found in zone {domain}")

    def generate_bind_config(self, domain: str) -> str:
        """Generate BIND zone file content."""
        zone = self.get_zone(domain)
        if not zone:
            raise ValueError(f"Zone {domain} not found.")

        soa_record = (
            f"$ORIGIN {domain}.\n"
            f"$TTL {zone.soa_minimum}\n"
            f"@\tIN\tSOA\tns1.debvisor.com. {zone.soa_email.replace('@', '.')} (\n"
            f"\t\t\t{zone.serial}\t; Serial\n"
            f"\t\t\t{zone.soa_refresh}\t; Refresh\n"
            f"\t\t\t{zone.soa_retry}\t; Retry\n"
            f"\t\t\t{zone.soa_expire}\t; Expire\n"
            f"\t\t\t{zone.soa_minimum}\t; Minimum TTL\n"
            ")\n\n"
        )

        records_str = "\n".join([r.to_bind_line(domain) for r in zone.records])
        return soa_record + records_str + "\n"

    def _is_valid_domain(self, domain: str) -> bool:
        if len(domain) > 255:
            return False
        if domain[-1] == ".":
            domain = domain[:-1]
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in domain.split("."))

    def _validate_record(self, record: DNSRecord) -> None:
        """Validate record content based on type."""
        if record.type == DNSRecordType.A:
            try:
                ipaddress.IPv4Address(record.value)
            except ValueError:
                raise ValueError(f"Invalid IPv4 address: {record.value}")

        elif record.type == DNSRecordType.AAAA:
            try:
                ipaddress.IPv6Address(record.value)
            except ValueError:
                raise ValueError(f"Invalid IPv6 address: {record.value}")

        elif record.type == DNSRecordType.CNAME:
            if not self._is_valid_domain(record.value) and not record.value.endswith('.'):
                # Allow FQDN with trailing dot, or simple hostname
                pass

        elif record.type == DNSRecordType.MX:
            if record.priority is None or not (0 <= record.priority <= 65535):
                raise ValueError("MX record requires priority between 0 and 65535")

        elif record.type == DNSRecordType.SRV:
            if not all(x is not None for x in [record.priority, record.weight, record.port]):
                raise ValueError("SRV record requires priority, weight, and port")
            if not (0 <= record.port <= 65535):  # type: ignore[operator]
                raise ValueError("Invalid port number")

        elif record.type == DNSRecordType.CAA:
            if record.flags is None or record.tag is None:
                raise ValueError("CAA record requires flags and tag")
