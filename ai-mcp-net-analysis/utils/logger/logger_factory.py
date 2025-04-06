from .logger import AbstractLogger, LoggerError
from ..config import ConfigData
from .logger_file import FileLogger


class LoggerFactory:
    """
    A factory class for creating logger instances.
    """

    # Logger singleton instance
    _instance = None

    @classmethod
    def get_logger(cls, config_data: ConfigData) -> AbstractLogger:
        """
        Get the singleton logger instance.
        :param config_data: Configuration data for the logger.
        :return: An instance of a logger.
        """
        if cls._instance is None:
            # Get logger type
            logger_type = config_data.logging.type

            # Create logger instance based on type
            match logger_type:
                case "file":
                    cls._instance = FileLogger(config_data)
                case _:
                    raise LoggerError(f"Unsupported logger type: {logger_type}")

        return cls._instance
