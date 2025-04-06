import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


from .logger import AbstractLogger, LoggerError
from ..config import ConfigData

# Constants
FILELOG_PATH = "logs/ai-mcp-net-analysis-server.log"
FILELOG_MAX_SIDE_MB = 10
FILELOG_BACKUP_COUNTS = 5
FILELOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class FileLogger(AbstractLogger):
    """
    A logger that writes log messages to a file.
    """

    def __init__(self, config_data: ConfigData):
        """
        Initialize the FileLogger with configuration data.
        :param config_data: Configuration data for the logger.
        """

        # Check if the config data is valid
        if not config_data.logging.file.enabled:
            raise LoggerError("File logging is not enabled in the configuration.")

        # Get configuration data for logging
        self._name = config_data.logging.name
        self._level = config_data.logging.level
        self._max_size_mb = config_data.logging.file.get_value("max_size_mb", FILELOG_MAX_SIDE_MB)
        self._backup_count = config_data.logging.file.get_value("backup_count", FILELOG_BACKUP_COUNTS)
        self._format = config_data.logging.file.get_value("format", FILELOG_FORMAT)
        self._path = config_data.logging.file.get_value("path", FILELOG_PATH)

        # Create the log directory if it doesn't exist
        log_file = Path(self._path).resolve()
        if not log_file.is_absolute():
            log_file = Path.cwd() / log_file
        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True, exist_ok=True)
        if not log_file.parent.is_dir():
            raise LoggerError(f"Log path is not a directory: {log_file.parent}")
        if not log_file.exists():
            log_file.touch()

        # Create the logger
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(self._level)

        # Create a rotating file handler
        self._handler = RotatingFileHandler(
            filename=self._path,
            maxBytes=self._max_size_mb * 1024 * 1024,  # Convert MB to bytes
            backupCount=self._backup_count,
        )
        self._handler.setLevel(self._level)
        self._handler.setFormatter(logging.Formatter(self._format))
        self._logger.addHandler(self._handler)
        # Set the logger to propagate messages to the root logger
        self._logger.propagate = False

    def log_info(self, message: str) -> None:
        """
        Log an informational message.
        :param message: The message to log.
        """
        self._logger.info(message)

    def log_warning(self, message: str) -> None:
        """
        Log a warning message.
        :param message: The message to log.
        """
        self._logger.warning(message)

    def log_error(self, message: str) -> None:
        """
        Log an error message.
        :param message: The message to log.
        """
        self._logger.error(message)

    def log_critical(self, message: str) -> None:
        """
        Log a critical error message.
        :param message: The message to log.
        """
        self._logger.critical(message)

    def log_debug(self, message: str) -> None:
        """
        Log a debug message.
        :param message: The message to log.
        """
        self._logger.debug(message)
