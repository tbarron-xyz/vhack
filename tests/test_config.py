"""
Tests for the AI Agent configuration loader.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add src directory to Python path for testing
test_dir = Path(__file__).parent
project_root = test_dir.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from vhack.config.config_loader import ConfigLoader


def test_config_loader_basic():
    """Test basic configuration loading."""
    # Create a temporary config file
    config_content = """
agent:
  name: "Test Agent"
  version: "1.0.0"

openrouter:
  base_url: "https://openrouter.ai/api/v1"
  model: "test-model"
  max_tokens: 500
  temperature: 0.5
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_path = f.name
    
    try:
        # Test loading
        loader = ConfigLoader(config_path)
        
        # Test basic access
        assert loader.get('agent.name') == "Test Agent"
        assert loader.get('openrouter.model') == "test-model"
        assert loader.get('openrouter.max_tokens') == 500
        
        # Test default values
        assert loader.get('nonexistent.key', 'default') == 'default'
        
        # Test config sections
        agent_config = loader.get_agent_config()
        assert agent_config['name'] == "Test Agent"
        
        openrouter_config = loader.get_openrouter_config()
        assert openrouter_config['model'] == "test-model"
        
    finally:
        # Clean up
        os.unlink(config_path)


def test_config_loader_missing_file():
    """Test handling of missing configuration file."""
    with pytest.raises(FileNotFoundError):
        ConfigLoader("nonexistent_config.yaml")


def test_config_validation():
    """Test configuration validation."""
    # Create a config missing required fields
    config_content = """
agent:
  name: "Test Agent"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_path = f.name
    
    try:
        loader = ConfigLoader(config_path)
        
        # Should raise ValueError for missing required fields
        with pytest.raises(ValueError):
            loader.validate_required_fields()
            
    finally:
        os.unlink(config_path)