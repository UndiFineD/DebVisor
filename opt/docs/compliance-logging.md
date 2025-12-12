# DebVisor Compliance Logging Configuration

## Overview

This directory contains configurations for enterprise-grade compliance logging with immutable audit trails.

## Architecture

    VM Hosts -> Fluent Bit -> Kafka -> Logstash -> {Elasticsearch, S3}
                                                  v           v
                                              Grafana   Immutable Archive

## Components

### Fluent Bit Agent

- **Location**: `config/fluent-bit/debvisor-compliance.conf`

- **Purpose**: Tails VM logs and ships to Kafka

- **Features**: JSON parsing, tenant tagging, retry logic

### Kafka Topic

    kafka-topics.sh --create \

      - -topic debvisor-compliance-logs \

      - -bootstrap-server kafka01:9092 \

      - -replication-factor 3 \

      - -partitions 12

### Logstash Pipeline

- **Location**: `config/logstash/debvisor-compliance-pipeline.conf`

- **Purpose**: Dual-path output (Elasticsearch + S3)

- **Features**:

- Real-time indexing for Grafana dashboards

- Immutable S3 archive with object lock

### S3 Bucket Configuration

## Enable object lock for WORM compliance

    aws s3api create-bucket \

      - -bucket debvisor-compliance-archive \

      - -object-lock-enabled-for-bucket

## Set default retention

    aws s3api put-object-lock-configuration \

      - -bucket debvisor-compliance-archive \

      - -object-lock-configuration \

      'ObjectLockEnabled=Enabled,Rule={DefaultRetention={Mode=COMPLIANCE,Years=7}}'

## Log Schema

### MFA Enforcement Event

    {
      "timestamp": "2025-11-23T07:59:00Z",
      "host": "vm-prod-001.debvisor.local",
      "tenant": "tenant1.local",
      "service": "ssh",
      "event_type": "mfa_enforcement",
      "action": "enabled",
      "initiator": "automation_playbook",
      "details": {
        "pam_module": "libpam-google-authenticator",
        "sshd_config": "AuthenticationMethods publickey,keyboard-interactive"
      },
      "method": "ansible",
      "reason": "Grafana compliance alert: MFA drift detected",
      "severity": "critical",
      "compliance_tag": "MFA",
      "audit_id": "MFA-20251123-001",
      "immutable_archive": true,
      "signature": "sha256:8f3a9c2e..."
    }

### Privileged Command Audit

    {
      "timestamp": "2025-11-23T08:15:30Z",
      "host": "node1.debvisor.local",
      "user": "admin",
      "event_type": "privileged_command",
      "command": "/usr/bin/systemctl restart bind9",
      "audit_id": "EXEC-20251123-042",
      "immutable_archive": true
    }

## Grafana Integration

Compliance logs are queryable via:

- **Elasticsearch datasource**: Real-time dashboards

- **Loki datasource**: Log search and analysis

## Security Features

1.**Tamper Resistance**: S3 object lock prevents log deletion/modification
1.**Cryptographic Signatures**: Each log entry hashed for integrity verification
1.**Multi-Tenant Isolation**: Tenant tags separate compliance evidence
1.**Audit Trail**: Complete chain from alert -> remediation -> verification

## Deployment

1. Deploy Fluent Bit config to all VM hosts

1. Create Kafka topic with replication

1. Deploy Logstash pipeline with credentials

1. Configure S3 bucket with object lock

1. Import Grafana compliance dashboard

## Retrieval for Auditors

## Query Elasticsearch for specific audit ID

    curl -X GET "[http://es01:9200/debvisor-compliance-*/_search"](http://es01:9200/debvisor-compliance-*/_search") \

      - H 'Content-Type: application/json' \

      - d '{"query": {"term": {"audit_id": "MFA-20251123-001"}}}'

## Download from S3 immutable archive

    aws s3 cp s3://debvisor-compliance-archive/logs/2025/11/23/ . --recursive

## Compliance Tags

- `MFA`: Multi-factor authentication events

- `Audit`: Configuration changes tracked by auditd

- `ImmutableLogs`: Log storage status verification

- `PrivilegedCommands`: Root/sudo command execution

- `AuthFailures`: Failed authentication attempts
