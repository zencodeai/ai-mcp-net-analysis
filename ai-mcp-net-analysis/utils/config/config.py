import yaml
import os
from schema import SchemaError
from .schema import config_schema


class ConfigError(Exception):
    """
    Custom exception for configuration errors.
    """
    pass


class ConfigData:
    """
    Class to represent configuration data.
    """

    def __init__(self, data: dict):
        """
        Initialize the ConfigData object with a dictionary.
        :param data: Dictionary containing configuration data.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigData(value)
            elif isinstance(value, list):
                value = [ConfigData(item) if isinstance(item, dict) else item for item in value]
            setattr(self, key, value)

    def __getitem__(self, key: str):
        """
        Get an item from the configuration data using dictionary-like access.
        :param key: Key to access the configuration data.
        :return: The value associated with the key.
        """
        return getattr(self, key)

    def to_dict(self) -> dict:
        """
        Convert the configuration data to a dictionary.
        :return: Dictionary representation of the configuration data.
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigData):
                value = value.to_dict()
            elif isinstance(value, list):
                value = [v.to_dict() if isinstance(v, ConfigData) else v for v in value]
            result[key] = value
        return result

    def __repr__(self):
        """
        String representation of the ConfigData object.
        :return: String representation of the configuration data.
        """
        return f"{self.__class__.__name__}({self.__dict__})"

    def get_value(self, key: str, default: any = None) -> any:
        """
        Get the value of the configuration data.
        :param key: Key to access the configuration data.
        :param default: Default value to return if the value is not set.
        :raises ValueError: If the value is not set and default is None.
        :return: The value of the configuration data.
        """
        if hasattr(self, key):
            return getattr(self, key)
        elif default is None:
            raise ValueError(f"Value '{key}' not set in configuration.")
        # If the value is not set, return the default value
        return default


class ConfigParser:

    def _config_load(self, cfg_path: str) -> None:
        """
        Load the YAML configuration file.
        """
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(f"Config file not found: {cfg_path}")

        with open(cfg_path, 'r') as file:
            try:
                self._config = yaml.safe_load(file)
                self._cfg_path = cfg_path
            except yaml.YAMLError as e:
                raise ConfigError(f"Error parsing YAML file {cfg_path}: {e}")

    def _config_validate(self) -> None:
        """
        Validate the loaded configuration against the schema.
        """
        if self._config is None:
            raise ValueError("Configuration not loaded.")

        try:
            config_schema.validate(self._config)
        except SchemaError as e:
            raise ConfigError(f"Configuration validation error: {e}")

    def __init__(self, cfg_path: str) -> None:
        """
        Initialize the ConfigParser with the path to the YAML config file and a schema.

        :param cfg_path: Path to the YAML configuration file.
        """
        self._cfg_path = None
        self._config = None

        # Load and validate the configuration
        self._config_load(cfg_path)
        self._config_validate()

    @classmethod
    def get_config(cls, cfg_path: str) -> "ConfigParser":
        """
        Factory method to get a Config instance.

        :param cfg_path: Path to the YAML configuration file.
        :return: An instance of Config.
        """
        return cls(cfg_path)

    @property
    def config_dict(self) -> dict:
        """
        Get the loaded configuration.

        :return: The loaded configuration as a dictionary.
        """
        return self._config

    @property
    def config(self) -> ConfigData:
        """
        Get the loaded configuration as a ConfigData object.

        :return: The loaded configuration as a ConfigData object.
        """
        return ConfigData(self._config)
