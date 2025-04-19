import subprocess

from utils import LoggerFactory, Logger


class CmdExecError(Exception):
    """
    Custom exception class for command execution errors.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        logger: Logger = LoggerFactory.get_logger()
        logger.log_debug(message)


class CmdExec:
    """
    Class for executing shell commands safely.
    """

    # Default timeout in s for command execution
    DEFAULT_TIMEOUT = 60

    @staticmethod
    def execute(command: list[str], timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Execute a shell command and return the result.
        :param command: The command to execute as a list of strings.
        :param response_model: The expected response model.
        :param timeout: Timeout for command execution in seconds.
        :return: The result of the command execution.
        """

        # Initialize logger
        logger = LoggerFactory.get_logger()

        cmd_text = ' '.join(command)

        try:
            # Execute the command with a timeout
            logger.log_debug(f"Executing command: {cmd_text}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.log_debug(f"Command executed successfully: {result.stdout}")
            return result.stdout
        except subprocess.TimeoutExpired:
            # If the command times out, we raise a custom exception
            raise CmdExecError("Command execution time out")
        except subprocess.CalledProcessError as e:
            # If the command fails, we raise a custom exception
            if e.returncode != 0:
                raise CmdExecError(f"Command execution failed with return code: {result.returncode}")
            elif result.stderr:
                raise CmdExecError(f"Command error: {result.stderr}")
            else:
                raise CmdExecError(f"Command execution failed: {e}")
        except Exception as e:
            # Catch any other exceptions and raise a custom exception
            raise CmdExecError(f"Command execution error: {e}")
