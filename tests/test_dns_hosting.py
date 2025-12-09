"""
Tests for DNS Hosting Service.
"""
import pytest
# from opt.services.dns.hosting import DNSHostingService, DNSRecord, DNSRecordType, DNSZone

@pytest.fixture
def dns_service() -> None:
    return DNSHostingService()

def test_create_zone(dns_service):
    zone = dns_service.create_zone("example.com", "cust_123")
    assert zone.domain == "example.com"
    assert zone.customer_id == "cust_123"
    assert len(zone.records) == 2  # 2 default NS records
    assert dns_service.get_zone("example.com") is not None

def test_create_duplicate_zone(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    with pytest.raises(ValueError, match="already exists"):
        dns_service.create_zone("example.com", "cust_456")

def test_invalid_domain(dns_service):
    with pytest.raises(ValueError, match="Invalid domain"):
        dns_service.create_zone("-invalid.com", "cust_123")

def test_add_record_a(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    record = DNSRecord(name="www", type=DNSRecordType.A, value="192.0.2.1")
    dns_service.add_record("example.com", record)
    
    zone = dns_service.get_zone("example.com")
    assert len(zone.records) == 3
    assert zone.records[-1].value == "192.0.2.1"

def test_add_record_invalid_a(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    record = DNSRecord(name="www", type=DNSRecordType.A, value="invalid-ip")
    with pytest.raises(ValueError, match="Invalid IPv4"):
        dns_service.add_record("example.com", record)

def test_add_record_mx(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    record = DNSRecord(name="@", type=DNSRecordType.MX, value="mail.example.com", priority=10)
    dns_service.add_record("example.com", record)
    
    zone = dns_service.get_zone("example.com")
    found = [r for r in zone.records if r.type == DNSRecordType.MX]
    assert len(found) == 1
    assert found[0].priority == 10

def test_remove_record(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    record = DNSRecord(name="www", type=DNSRecordType.A, value="192.0.2.1")
    dns_service.add_record("example.com", record)
    
    zone = dns_service.get_zone("example.com")
    record_id = zone.records[-1].id
    
    dns_service.remove_record("example.com", record_id)
    assert len(zone.records) == 2 # Back to just NS records

def test_generate_bind_config(dns_service):
    dns_service.create_zone("example.com", "cust_123")
    dns_service.add_record("example.com", DNSRecord(name="www", type=DNSRecordType.A, value="192.0.2.1"))
    dns_service.add_record("example.com", DNSRecord(name="@", type=DNSRecordType.MX, value="mail.example.com", priority=10))
    
    config = dns_service.generate_bind_config("example.com")
    
    assert "$ORIGIN example.com." in config
    assert "SOA\tns1.debvisor.com." in config
    assert "www.example.com\t3600\tIN\tA\t192.0.2.1" in config or "www\t3600\tIN\tA\t192.0.2.1" in config
    assert "MX\t10\tmail.example.com" in config

def test_serial_increment(dns_service):
    zone = dns_service.create_zone("example.com", "cust_123")
    initial_serial = zone.serial
    
    dns_service.add_record("example.com", DNSRecord(name="test", type=DNSRecordType.A, value="1.2.3.4"))
    assert zone.serial > initial_serial
