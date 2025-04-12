from .type import DataContainer, DataContainerError


class TimeoutSecContainer(DataContainer):
    """Subclass for handling timouts in seconds."""

    def __init__(self, value: int, value_min: int = 1, value_max: int = 3600):
        self._value: int = value
        self._value_min: int = value_min
        self._value_max: int = value_max
        self._validate()

    def _validate(self) -> None:
        """Validate the timeout."""
        if self._value < self._value_min or self._value > self._value_max:
            raise DataContainerError(
                f"Timeout value must be between {self._value_min}s and {self._value_max}s, got {self._value}s."
            )

    def get_type(self) -> any:
        """Get the type of the value."""
        return int.__class__.__name__

    def get_value(self) -> any:
        """Get the value of the CIDR IP address."""
        return self._value

    def __str__(self):
        """Return the string representation of the value."""
        return str(self._value)
