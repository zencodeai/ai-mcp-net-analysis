from abc import ABC, abstractmethod


class DataContainerError(Exception):
    """
    Custom exception for data container errors.
    """
    pass


class DataContainer(ABC):
    """
    Abstract root class for data container and validation.
    """

    @abstractmethod
    def _validate(self) -> None:
        """
        Validate the given data against the container's rules.
        Must be implemented by subclasses.
        :raises DataContainerError: If validation fails.
        """
        pass

    @abstractmethod
    def get_type(self) -> any:
        """
        Get the type or schema of the data this container handles.
        Must be implemented by subclasses.
        :return: The type or schema.
        """
        pass

    @abstractmethod
    def get_value(self) -> any:
        """
        Get the value of the data this container holds.
        Must be implemented by subclasses.
        :return: The value of the data.
        """
        pass
