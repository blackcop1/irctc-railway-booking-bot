"""Configuration management for IRCTC booking bot"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the booking bot"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from YAML file
        
        Args:
            config_path: Path to configuration file. Defaults to config/config.yml
        """
        if config_path is None:
            config_path = "config/config.yml"
        
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        
        if self.config_path.exists():
            self.load()
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    def load(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'irctc.username')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'irctc.username')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save configuration to YAML file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save configuration: {e}")
    
    def validate(self) -> bool:
        """Validate required configuration fields
        
        Returns:
            True if configuration is valid
        """
        required_fields = [
            'irctc.username',
            'irctc.password',
            'irctc.tatkal_time',
            'captcha.provider',
            'captcha.api_key',
        ]
        
        for field in required_fields:
            if not self.get(field):
                raise ValueError(f"Missing required configuration: {field}")
        
        return True
    
    def __repr__(self) -> str:
        return f"Config(path={self.config_path})"
