# Phase 5 Week 3-4 Deployment Guide

**Updated:** January 15, 2025
**Status:** Production Ready
**Target Deployment:** January 20-25, 2025

---

## Pre-Deployment Checklist

### Environment Validation

- [ ] Python 3.8+ installed
- [ ] All dependencies available (psutil, Flask, SQLAlchemy, etc.)
- [ ] Database migrations completed
- [ ] SMTP credentials configured (for reporting)
- [ ] Adequate disk space (minimum 500MB)
- [ ] Network connectivity verified

### Code Quality Verification

```bash
# Run linting
python fix_markdown_lint_final.py *.md

# Run unit tests
python -m pytest tests/test_analytics.py -v
python -m pytest tests/test_diagnostics.py -v
python -m pytest tests/test_multi_cluster.py -v

# Check type hints
mypy opt/web/panel/analytics.py
mypy opt/services/diagnostics.py
mypy opt/services/multi_cluster.py
```python

---

## Installation Steps

### Step 1: Backup Current System

```bash
# Create backup of current configuration
tar -czf debvisor_backup_$(date +%Y%m%d_%H%M%S).tar.gz /path/to/debvisor

# Verify backup
tar -tzf debvisor_backup_*.tar.gz | head -20
```python

### Step 2: Deploy Core Modules

```bash
# Copy new modules to deployment directory
cp opt/web/panel/analytics.py /opt/debvisor/web/panel/
cp opt/services/reporting_scheduler.py /opt/debvisor/services/
cp opt/services/diagnostics.py /opt/debvisor/services/
cp opt/services/multi_cluster.py /opt/debvisor/services/
cp -r opt/netcfg-tui /opt/debvisor/

# Verify file permissions
chmod 644 /opt/debvisor/web/panel/analytics.py
chmod 644 /opt/debvisor/services/*.py
chmod 755 /opt/debvisor/netcfg-tui/main.py
```python

### Step 3: Install Python Dependencies

```bash
# Update pip
pip install --upgrade pip

# Install required packages if not present
pip install psutil     # For diagnostics
pip install python-dotenv  # For environment config
pip install APScheduler    # For report scheduling (optional)

# Verify installations
python -c "import psutil; print(psutil.cpu_percent())"
python -c "import APScheduler; print('APScheduler OK')"
```python

### Step 4: Configure Environment

Create or update `/opt/debvisor/.env`:

```bash
# Analytics Configuration
ANALYTICS_RETENTION_DAYS=35
ANALYTICS_BATCH_SIZE=1000

# Reporting Configuration
SMTP_HOST=mail.example.com
SMTP_PORT=587
SMTP_USER=reports@example.com
SMTP_PASSWORD=your_secure_password
SMTP_TLS=true
REPORT_FROM_EMAIL=reports@example.com

# Diagnostics Configuration
DIAGNOSTICS_CHECK_TIMEOUT=30
DIAGNOSTICS_HISTORY_LIMIT=1000

# Multi-Cluster Configuration
CLUSTER_HEARTBEAT_TIMEOUT=30
SERVICE_DISCOVERY_CACHE_TTL=300
```python

### Step 5: Database Migrations

```bash
# If using database for persistent storage
python opt/models/migrations.py apply

# Verify migration
python opt/models/migrations.py status
```python

### Step 6: Deploy Test Suites

```bash
# Copy test files
cp tests/test_analytics.py tests/
cp tests/test_diagnostics.py tests/
cp tests/test_multi_cluster.py tests/

# Run smoke tests
python -m pytest tests/test_analytics.py::TestAnalyticsEngine::test_record_metric -v
python -m pytest tests/test_diagnostics.py::TestDiagnosticsFramework::test_register_check -v
python -m pytest tests/test_multi_cluster.py::TestClusterRegistry::test_add_cluster -v
```python

### Step 7: Deploy Documentation

```bash
# Copy API documentation
cp API_DOCUMENTATION.md /opt/debvisor/docs/
cp PHASE_5_WEEK_3_4_IMPLEMENTATION_SUMMARY.md /opt/debvisor/docs/

# Update main README
echo "## Phase 5 Week 3-4 Features" >> /opt/debvisor/README.md
echo "- Advanced Analytics Dashboard" >> /opt/debvisor/README.md
echo "- Custom Report Scheduling" >> /opt/debvisor/README.md
echo "- Advanced Diagnostics Framework" >> /opt/debvisor/README.md
echo "- Network Configuration TUI" >> /opt/debvisor/README.md
echo "- Multi-Cluster Foundation" >> /opt/debvisor/README.md
```python

---

## Integration Steps

### Analytics Dashboard Integration

```bash
# Create Flask blueprint (if not exists)
cat > opt/web/panel/blueprints/analytics_bp.py << 'EOF'
from flask import Blueprint, jsonify, request
from opt.web.panel.analytics import AnalyticsEngine, MetricType, TimeGranularity

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')
engine = AnalyticsEngine()

@analytics_bp.route('/record', methods=['POST'])
def record_metric():
    data = request.json
    success = engine.record_metric(
        metric_type=MetricType[data['type']],
        value=data['value'],
        resource_id=data['resource_id'],
        tags=data.get('tags')
    )
    return jsonify({'success': success}), 200 if success else 400

@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    time_window = request.args.get('time_window', 3600, type=int)
    summary = engine.get_dashboard_summary(time_window)
    return jsonify(summary), 200

@analytics_bp.route('/anomalies/<metric_type>', methods=['GET'])
def get_anomalies(metric_type):
    resource_id = request.args.get('resource_id')
    anomalies = engine.detect_anomalies(
        metric_type=MetricType[metric_type],
        resource_id=resource_id
    )
    return jsonify({'anomalies': anomalies}), 200
EOF

# Register blueprint in app.py
cat >> opt/web/panel/app.py << 'EOF'

from blueprints.analytics_bp import analytics_bp
app.register_blueprint(analytics_bp)
EOF
```python

### Report Scheduling Integration

```bash
# Create Flask blueprint
cat > opt/web/panel/blueprints/reports_bp.py << 'EOF'
from flask import Blueprint, jsonify, request
from opt.services.reporting_scheduler import ReportScheduler, ReportFrequency

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')
scheduler = ReportScheduler()

@reports_bp.route('/schedule', methods=['POST'])
def schedule_report():
    data = request.json
    result = scheduler.schedule_report(
        report_id=data['id'],
        name=data['name'],
        template_id=data['template'],
        frequency=ReportFrequency[data['frequency']],
        recipients=data['recipients'],
        parameters=data.get('parameters', {})
    )
    return jsonify({'success': result}), 200 if result else 400

@reports_bp.route('/status', methods=['GET'])
def get_status():
    status = scheduler.get_scheduler_status()
    return jsonify(status), 200

@reports_bp.route('/history/<report_id>', methods=['GET'])
def get_history(report_id):
    limit = request.args.get('limit', 100, type=int)
    history = scheduler.get_report_history(report_id, limit)
    return jsonify({'reports': [asdict(r) for r in history]}), 200
EOF

# Register blueprint
cat >> opt/web/panel/app.py << 'EOF'

from blueprints.reports_bp import reports_bp
app.register_blueprint(reports_bp)
EOF
```python

### Diagnostics Integration

```bash
# Create Flask blueprint [2]
cat > opt/web/panel/blueprints/diagnostics_bp.py << 'EOF'
from flask import Blueprint, jsonify
from opt.services.diagnostics import DiagnosticsFramework

diagnostics_bp = Blueprint('diagnostics', __name__, url_prefix='/api/diagnostics')
framework = DiagnosticsFramework()

@diagnostics_bp.route('/run', methods=['POST'])
def run_diagnostics():
    report = framework.run_diagnostics()
    return jsonify({
        'health_score': report.overall_health_score,
        'issues': report.issues_found,
        'summary': report.summary,
        'checks': [asdict(c) for c in report.checks]
    }), 200

@diagnostics_bp.route('/summary', methods=['GET'])
def get_summary():
    summary = framework.get_diagnostics_summary()
    return jsonify(summary), 200

@diagnostics_bp.route('/trend', methods=['GET'])
def get_trend():
    hours = request.args.get('hours', 24, type=int)
    trend = framework.get_health_trend(hours)
    return jsonify({'trend': trend}), 200
EOF

# Register blueprint [2]
cat >> opt/web/panel/app.py << 'EOF'

from blueprints.diagnostics_bp import diagnostics_bp
app.register_blueprint(diagnostics_bp)
EOF
```python

### Multi-Cluster Integration

```bash
# Create Flask blueprint [3]
cat > opt/web/panel/blueprints/clusters_bp.py << 'EOF'
from flask import Blueprint, jsonify, request
from opt.services.multi_cluster import MultiClusterManager

clusters_bp = Blueprint('clusters', __name__, url_prefix='/api/clusters')
manager = MultiClusterManager()

@clusters_bp.route('/add', methods=['POST'])
def add_cluster():
    data = request.json
    cluster_id = manager.add_cluster(
        name=data['name'],
        endpoint=data['endpoint'],
        region=data['region'],
        version=data['version']
    )
    return jsonify({'cluster_id': cluster_id}), 201

@clusters_bp.route('/status', methods=['GET'])
def get_status():
    status = manager.get_federation_status()
    return jsonify(status), 200

@clusters_bp.route('/discover/<service_name>', methods=['GET'])
def discover_service(service_name):
    region = request.args.get('region')
    service = manager.discovery.discover_service(service_name, region)
    if service:
        return jsonify({'service': asdict(service)}), 200
    return jsonify({'error': 'Not found'}), 404
EOF

# Register blueprint [3]
cat >> opt/web/panel/app.py << 'EOF'

from blueprints.clusters_bp import clusters_bp
app.register_blueprint(clusters_bp)
EOF
```python

---

## Verification Tests

### Test 1: Analytics Recording and Retrieval

```bash
python << 'PYTEST'
from opt.web.panel.analytics import AnalyticsEngine, MetricType
import time

engine = AnalyticsEngine()

# Record metrics
for i in range(100):
    engine.record_metric(
        metric_type=MetricType.CPU_USAGE,
        value=50 + (i % 20),
        resource_id="test-node"
    )
    time.sleep(0.01)

# Verify
summary = engine.get_dashboard_summary()
assert summary is not None
assert 'metrics' in summary
print("? Analytics test passed")
PYTEST
```python

### Test 2: Diagnostics Framework

```bash
python << 'PYTEST'
from opt.services.diagnostics import DiagnosticsFramework

framework = DiagnosticsFramework()
report = framework.run_diagnostics()

assert report is not None
assert 0 <= report.overall_health_score <= 100
assert len(report.checks) > 0
print("? Diagnostics test passed")
PYTEST
```python

### Test 3: Multi-Cluster Manager

```bash
python << 'PYTEST'
from opt.services.multi_cluster import MultiClusterManager

manager = MultiClusterManager()
cluster_id = manager.add_cluster(
    name="test-cluster",
    endpoint="http://test.local:6443",
    region="us-west",
    version="1.28.0"
)

assert cluster_id is not None
cluster = manager.registry.get_cluster(cluster_id)
assert cluster.name == "test-cluster"
print("? Multi-cluster test passed")
PYTEST
```python

### Test 4: Network Config

```bash
python << 'PYTEST'
from opt.netcfg_tui.main import NetworkConfig

config = NetworkConfig()
config.save_config('/tmp/test_config.json')

assert os.path.exists('/tmp/test_config.json')
config2 = NetworkConfig()
assert config2.load_config('/tmp/test_config.json')
print("? Network config test passed")
PYTEST
```python

---

## Rollback Plan

### If Critical Issues Found

```bash
# Immediate: Stop application
systemctl stop debvisor

# Restore from backup
tar -xzf debvisor_backup_YYYYMMDD_HHMMSS.tar.gz -C /

# Restart
systemctl start debvisor

# Verify [2]
curl http://localhost:8000/api/health
```python

### Gradual Rollback (If Issues in Production)

```bash
# Disable new features via configuration
export ANALYTICS_ENABLED=false
export REPORTING_ENABLED=false
export DIAGNOSTICS_ENABLED=false

# Restart application
systemctl restart debvisor

# System continues with Phase 5 Week 1-2 features
```python

---

## Monitoring and Health Checks

### Post-Deployment Monitoring

```bash
# Check application health
curl -s http://localhost:8000/api/health | jq .

# Monitor error logs
tail -f /var/log/debvisor/error.log

# Monitor performance
tail -f /var/log/debvisor/performance.log

# Check diagnostics
curl -s http://localhost:8000/api/diagnostics/summary | jq .
```python

### Alerting Configuration

```bash
# Alert if health score drops below 80%
# Alert if errors per minute exceed 10
# Alert if API response time exceeds 1000ms
# Alert if disk usage exceeds 80%
```python

---

## Performance Benchmarks

Expected performance after deployment:

| Operation | Baseline | Target | Status |
|-----------|----------|--------|--------|
| Metric record | <1ms | <2ms | ? |
| Anomaly detection | <100ms | <150ms | ? |
| Report generation | 5-10s | 15-20s | ? |
| Diagnostics run | 1-2s | 3-5s | ? |
| Service discovery | <50ms | <100ms | ? |

---

## Support and Troubleshooting

### Common Issues

**Issue 1: SMTP Delivery Fails**
```python
Solution: Verify credentials in .env file
$ echo $SMTP_PASSWORD | wc -c  # Should be reasonable length
```python

**Issue 2: High Memory Usage**
```python
Solution: Reduce ANALYTICS_RETENTION_DAYS
$ export ANALYTICS_RETENTION_DAYS=7
$ systemctl restart debvisor
```python

**Issue 3: Slow Diagnostics**
```python
Solution: Increase CHECK_TIMEOUT
$ export DIAGNOSTICS_CHECK_TIMEOUT=60
$ systemctl restart debvisor
```python

### Support Contact

- Documentation: `/opt/debvisor/docs/API_DOCUMENTATION.md`
- Issues: `https://github.com/debvisor/issues`
- Email: `support@debvisor.local`

---

## Deployment Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Environment Setup | 1 hour | Ready |
| Code Deployment | 30 min | Ready |
| Integration | 2 hours | Ready |
| Testing | 2 hours | Ready |
| **Total** | **5.5 hours** | **Ready** |

**Estimated Deployment Window:** 8:00 AM - 1:30 PM (minimal impact)

---

## Success Criteria

Deployment successful if:

- ? All 37+ unit tests pass
- ? Health score > 80%
- ? API response time < 500ms
- ? No critical errors in logs
- ? All features accessible via API
- ? Diagnostics report working
- ? Analytics dashboard responsive
- ? Reports scheduled and delivering

---

## Post-Deployment Steps

1. Monitor error logs for 24 hours
1. Run daily diagnostics checks
1. Verify report delivery (next scheduled time)
1. Collect performance metrics
1. User acceptance testing
1. Update operations runbook
1. Document any issues/learnings

---

**Deployment Ready:** ? January 15, 2025
