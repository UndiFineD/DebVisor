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
Integration Tests for DebVisor Phase 4 Features.

Tests covering:
- 2FA enrollment and verification
- WebSocket connections and events
- Report generation
- Theme management
- Batch operations
"""

import pytest
from opt.testing.framework import (
    PerformanceTester,
)
from opt.web.panel.auth_2fa import TwoFactorAuthManager
from opt.web.panel.websocket_events import EventFactory, WebSocketEventBus
from opt.web.panel.reporting import (
    HealthReport,
    CapacityPlanningReport,
    HealthMetric,
    StoragePool,
)
from opt.web.panel.theme import ThemeManager, ThemeMode
from opt.web.panel.batch_operations import BatchOperationManager, OperationType


class Test2FAIntegration:
    """Integration tests for 2FA authentication."""

    @pytest.fixture
    def twofa_manager(self) -> None:
        """Create 2FA manager instance."""
        return TwoFactorAuthManager()  # type: ignore[return-value]

    def test_totp_enrollment_flow(self, twofa_manager):
        """Test TOTP enrollment workflow."""
        user_id = "test_user"

        # Initiate enrollment
        enrollment_data = twofa_manager.initiate_enrollment(user_id)

        assert enrollment_data is not None
        assert "enrollment_id" in enrollment_data
        assert "totp_uri" in enrollment_data
        assert "qr_code_base64" in enrollment_data

    def test_totp_token_verification(self, twofa_manager):
        """Test TOTP token verification."""
        # user_id = "test_user"

        # Get TOTP manager
        totp_mgr = twofa_manager.totp_manager
        secret = totp_mgr.generate_secret()

        # Generate token
        import pyotp

        totp = pyotp.TOTP(secret)
        token = totp.now()

        # Verify token
        is_valid = totp_mgr.verify_token(token, secret)
        assert is_valid

    def test_backup_code_generation(self, twofa_manager):
        """Test backup code generation."""
        backup_mgr = twofa_manager.backup_code_manager

        # Generate codes
        codes = backup_mgr.generate_codes()

        assert len(codes) == 9
        # Check format XXXX-XXXX
        for code in codes:
            assert len(code) == 9
            assert code[4] == "-"

    def test_invalid_token_verification(self, twofa_manager):
        """Test invalid token verification."""
        totp_mgr = twofa_manager.totp_manager
        secret = totp_mgr.generate_secret()

        # Invalid token
        is_valid = totp_mgr.verify_token("000000", secret)
        assert not is_valid

    @pytest.mark.asyncio
    async def test_totp_performance(self) -> None:
        """Test TOTP generation performance."""
        twofa_manager = TwoFactorAuthManager()
        totp_mgr = twofa_manager.totp_manager

        # Measure performance
        metrics = PerformanceTester.measure_execution_time(
            totp_mgr.generate_secret, iterations=100
        )

        # Should be fast (< 10ms per operation)
        assert metrics.duration_ms < 10


class TestWebSocketIntegration:
    """Integration tests for WebSocket events."""

    @pytest.fixture
    def event_bus(self) -> None:
        """Create event bus."""
        return WebSocketEventBus()  # type: ignore[return-value]

    @pytest.mark.asyncio
    async def test_event_publish_and_receive(self, event_bus):
        """Test event publishing and receipt."""
        # Subscribe client
        await event_bus.subscribe(
            client_id="client1",
            event_types=["node_status"],
            user_id="user1",
            permissions=["view:node_status"],
        )

        # Publish event
        event = EventFactory.node_status_event("node1", "online")
        await event_bus.publish(event)

        # Receive message
        message = await event_bus.get_message("client1", timeout=1)
        assert message is not None
        assert message.event_type == "node_status"

    @pytest.mark.asyncio
    async def test_rbac_filtering(self, event_bus):
        """Test RBAC-based event filtering."""
        # Subscribe with limited permissions
        await event_bus.subscribe(
            client_id="client1",
            event_types=["node_status"],
            user_id="user1",
            permissions=["view:job_progress"],    # No node_status permission
        )

        # Publish node status event
        event = EventFactory.node_status_event("node1", "online")
        await event_bus.publish(event)

        # Client should not receive (no permission)
        message = await event_bus.get_message("client1", timeout=0.5)
        assert message is None

    @pytest.mark.asyncio
    async def test_multiple_subscribers(self, event_bus):
        """Test multiple clients receiving same event."""
        # Subscribe two clients
        for i in range(1, 3):
            await event_bus.subscribe(
                client_id=f"client{i}",
                event_types=["alert"],
                user_id=f"user{i}",
                permissions=["view:alert"],
            )

        # Publish alert
        event = EventFactory.alert_event("HIGH_MEMORY", "Memory usage high")
        await event_bus.publish(event)

        # Both clients should receive
        for i in range(1, 3):
            message = await event_bus.get_message(f"client{i}", timeout=1)
            assert message is not None
            assert message.event_type == "alert"


class TestReportingIntegration:
    """Integration tests for report generation."""

    def test_health_report_generation(self) -> None:
        """Test health report HTML generation."""
        report = HealthReport()

        # Add metrics
        report.add_metric(
            HealthMetric(
                name="CPU",
                value=75,
                unit="%",
                warning_threshold=80,
                critical_threshold=95,
            )
        )

        # Add node status
        report.add_node_status("node1", "online", 45.0, 60.0, 70.0)

        # Generate HTML
        html = report.generate_html()

        assert "CPU" in html
        assert "node1" in html
        assert "online" in html

    def test_capacity_planning_forecast(self) -> None:
        """Test capacity planning forecasting."""
        report = CapacityPlanningReport()
        report.growth_rate = 0.05    # 5% monthly growth

        # Add pool
        pool = StoragePool(
            pool_id="pool1",
            pool_name="Storage Pool 1",
            used_bytes=5_000_000_000,
            total_bytes=10_000_000_000,
        )
        report.add_pool(pool)

        # Get summary
        summary = report.get_summary()

        assert summary["total_capacity_gb"] == 10.0
        assert summary["total_used_gb"] == 5.0

    def test_recommendations_generation(self) -> None:
        """Test recommendation generation."""
        report = HealthReport()

        # Add critical metric
        report.add_metric(
            HealthMetric(
                name="Memory",
                value=95,    # Critical
                unit="%",
                warning_threshold=80,
                critical_threshold=90,
            )
        )

        # Get recommendations
        recommendations = report.get_recommendations()

        assert len(recommendations) > 0
        assert any("Memory" in rec for rec in recommendations)


class TestThemeIntegration:
    """Integration tests for theme management."""

    @pytest.fixture
    def theme_manager(self) -> None:
        """Create theme manager."""
        return ThemeManager()  # type: ignore[return-value]

    def test_default_themes_available(self, theme_manager):
        """Test that default themes are registered."""
        themes = theme_manager.list_themes()

        assert "light" in themes
        assert "dark" in themes

    def test_theme_switching(self, theme_manager):
        """Test switching between themes."""
        # Switch to dark
        result = theme_manager.set_theme("dark")
        assert result

        # Verify current theme
        css = theme_manager.get_theme_css()
        assert "dark" in css.lower() or "121212" in css    # Dark background color

    def test_css_generation(self, theme_manager):
        """Test CSS variable generation."""
        css = theme_manager.get_theme_css()

        # Check for CSS variables
        assert "--color-primary" in css
        assert "--color-background" in css
        assert "--font-family" in css

    def test_custom_theme_creation(self, theme_manager):
        """Test creating custom theme."""
        custom_colors = {
            "primary": "    #FF0000",  # Red
            "background": "    #FFFFFF",
        }

        custom_theme = theme_manager.create_custom_theme(
            name="custom",
            mode=ThemeMode.LIGHT,
            colors_dict=custom_colors,
        )

        assert custom_theme is not None
        assert custom_theme.name == "custom"


class TestBatchOperationsIntegration:
    """Integration tests for batch operations."""

    @pytest.fixture
    def batch_manager(self) -> None:
        """Create batch operation manager."""
        return BatchOperationManager()  # type: ignore[return-value]

    @pytest.mark.asyncio
    async def test_batch_operation_creation(self, batch_manager):
        """Test creating batch operation."""
        operation = await batch_manager.create_batch_operation(
            op_type=OperationType.CONFIG_UPDATE,
            name="Update Configurations",
            description="Test config update",
            resources=["resource1", "resource2"],
        )

        assert operation.id is not None
        assert operation.type == OperationType.CONFIG_UPDATE

    @pytest.mark.asyncio
    async def test_dry_run_preview(self, batch_manager):
        """Test dry-run preview."""
        operation = await batch_manager.create_batch_operation(
            op_type=OperationType.NODE_REBOOT,
            name="Reboot Nodes",
            description="Test reboot",
            resources=["node1", "node2", "node3"],
        )

        preview = await batch_manager.preview_dry_run(operation)

        assert preview["resource_count"] == 3
        assert preview["rollback_supported"] is not None

    @pytest.mark.asyncio
    async def test_operation_history(self, batch_manager):
        """Test operation history tracking."""
        # Create and complete multiple operations
        for i in range(3):
            await batch_manager.create_batch_operation(
                op_type=OperationType.CONFIG_UPDATE,
                name=f"Operation {i}",
                description=f"Test operation {i}",
                resources=[f"resource{i}"],
            )

        # Get history
        history = batch_manager.get_history(limit=10)

        assert len(history) > 0


class TestEndToEndWorkflow:
    """End-to-end integration tests."""

    @pytest.mark.asyncio
    async def test_2fa_enrollment_workflow(self) -> None:
        """Test complete 2FA enrollment workflow."""
        twofa_manager = TwoFactorAuthManager()
        user_id = "e2e_test_user"

        # Step 1: Initiate enrollment
        enrollment_data = twofa_manager.initiate_enrollment(user_id)
        assert enrollment_data is not None

        # Step 2: Get QR code
        qr_code = enrollment_data.get("qr_code_base64")
        assert qr_code is not None

        # Step 3: Get backup codes
        backup_codes = twofa_manager.backup_code_manager.generate_codes()  # type: ignore[attr-defined]
        assert len(backup_codes) == 9

    @pytest.mark.asyncio
    async def test_monitoring_workflow(self) -> None:
        """Test monitoring workflow with reports and alerts."""
        # Create event bus and report
        event_bus = WebSocketEventBus()
        report = HealthReport()

        # Subscribe to alerts
        await event_bus.subscribe(
            client_id="monitor1",
            event_types=["alert"],
            user_id="monitor",
            permissions=["view:alert"],
        )

        # Add node and metric to report
        report.add_node_status("node1", "online", 50, 60, 70)
        report.add_metric(
            HealthMetric(
                name="CPU",
                value=75,
                unit="%",
                warning_threshold=80,
                critical_threshold=95,
            )
        )

        # Publish alert
        alert_event = EventFactory.alert_event(
            "CPU_WARNING", "CPU usage at 75%", "warning"
        )
        await event_bus.publish(alert_event)

        # Verify alert received
        message = await event_bus.get_message("monitor1", timeout=1)
        assert message is not None
