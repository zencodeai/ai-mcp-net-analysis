from utils import CmdExec, CIDRIPContainer, TimeoutSecContainer

from tools import Tools


class ToolsNetDiscovery(Tools):
    """
    Network host discovery class.
    This class is responsible for discovering network hosts and their statuses.
    """

    @classmethod
    def nmap_ping_sweep(cls, ip_cidr: str, timeout_s: int) -> str:
        """
        Perform a ping sweep of a network using nmap.
        :param ip_cidr: The CIDR notation of the IP range to scan.
        :param timeout_s: The timeout for each ping in seconds.
        :return: The XML output from nmap.
        """
        # Validate the CIDR IP address
        cidr = CIDRIPContainer(ip_cidr)

        # Validate the timeout
        timeout = TimeoutSecContainer(timeout_s)

        # Execute the command and capture the output
        command = ["nmap", "-oX", "-", "-sn", "-PE", "--max-retries", "0", "--host-timeout", f"{timeout}s", f"{cidr}"]
        result = CmdExec.execute(command)
        return result
