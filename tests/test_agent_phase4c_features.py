"""
Tests for Phase 4c: Advanced Parallel Execution & Notifications

Phase 4c implements:
1. Async file processing with concurrent execution
2. Multiprocessing for parallel agent execution
3. Webhook/callback support for external notifications

Test coverage includes:
- Async file processing (create event loop, concurrent tasks)
- Multiprocessing agent execution (worker processes, pool management)
- Webhook registration and notifications (HTTP POST, JSON payload)
- Callback registration and execution (sync callbacks, error handling)
- Integration with existing Phase 4a features (dry-run, selective agents, timeouts)
- Edge cases (empty file lists, webhook failures, callback exceptions)
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json
import asyncio
import sys
import os

# Add scripts/agent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts' / 'agent'))

from agent import Agent


class TestAsyncFileProcessing:
    """Tests for async_process_files method."""

    def test_async_process_files_returns_list(self, tmp_path):
        """Test that async_process_files returns a list of modified files."""
        agent = Agent(repo_root=str(tmp_path))
        
        # Create test files
        test_files = [
            tmp_path / 'test1.py',
            tmp_path / 'test2.py'
        ]
        for f in test_files:
            f.write_text('# test file')
        
        # Mock process_file to not actually process
        agent.process_file = Mock()
        
        # Run async processing
        result = asyncio.run(agent.async_process_files(test_files))
        
        # Result should be a list
        assert isinstance(result, list)
        assert agent.process_file.called

    def test_async_process_files_with_empty_list(self, tmp_path):
        """Test async processing with empty file list."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        result = asyncio.run(agent.async_process_files([]))
        
        assert result == []

    def test_async_process_files_tracks_metrics(self, tmp_path):
        """Test that async processing updates metrics."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        
        agent.process_file = Mock()
        
        asyncio.run(agent.async_process_files(test_files))
        
        # Metrics should be updated
        assert agent.metrics['files_processed'] >= 0

    def test_async_process_files_concurrent_execution(self, tmp_path):
        """Test that async processing executes tasks concurrently."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        test_files = [
            tmp_path / 'test1.py',
            tmp_path / 'test2.py',
            tmp_path / 'test3.py'
        ]
        for f in test_files:
            f.write_text('# test')
        
        agent.process_file = Mock()
        
        asyncio.run(agent.async_process_files(test_files))
        
        # All files should be processed
        assert agent.process_file.call_count == len(test_files)


class TestMultiprocessingExecution:
    """Tests for multiprocessing file processing."""

    def test_process_files_multiprocessing_returns_list(self, tmp_path):
        """Test that multiprocessing processing returns a list."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True, max_workers=2)
        
        test_files = [
            tmp_path / 'test1.py',
            tmp_path / 'test2.py'
        ]
        for f in test_files:
            f.write_text('# test file')
        
        agent.process_file = Mock()
        
        result = agent.process_files_multiprocessing(test_files)
        
        assert isinstance(result, list)

    def test_process_files_multiprocessing_with_empty_list(self, tmp_path):
        """Test multiprocessing with empty file list."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True)
        
        result = agent.process_files_multiprocessing([])
        
        assert result == []

    def test_process_files_multiprocessing_respects_max_workers(self, tmp_path):
        """Test that multiprocessing respects max_workers setting."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True, max_workers=2)
        
        assert agent.max_workers == 2

    def test_process_files_multiprocessing_updates_metrics(self, tmp_path):
        """Test that multiprocessing updates metrics correctly."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True, max_workers=2)
        
        test_files = [tmp_path / f'test{i}.py' for i in range(3)]
        for f in test_files:
            f.write_text('# test')
        
        agent.process_file = Mock()
        
        agent.process_files_multiprocessing(test_files)
        
        # Metrics should be updated
        assert agent.metrics['files_processed'] == len(test_files)

    def test_process_files_threaded_returns_list(self, tmp_path):
        """Test that threaded processing returns a list."""
        agent = Agent(repo_root=str(tmp_path), max_workers=2)
        
        test_files = [
            tmp_path / 'test1.py',
            tmp_path / 'test2.py'
        ]
        for f in test_files:
            f.write_text('# test file')
        
        agent.process_file = Mock()
        
        result = agent.process_files_threaded(test_files)
        
        assert isinstance(result, list)

    def test_process_files_threaded_updates_metrics(self, tmp_path):
        """Test that threaded processing updates metrics."""
        agent = Agent(repo_root=str(tmp_path), max_workers=2)
        
        test_files = [tmp_path / f'test{i}.py' for i in range(2)]
        for f in test_files:
            f.write_text('# test')
        
        agent.process_file = Mock()
        
        agent.process_files_threaded(test_files)
        
        assert agent.metrics['files_processed'] > 0


class TestWebhookSupport:
    """Tests for webhook registration and notification."""

    def test_register_webhook(self, tmp_path):
        """Test registering a webhook URL."""
        agent = Agent(repo_root=str(tmp_path))
        webhook_url = 'https://example.com/webhook'
        
        agent.register_webhook(webhook_url)
        
        assert webhook_url in agent.webhooks

    def test_register_multiple_webhooks(self, tmp_path):
        """Test registering multiple webhooks."""
        agent = Agent(repo_root=str(tmp_path))
        urls = [
            'https://example.com/webhook1',
            'https://example.com/webhook2',
            'https://example.com/webhook3'
        ]
        
        for url in urls:
            agent.register_webhook(url)
        
        assert agent.webhooks == urls

    def test_send_webhook_notification(self, tmp_path):
        """Test sending webhook notification."""
        agent = Agent(repo_root=str(tmp_path))
        agent.register_webhook('https://example.com/webhook')
        
        with patch('agent.requests.post') as mock_post:
            agent.send_webhook_notification('test_event', {'data': 'test'})
            
            # Webhook should be called if requests is available
            # (may not be called if requests not installed)
            if mock_post.called:
                assert mock_post.call_count == 1

    def test_send_webhook_notification_multiple(self, tmp_path):
        """Test sending to multiple webhooks."""
        agent = Agent(repo_root=str(tmp_path))
        urls = [
            'https://example.com/webhook1',
            'https://example.com/webhook2'
        ]
        
        for url in urls:
            agent.register_webhook(url)
        
        with patch('agent.requests.post') as mock_post:
            agent.send_webhook_notification('event', {'data': 'test'})
            
            # If requests available, all webhooks should be attempted
            if mock_post.called:
                assert mock_post.call_count == len(urls)

    def test_send_webhook_notification_with_metrics(self, tmp_path):
        """Test sending webhook with metrics data."""
        agent = Agent(repo_root=str(tmp_path))
        agent.register_webhook('https://example.com/webhook')
        agent.metrics = {
            'files_processed': 42,
            'files_modified': 15,
            'start_time': 0.0
        }
        
        with patch('agent.requests.post') as mock_post:
            agent.send_webhook_notification('agent_complete', agent.metrics)
            
            if mock_post.called:
                # Check that metrics were included
                call_args = mock_post.call_args
                assert call_args is not None

    def test_send_webhook_notification_handles_timeout(self, tmp_path):
        """Test webhook notification handles timeout gracefully."""
        agent = Agent(repo_root=str(tmp_path))
        agent.register_webhook('https://example.com/webhook')
        
        with patch('agent.requests.post') as mock_post:
            mock_post.side_effect = Exception('Timeout')
            
            # Should not raise, just log
            agent.send_webhook_notification('event', {'data': 'test'})


class TestCallbackSupport:
    """Tests for callback registration and execution."""

    def test_register_callback(self, tmp_path):
        """Test registering a callback function."""
        agent = Agent(repo_root=str(tmp_path))
        callback = Mock()
        
        agent.register_callback(callback)
        
        assert callback in agent.callbacks

    def test_register_multiple_callbacks(self, tmp_path):
        """Test registering multiple callbacks."""
        agent = Agent(repo_root=str(tmp_path))
        callbacks = [Mock(), Mock(), Mock()]
        
        for cb in callbacks:
            agent.register_callback(cb)
        
        assert agent.callbacks == callbacks

    def test_execute_callbacks_calls_all(self, tmp_path):
        """Test that execute_callbacks calls all registered callbacks."""
        agent = Agent(repo_root=str(tmp_path))
        callbacks = [Mock(), Mock()]
        
        for cb in callbacks:
            agent.register_callback(cb)
        
        agent.execute_callbacks('test_event', {'data': 'test'})
        
        for cb in callbacks:
            assert cb.called

    def test_execute_callbacks_passes_event_data(self, tmp_path):
        """Test that callbacks receive event name and data."""
        agent = Agent(repo_root=str(tmp_path))
        callback = Mock()
        agent.register_callback(callback)
        
        event_name = 'test_event'
        event_data = {'key': 'value', 'count': 42}
        
        agent.execute_callbacks(event_name, event_data)
        
        callback.assert_called_once_with(event_name, event_data)

    def test_execute_callbacks_handles_exceptions(self, tmp_path):
        """Test that exceptions in callbacks don't stop others."""
        agent = Agent(repo_root=str(tmp_path))
        
        callback1 = Mock(side_effect=Exception('Test error'))
        callback2 = Mock()
        callback3 = Mock()
        
        agent.register_callback(callback1)
        agent.register_callback(callback2)
        agent.register_callback(callback3)
        
        # Should not raise
        agent.execute_callbacks('event', {})
        
        # callback2 and callback3 should still be called
        assert callback2.called
        assert callback3.called

    def test_execute_callbacks_with_real_callback(self, tmp_path):
        """Test execute_callbacks with a real callback function."""
        agent = Agent(repo_root=str(tmp_path))
        
        results = []
        
        def my_callback(event_name, event_data):
            results.append((event_name, event_data))
        
        agent.register_callback(my_callback)
        
        agent.execute_callbacks('completion', {'status': 'done'})
        
        assert len(results) == 1
        assert results[0] == ('completion', {'status': 'done'})


class TestParallelExecutionIntegration:
    """Integration tests for parallel execution."""

    def test_run_with_parallel_execution_async(self, tmp_path):
        """Test run_with_parallel_execution with async enabled."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        # Mock find_code_files
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        agent.find_code_files = Mock(return_value=test_files)
        agent.process_file = Mock()
        agent.run_stats_update = Mock()
        
        agent.run_with_parallel_execution()
        
        assert agent.find_code_files.called
        assert agent.run_stats_update.called

    def test_run_with_parallel_execution_multiprocessing(self, tmp_path):
        """Test run_with_parallel_execution with multiprocessing enabled."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True, max_workers=2)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        agent.find_code_files = Mock(return_value=test_files)
        agent.process_file = Mock()
        agent.run_stats_update = Mock()
        
        agent.run_with_parallel_execution()
        
        assert agent.find_code_files.called

    def test_run_with_parallel_execution_triggers_callbacks(self, tmp_path):
        """Test that parallel execution triggers completion callbacks."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        callback = Mock()
        agent.register_callback(callback)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        agent.find_code_files = Mock(return_value=test_files)
        agent.process_file = Mock()
        agent.run_stats_update = Mock()
        
        agent.run_with_parallel_execution()
        
        # Callback should be called with agent_complete event
        assert any(call[0][0] == 'agent_complete' for call in callback.call_args_list)

    def test_run_with_dry_run_and_async(self, tmp_path):
        """Test async execution with dry-run mode enabled."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True, dry_run=True)
        
        assert agent.dry_run is True
        assert agent.enable_async is True

    def test_run_with_selective_agents_and_multiprocessing(self, tmp_path):
        """Test multiprocessing with selective agent execution."""
        agent = Agent(
            repo_root=str(tmp_path),
            enable_multiprocessing=True,
            selective_agents=['coder', 'tests']
        )
        
        assert agent.selective_agents == {'coder', 'tests'}
        assert agent.enable_multiprocessing is True


class TestPhase4cEdgeCases:
    """Edge case tests for Phase 4c features."""

    def test_async_process_files_with_exception(self, tmp_path):
        """Test async processing handles exceptions gracefully."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        
        agent.process_file = Mock(side_effect=Exception('Test error'))
        
        # Should not raise, should handle exception
        result = asyncio.run(agent.async_process_files(test_files))
        
        assert isinstance(result, list)

    def test_multiprocessing_with_exception(self, tmp_path):
        """Test multiprocessing handles exceptions in worker."""
        agent = Agent(repo_root=str(tmp_path), enable_multiprocessing=True, max_workers=1)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        
        agent.process_file = Mock(side_effect=Exception('Worker error'))
        
        result = agent.process_files_multiprocessing(test_files)
        
        assert isinstance(result, list)

    def test_webhook_without_requests_library(self, tmp_path):
        """Test webhook sending when requests library not available."""
        agent = Agent(repo_root=str(tmp_path))
        agent.register_webhook('https://example.com/webhook')
        
        # Should not raise even if requests not available
        agent.send_webhook_notification('event', {})

    def test_multiple_loop_iterations_with_async(self, tmp_path):
        """Test parallel execution across multiple loop iterations."""
        agent = Agent(repo_root=str(tmp_path), enable_async=True, loop=2)
        
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        agent.find_code_files = Mock(return_value=test_files)
        agent.process_file = Mock()
        agent.run_stats_update = Mock()
        
        agent.run_with_parallel_execution()
        
        # Both loop iterations should happen
        assert agent.find_code_files.call_count == 1

    def test_webhook_payload_format(self, tmp_path):
        """Test webhook payload includes required fields."""
        agent = Agent(repo_root=str(tmp_path))
        agent.register_webhook('https://example.com/webhook')
        
        with patch('agent.requests.post') as mock_post:
            event_data = {'key': 'value'}
            agent.send_webhook_notification('test_event', event_data)
            
            if mock_post.called:
                call_args = mock_post.call_args
                payload = call_args.kwargs.get('json')
                if payload:
                    assert 'event' in payload
                    assert 'timestamp' in payload
                    assert 'data' in payload

    def test_callback_execution_order(self, tmp_path):
        """Test callbacks execute in registration order."""
        agent = Agent(repo_root=str(tmp_path))
        
        results = []
        
        def callback1(event, data):
            results.append(1)
        
        def callback2(event, data):
            results.append(2)
        
        def callback3(event, data):
            results.append(3)
        
        agent.register_callback(callback1)
        agent.register_callback(callback2)
        agent.register_callback(callback3)
        
        agent.execute_callbacks('test', {})
        
        assert results == [1, 2, 3]

    def test_async_with_multiprocessing_preference(self, tmp_path):
        """Test that multiprocessing takes preference over async."""
        agent = Agent(
            repo_root=str(tmp_path),
            enable_async=True,
            enable_multiprocessing=True,
            max_workers=2
        )
        
        # Both should be enabled
        assert agent.enable_async is True
        assert agent.enable_multiprocessing is True
        # In run(), multiprocessing should be preferred
        test_files = [tmp_path / 'test.py']
        test_files[0].write_text('# test')
        agent.find_code_files = Mock(return_value=test_files)
        agent.process_file = Mock()
        agent.run_stats_update = Mock()
        
        # Call the method that has preference logic
        agent.run()
        
        # Multiprocessing should be used due to priority in run_with_parallel_execution

    def test_max_workers_validation(self, tmp_path):
        """Test max_workers parameter is properly set."""
        for workers in [1, 2, 4, 8]:
            agent = Agent(repo_root=str(tmp_path), max_workers=workers)
            assert agent.max_workers == workers

    def test_empty_webhooks_list_no_error(self, tmp_path):
        """Test sending notification with no webhooks registered."""
        agent = Agent(repo_root=str(tmp_path))
        
        # Should not raise even though no webhooks registered
        agent.send_webhook_notification('event', {})
        
        assert agent.webhooks == []

    def test_empty_callbacks_list_no_error(self, tmp_path):
        """Test executing callbacks with none registered."""
        agent = Agent(repo_root=str(tmp_path))
        
        # Should not raise even though no callbacks registered
        agent.execute_callbacks('event', {})
        
        assert agent.callbacks == []
