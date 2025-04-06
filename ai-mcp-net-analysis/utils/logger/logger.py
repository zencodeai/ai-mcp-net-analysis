from abc import ABC, abstractmethod


class LoggerError(Exception):
    """
    Custom exception for logger errors.
    """
    pass


class Logger(ABC):
    """
    A generic abstract logger class that defines the structure for logging.
    Subclasses must implement the log_info, log_warning, and log_error methods.
    """

    @abstractmethod
    def log_info(self, message: str) -> None:
        """
        Log an informational message.
        :param message: The message to log.
        """
        pass

    @abstractmethod
    def log_warning(self, message: str) -> None:
        """
        Log a warning message.
        :param message: The message to log.
        """
        pass

    @abstractmethod
    def log_error(self, message: str) -> None:
        """
        Log an error message.
        :param message: The message to log.
        """
        pass

    @abstractmethod
    def log_critical(self, message: str) -> None:
        """
        Log a critical error message.
        :param message: The message to log.
        """
        pass

    @abstractmethod
    def log_debug(self, message: str) -> None:
        """
        Log a debug message.
        :param message: The message to log.
        """
        pass
