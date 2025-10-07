"""
Configuration loader for the AI Agent.
Handles loading and validation of YAML configuration files.
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


class ConfigLoader:
    """Handles loading and accessing configuration from YAML files."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dictionary containing configuration data
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config if config is not None else {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML configuration: {e}")
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to configuration value (e.g., 'openrouter.model')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_openrouter_config(self) -> Dict[str, Any]:
        """Get OpenRouter specific configuration."""
        return self.get('openrouter', {})
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent specific configuration."""
        return self.get('agent', {})
    
    def get_behavior_config(self) -> Dict[str, Any]:
        """Get behavior specific configuration."""
        return self.get('behavior', {})
    
    def reload(self):
        """Reload configuration from file."""
        self.config = self._load_config()
    
    def validate_required_fields(self):
        """
        Validate that required configuration fields are present.
        
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = [
            'openrouter.base_url',
            'openrouter.model'
        ]
        
        missing_fields = []
        for field in required_fields:
            if self.get(field) is None:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")