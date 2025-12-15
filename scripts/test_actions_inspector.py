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

"""
Tests for actions_inspector.py
"""


import pytest
import logging
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from actions_inspector import setup_logging, inspect_workflows

def test_setup_logging():
    with patch('logging.basicConfig') as mock_basic_config:
        setup_logging(verbose=True)
        mock_basic_config.assert_called_with(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    with patch('logging.basicConfig') as mock_basic_config:
        setup_logging(verbose=False)
        mock_basic_config.assert_called_with(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

def test_inspect_workflows_directory_not_found():
    with patch('pathlib.Path.exists', return_value=False):
        with patch('logging.error') as mock_logging_error:
            with patch('sys.exit') as mock_exit:
                inspect_workflows(Path("non_existent_dir"))
                mock_logging_error.assert_called()
                mock_exit.assert_called_with(1)

def test_inspect_workflows_success(tmp_path):
    # Create a dummy workflow file
    workflow_dir = tmp_path / "workflows"
    workflow_dir.mkdir()
    (workflow_dir / "test.yml").touch()

    with patch('logging.info') as mock_logging_info:
        inspect_workflows(workflow_dir)
        # Check if logging.info was called for the directory and the file
        assert mock_logging_info.call_count >= 1

