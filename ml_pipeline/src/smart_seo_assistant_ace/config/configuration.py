"""
Configuration management for SEO Assistant Pipeline
Handles loading and validation of configuration from various sources
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from ..entity import PipelineConfig
from ..constants import (
    GEMINI_MODEL_NAME,
    MAX_RETRIES,
    DEFAULT_TIMEOUT,
    CONTEXT_CACHE_TTL
)


class ConfigurationManager:
    """Manages configuration loading and validation for the SEO pipeline"""
    
    def __init__(self, config_file_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file_path: Optional path to YAML config file
        """
        self.config_file_path = config_file_path
        self.config_data = {}
        
        # Load environment variables
        if load_dotenv:
            load_dotenv()
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from multiple sources"""
        # 1. Load from YAML file if provided
        if self.config_file_path and Path(self.config_file_path).exists():
            self._load_yaml_config()
        
        # 2. Load default config
        self._load_default_config()
        
        # 3. Override with environment variables
        self._load_env_config()
    
    def _load_yaml_config(self):
        """Load configuration from YAML file"""
        if not yaml:
            print("Warning: PyYAML not installed, skipping YAML config loading")
            return
            
        try:
            with open(self.config_file_path, 'r') as file:
                yaml_config = yaml.safe_load(file)
                if yaml_config:
                    self.config_data.update(yaml_config)
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file_path}: {e}")
    
    def _load_default_config(self):
        """Load default configuration values"""
        defaults = {
            "gemini_model": GEMINI_MODEL_NAME,
            "max_retries": MAX_RETRIES,
            "timeout": DEFAULT_TIMEOUT,
            "cache_enabled": True,
            "cache_ttl": CONTEXT_CACHE_TTL,
            "debug_mode": False
        }
        
        # Update with defaults only if not already set
        for key, value in defaults.items():
            if key not in self.config_data:
                self.config_data[key] = value
    
    def _load_env_config(self):
        """Load configuration from environment variables"""
        env_mappings = {
            "GEMINI_MODEL": "gemini_model",
            "MAX_RETRIES": "max_retries",
            "TIMEOUT": "timeout",
            "CACHE_ENABLED": "cache_enabled",
            "CACHE_TTL": "cache_ttl",
            "DEBUG_MODE": "debug_mode"
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert to appropriate type
                self.config_data[config_key] = self._convert_env_value(env_value, config_key)
    
    def _convert_env_value(self, value: str, key: str) -> Any:
        """Convert environment variable string to appropriate type"""
        # Boolean conversions
        if key in ["cache_enabled", "debug_mode"]:
            return value.lower() in ["true", "1", "yes", "on"]
        
        # Integer conversions
        if key in ["max_retries", "timeout", "cache_ttl"]:
            try:
                return int(value)
            except ValueError:
                print(f"Warning: Invalid integer value for {key}: {value}")
                return self.config_data.get(key, 0)
        
        # String values
        return value
    
    def get_pipeline_config(self) -> PipelineConfig:
        """
        Get validated pipeline configuration
        
        Returns:
            PipelineConfig: Validated configuration object
            
        Raises:
            ValueError: If required configuration is missing
        """
        # Get API key (required) - check both GEMINI_API_KEY and GOOGLE_API_KEY for compatibility
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Get your key from: https://aistudio.google.com/app/apikey"
            )
        
        return PipelineConfig(
            gemini_api_key=api_key,
            gemini_model=self.config_data.get("gemini_model", GEMINI_MODEL_NAME),
            max_retries=self.config_data.get("max_retries", MAX_RETRIES),
            timeout=self.config_data.get("timeout", DEFAULT_TIMEOUT),
            cache_enabled=self.config_data.get("cache_enabled", True),
            cache_ttl=self.config_data.get("cache_ttl", CONTEXT_CACHE_TTL),
            debug_mode=self.config_data.get("debug_mode", False)
        )
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get specific configuration value"""
        return self.config_data.get(key, default)
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration values"""
        self.config_data.update(updates)
    
    def save_config(self, file_path: str):
        """Save current configuration to YAML file"""
        if not yaml:
            raise ImportError("PyYAML not installed, cannot save YAML config")
            
        try:
            with open(file_path, 'w') as file:
                yaml.dump(self.config_data, file, default_flow_style=False)
        except Exception as e:
            raise IOError(f"Could not save config to {file_path}: {e}")
    
    def validate_config(self) -> bool:
        """
        Validate current configuration
        
        Returns:
            bool: True if configuration is valid
        """
        required_keys = ["gemini_model", "max_retries", "timeout"]
        
        for key in required_keys:
            if key not in self.config_data:
                print(f"Error: Missing required configuration: {key}")
                return False
        
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            print("Error: GOOGLE_API_KEY environment variable not found")
            return False
        
        # Validate numeric values
        numeric_keys = ["max_retries", "timeout", "cache_ttl"]
        for key in numeric_keys:
            if key in self.config_data and not isinstance(self.config_data[key], int):
                print(f"Error: {key} must be an integer")
                return False
        
        return True
    
    def __str__(self) -> str:
        """String representation of configuration"""
        config_copy = self.config_data.copy()
        if yaml:
            return f"SEO Pipeline Configuration:\n{yaml.dump(config_copy, default_flow_style=False)}"
        else:
            return f"SEO Pipeline Configuration:\n{config_copy}"


def load_config(config_file: Optional[str] = None) -> PipelineConfig:
    """
    Convenience function to load pipeline configuration
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        PipelineConfig: Loaded and validated configuration
    """
    config_manager = ConfigurationManager(config_file)
    
    if not config_manager.validate_config():
        raise ValueError("Configuration validation failed")
    
    return config_manager.get_pipeline_config()
