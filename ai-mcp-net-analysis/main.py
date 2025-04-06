from utils import ConfigParser
from utils import Logger, LoggerFactory
from utils import CIDRIPContainer


def _main():
    """
    Main function to run the application.
    """
    # Load the configuration
    cfg_path = "config/config.yaml"  # Path to your config file
    config = ConfigParser.get_config(cfg_path)

    # Access the configuration
    print("Configuration loaded successfully.")
    print(config.config_dict)

    config_data = config.config
    print("Configuration data:")
    print(config_data.logging.file.enabled)
    print(config_data.logging.file.format)
    print(config_data.logging.file.get_value("max_size_mb"))
    print(config_data.logging.file.get_value("test", "default_value"))

    logger: Logger = LoggerFactory.get_logger(config_data)
    logger.log_info("This is an info message.")
    logger.log_warning("This is a warning message.")
    logger.log_error("This is an error message.")
    logger.log_critical("This is a critical message.")
    logger.log_debug("This is a debug message.")

    cidr = CIDRIPContainer("192.168.0.120/24")
    print(f"CIDR: {cidr.get_value()}")
    print(f"Is IPv4: {cidr.is_ipv4()}")
    print(f"Is IPv6: {cidr.is_ipv6()}")


# Application entry point
if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        print(f"An error occurred: {e}")
