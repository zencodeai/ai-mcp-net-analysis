from ipaddress import ip_network, IPv4Network, IPv6Network

from .type import DataContainer, DataContainerError


class CIDRIPContainer(DataContainer):
    """Subclass for handling IPv4 and IPv6 CIDR IP addresses."""

    def __init__(self, value: str):
        self._network = None
        self._value = value
        self._validate()

    def _validate(self) -> None:
        """Validate the given CIDR IP address."""
        try:
            self._network = ip_network(self._value, strict=False)
            if not isinstance(self._network, (IPv4Network, IPv6Network)):
                raise DataContainerError(f"Invalid CIDR IP address: {self._value} - {self._network.__class__.__name__}")
        except ValueError as e:
            raise DataContainerError(f"Invalid CIDR IP address: {self._value}") from e

    def get_type(self) -> any:
        """Get the type of the CIDR IP address."""
        return self._network.__class__.__name__

    def get_value(self) -> any:
        """Get the value of the CIDR IP address."""
        return self._network.__str__()

    def is_ipv4(self) -> bool:
        """Check if the CIDR IP address is IPv4."""
        return isinstance(self._network, IPv4Network)

    def is_ipv6(self) -> bool:
        """Check if the CIDR IP address is IPv6."""
        return isinstance(self._network, IPv6Network)
