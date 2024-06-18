"""Class for Filter logs and logging logic."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from opsdroid.const import DEFAULT_LOG_FILENAME, __version__

branch_coverage = {} 

def initialize_coverage(func_name, num_branches):
    branch_coverage[func_name] = [False] * num_branches

def mark_branch(func_name, branch_id):
    branch_coverage[func_name][branch_id] = True

def report_coverage():
    total_branches = 0
    reached_branches = 0
    
    for func_name, branches in branch_coverage.items():
        func_total = len(branches)
        func_reached = sum(branches)
        
        total_branches += func_total
        reached_branches += func_reached
        
        coverage_percentage = (func_reached / func_total) * 100 if func_total > 0 else 0
        
        print(f"Coverage for {func_name}:")
        for i, reached in enumerate(branches):
            print(f"  Branch {i}: {'Reached! ✅' if reached else 'Not Reached ❌'}")
        print(f"  Function coverage: {coverage_percentage:.2f}%\n")
    
    overall_coverage = (reached_branches / total_branches) * 100 if total_branches > 0 else 0
    print(f"Overall branch coverage: {overall_coverage:.2f}%")

initialize_coverage("ParsingFilter.__init__", 3)
initialize_coverage("ParsingFilter.filter", 2)
initialize_coverage("set_formatter_string", 3)
initialize_coverage("configure_logging", 8)
initialize_coverage("get_logging_level", 5)

_LOGGER = logging.getLogger(__name__)


class ParsingFilter(logging.Filter):
    """Class that filters logs."""

    def __init__(self, config, *parse_list):
        """Create object to implement filtering."""
        super(ParsingFilter, self).__init__()
        self.config = config
        self.parse_list = []
        try:
            if (
                self.config["filter"]["whitelist"]
                and self.config["filter"]["blacklist"]
            ):
                mark_branch("ParsingFilter.__init__", 0)
                _LOGGER.warning(
                    "Both whitelist and blacklist filters found in configuration. "
                    "Only one can be used at a time - only the whitelist filter will be used."
                )
                self.parse_list = [
                    logging.Filter(name) for name in parse_list[0]["whitelist"]
                ]
            else:
                mark_branch("ParsingFilter.__init__", 1)
        except KeyError:
            mark_branch("ParsingFilter.__init__", 2)
            self.parse_list = parse_list[0].get("whitelist") or parse_list[0].get(
                "blacklist"
            )
            self.parse_list = [logging.Filter(name) for name in self.parse_list]

    def filter(self, record):
        """Apply filter to the log message.

        This is a subset of Logger.filter, this method applies the logger
        filters and returns a bool. If the value is true the record will
        be passed to the handlers and the log shown. If the value is
        false it will be ignored.

        Args:
            record: a log record containing the log message and the
                name of the log - example: opsdroid.core.

        Returns:
            Boolean: If True - pass the log to handler.

        """

        if self.config["filter"].get("whitelist"):
            mark_branch("ParsingFilter.filter", 0)
            return any(name.filter(record) for name in self.parse_list)
        else:
            mark_branch("ParsingFilter.filter",1)
            return not any(name.filter(record) for name in self.parse_list)


def set_formatter_string(config: dict):
    """Set the formatter string dependending on the config.

    Currently our logs allow you to pass different configuration parameters to
    format the logs that are returned to us. This is a helper function to handle
    these cases.

    Args:
        config: contains only the logging section of the configuration since we
            don't care about anything else for logs.

    """
    formatter_str = "%(levelname)s %(name)s"

    if config.get("formatter"):
        mark_branch("set_formatter_string",0)
        return config["formatter"]

    if config.get("extended"):
        mark_branch("set_formatter_string",1)
        formatter_str += ".%(funcName)s():"

    if config.get("timestamp"):
        mark_branch("set_formatter_string",2)
        formatter_str = "%(asctime)s " + formatter_str

    formatter_str += " %(message)s"

    return formatter_str


def configure_logging(config):
    """Configure the root logger based on user config."""
    rootlogger = logging.getLogger()
    while rootlogger.handlers:
        rootlogger.handlers.pop()

    try:
        if config["path"]:
            logfile_path = os.path.expanduser(config["path"])
        else:
            logfile_path = config["path"]
    except KeyError:
        logfile_path = DEFAULT_LOG_FILENAME

    if logfile_path:
        logdir = os.path.dirname(os.path.realpath(logfile_path))
        if not os.path.isdir(logdir):
            os.makedirs(logdir)

    log_level = get_logging_level(config.get("level", "info"))
    rootlogger.setLevel(log_level)
    formatter_str = set_formatter_string(config)
    formatter = logging.Formatter(formatter_str)
    handler = None

    if config.get("rich") is not False:
        mark_branch("configure_logging", 0)
        handler = RichHandler(
            rich_tracebacks=True,
            show_time=config.get("timestamp", True),
            show_path=config.get("extended", True),
        )

    if logfile_path:
        mark_branch("configure_logging", 1)
        file_handler = RotatingFileHandler(
            logfile_path, maxBytes=config.get("file-size", 50e6)
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        rootlogger.addHandler(file_handler)

    # If we are running in a non-interactive shell (without a tty)
    # then use simple logging instead of rich logging
    # Config value always overrides
    running_in_non_interactive_shell = False
    console = config.get("test_logging_console", sys.stderr)
    if config.get("console") is True:
        mark_branch("configure_logging", 2)
        handler = logging.StreamHandler(stream=console)
        handler.setFormatter(formatter)
    else:
        if config.get("console") is None and not console.isatty():
            mark_branch("configure_logging", 3)
            running_in_non_interactive_shell = True
            handler = logging.StreamHandler(stream=console)
            handler.setFormatter(formatter)

    # If we still don't have the handler, we are assuming that
    # the user wants to switch off logging, let's log only
    # Critical errors
    if not handler:
        mark_branch("configure_logging", 4)
        handler = logging.StreamHandler(stream=console)
        handler.setFormatter(formatter)
        log_level = get_logging_level("critical")

    if config.get("filter") and handler:
        mark_branch("configure_logging", 5)
        handler.addFilter(ParsingFilter(config, config["filter"]))
    if handler:
        mark_branch("configure_logging", 6)
        handler.setLevel(log_level)
        rootlogger.addHandler(handler)

    _LOGGER.info("=" * 40)
    _LOGGER.info("Started opsdroid %s.", __version__)
    if running_in_non_interactive_shell:
        mark_branch("configure_logging", 7)
        _LOGGER.warning(
            "Running in non-interactive shell - falling back to simple logging. You can override this using 'logging.config: false'"
        )


def get_logging_level(logging_level):
    """Get the logger level based on the user configuration.

    Args:
        logging_level: logging level from config file

    Returns:
        logging LEVEL ->
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0

    """
    if logging_level == "critical":
        mark_branch("get_logging_level", 0)
        return logging.CRITICAL

    if logging_level == "error":
        mark_branch("get_logging_level", 1)
        return logging.ERROR
    
    if logging_level == "warning":
        mark_branch("get_logging_level", 2)
        return logging.WARNING

    if logging_level == "debug":
        mark_branch("get_logging_level", 3)
        return logging.DEBUG
    else:
        mark_branch("get_logging_level", 4)
    return logging.INFO

# Example usage of the instrumented code
if __name__ == "__main__":
    # Define a configuration dictionary for logging settings
    config = {
        "filter": {
            "whitelist": ["example.whitelist"],
            "blacklist": []
        },
        "path": "logfile.log",
        "level": "debug",
        "formatter": None,
        "extended": True,
        "timestamp": True,
        "rich": True,
        "console": True
    }

    # Test ParsingFilter.__init__ for all branches
    # Case 1: Both whitelist and blacklist filters
    config_case1 = config.copy()
    config_case1["filter"] = {
        "whitelist": ["example.whitelist"],
        "blacklist": ["example.blacklist"]
    }
    parser_case1 = ParsingFilter(config_case1, config_case1["filter"])

    # Case 2: Only whitelist filter
    config_case2 = config.copy()
    config_case2["filter"] = {
        "whitelist": ["example.whitelist"]
    }
    parser_case2 = ParsingFilter(config_case2, config_case2["filter"])

    # Case 3: No whitelist or blacklist filter
    config_case3 = config.copy()
    parser_case3 = ParsingFilter(config_case3, config_case3["filter"])

    # Case 4: Only blacklist filter
    config_case6 = config.copy()
    config_case6["filter"] = {
        "blacklist": ["example.blacklist"]
    }

    # Create a ParsingFilter object with the configurations
    parser1 = ParsingFilter(config_case1, config_case1["filter"])
    parser2 = ParsingFilter(config_case2, config_case2["filter"])
    parser3 = ParsingFilter(config_case6, config_case6["filter"])

    # Create a LogRecord object representing a log message
    record = logging.LogRecord(
        name="example.whitelist", 
        level=logging.DEBUG, 
        pathname="", 
        lineno=0, 
        msg="Test message", 
        args=(), 
        exc_info=None
    )

    # Apply the filter to the log record to see if it passes
    parser1.filter(record)
    parser2.filter(record)
    parser3.filter(record)

    # Set the formatter string based on the configuration
    formatter_string = set_formatter_string(config_case1)
    formatter_string = set_formatter_string(config_case2)
    formatter_string = set_formatter_string(config_case6)

    # Test set_formatter_string for all branches
    formatter_case1 = set_formatter_string(config)
    config_case4 = config.copy()
    config_case4["formatter"] = "custom_formatter"
    formatter_case2 = set_formatter_string(config_case4)
    config_case5 = config.copy()
    config_case5["extended"] = False
    formatter_case3 = set_formatter_string(config_case5)

    # Test configure_logging for all branches
    configure_logging(config)

    # Test get_logging_level for all branches
    level_case1 = get_logging_level("critical")
    level_case2 = get_logging_level("error")
    level_case3 = get_logging_level("warning")
    level_case4 = get_logging_level("debug")
    level_case5 = get_logging_level("info")

    # Call the report_coverage function to report code coverage
    report_coverage()