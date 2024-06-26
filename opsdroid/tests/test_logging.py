"""Test the logging module."""
import logging
import os
import re
import sys
import tempfile

import rich.logging

from opsdroid.opsdroid_logging import report_coverage
import opsdroid.opsdroid_logging as opsdroid
import pytest
from opsdroid.cli.start import configure_lang
from rich.logging import RichHandler
from io import StringIO

configure_lang({})

def test_set_logging_level():
    assert logging.DEBUG == opsdroid.get_logging_level("debug")
    assert logging.INFO == opsdroid.get_logging_level("info")
    assert logging.WARNING == opsdroid.get_logging_level("warning")
    assert logging.ERROR == opsdroid.get_logging_level("error")
    assert logging.CRITICAL == opsdroid.get_logging_level("critical")
    assert logging.INFO == opsdroid.get_logging_level("")


def test_configure_no_logging():
    config = {"path": False, "console": False, "rich": False}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()

    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    assert rootlogger.handlers[0].level == logging.CRITICAL


def test_configure_file_logging():
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = {"path": os.path.join(tmp_dir, "output.log"), "console": False}

    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 2
    assert isinstance(rootlogger.handlers[0], logging.handlers.RotatingFileHandler)
    assert isinstance(rootlogger.handlers[1], RichHandler)
    assert rootlogger.handlers[0].level == logging.INFO


def test_log_to_file_only(capsys):
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = {
            "path": os.path.join(tmp_dir, "output.log"),
            "console": False,
            "rich": False,
            "filter": {"blacklist": "opsdroid.logging"},
        }
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 2
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    assert rootlogger.handlers[1].level == logging.CRITICAL
    assert isinstance(rootlogger.handlers[0], logging.handlers.RotatingFileHandler)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_configure_file_logging_directory_not_exists(mocker):
    logmock = mocker.patch("logging.getLogger")
    mocklogger = mocker.MagicMock()
    mocklogger.handlers = [True]
    logmock.return_value = mocklogger
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = {
            "path": os.path.join(tmp_dir, "mynonexistingdirectory", "output.log"),
            "console": False,
        }
    opsdroid.configure_logging(config)


def test_configure_console_logging():
    config = {"path": False, "level": "error", "console": True}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    assert rootlogger.handlers[0].level == logging.ERROR


def test_configure_console_blacklist(capsys):
    config = {
        "path": False,
        "level": "error",
        "console": True,
        "filter": {"blacklist": "opsdroid"},
    }

    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    assert rootlogger.handlers[0].level == logging.ERROR

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_configure_console_whitelist():
    config = {
        "path": False,
        "level": "info",
        "console": True,
        "filter": {"whitelist": "opsdroid.logging"},
    }

    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    assert rootlogger.handlers[0].level == logging.INFO


def test_configure_logging_with_timestamp(capsys):
    config = {"path": False, "level": "info", "console": True, "timestamp": True}

    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    captured = capsys.readouterr()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    # Regex to match timestamp: 2020-12-02 17:46:33,158
    regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} INFO opsdroid\.logging"
    assert re.match(regex, captured.err)


def test_configure_extended_logging():
    config = {"path": False, "level": "error", "console": True, "extended": True}

    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)


def test_configure_extended_logging_with_timestamp(capsys):
    config = {
        "path": False,
        "level": "info",
        "console": True,
        "extended": True,
        "timestamp": True,
    }
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    captured = capsys.readouterr()
    assert len(rootlogger.handlers) == 1
    assert isinstance(rootlogger.handlers[0], logging.StreamHandler)
    # Regex to match timestamp: 2020-12-02 17:46:33,158
    regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} INFO opsdroid\.logging\.configure_logging\(\):"
    assert re.match(regex, captured.err)


def test_configure_default_logging(capsys):
    config = {}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert len(rootlogger.handlers), 2
    assert isinstance(rootlogger.handlers[0], logging.handlers.RotatingFileHandler)
    assert rootlogger.handlers[0].level == logging.INFO
    # If running in a non-interactive console the StreamingHandler will be used
    if not sys.stdout.isatty():
        assert isinstance(rootlogger.handlers[1], logging.StreamHandler)
    # If running in an interactive console the RichHandler will be used
    if sys.stdout.isatty():
        assert isinstance(rootlogger.handlers[1], RichHandler)
    assert rootlogger.handlers[1].level == logging.INFO

    captured = capsys.readouterr()
    # StreamingHandler writes to stderr
    if not sys.stdout.isatty():
        assert "Started opsdroid" in captured.err
        # Check if we log a warning message
        assert "falling back to simple logging" in captured.err
    # RichHandler writes to stdout
    if sys.stdout.isatty():
        assert "Started opsdroid" in captured.out
        # Check if we log a warning message
        assert "falling back to simple logging" in captured.out


def test_configure_logging_config_override(capsys):
    # Test overriding the logging via config
    config = {"console": True}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    # Check that we have the correct logging handler
    assert isinstance(rootlogger.handlers[1], logging.StreamHandler)
    captured = capsys.readouterr()
    # If overriding the console from the config the warning message should not be displayed
    assert "falling back to simple logging" not in captured.err

    config = {"console": False}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    # Check that we have the correct logging handler
    assert isinstance(rootlogger.handlers[1], RichHandler)
    captured = capsys.readouterr()
    assert "falling back to simple logging" not in captured.err


def test_configure_logging_fallback_interactive(mocker):
    # Testing interactive shell
    stdout_mock = mocker.patch("sys.stdout")
    stdout_mock.isatty.return_value = "istty"
    config = {"test_logging_console": stdout_mock}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert isinstance(rootlogger.handlers[1], rich.logging.RichHandler)


def test_configure_logging_fallback_non_interactive():
    # Testing non-interactive shell using StringIO
    # Create a fake object to simulate a non-interactive console
    config = {"test_logging_console": StringIO()}
    opsdroid.configure_logging(config)
    rootlogger = logging.getLogger()
    assert isinstance(rootlogger.handlers[1].stream, StringIO)


def test_configure_logging_formatter(capsys):
    config = {
        "path": False,
        "console": True,
        "formatter": "%(name)s:",
    }

    opsdroid.configure_logging(config)
    captured = capsys.readouterr()

    log = "opsdroid.logging:\nopsdroid.logging:\n"

    assert log in captured.err


@pytest.fixture
def white_and_black_config():
    # Set up
    config = {
        "path": False,
        "level": "info",
        "console": True,
        "filter": {"whitelist": ["opsdroid"], "blacklist": ["opsdroid.core"]},
    }

    yield config

    # Tear down
    config = {}
    opsdroid.configure_logging(config)


def test_configure_whitelist_and_blacklist(capsys, white_and_black_config):
    opsdroid.configure_logging(white_and_black_config)
    captured = capsys.readouterr()

    log1 = "Both whitelist and blacklist filters found in configuration."
    log2 = "Only one can be used at a time - only the whitelist filter will be used."

    assert log1 in captured.err
    assert log2 in captured.err
    

report_coverage()


#########################################################################################################################################################################################


import logging
import opsdroid.opsdroid_logging as opsdroid
import pytest

# Mock the logger to test warning messages
from unittest.mock import MagicMock, patch

# Additional imports
from io import StringIO

#ParsingFilter.__init__
def test_parsing_filter_init_whitelist_and_blacklist():
    config = {"filter": {"whitelist": ["opsdroid"], "blacklist": ["opsdroid.core"]}}
    filter_obj = opsdroid.ParsingFilter(config, config["filter"])
    assert filter_obj.config == config
    assert len(filter_obj.parse_list) == 1  # Only whitelist should be used

def test_parsing_filter_init_only_whitelist():
    config = {"filter": {"whitelist": ["opsdroid"]}}
    filter_obj = opsdroid.ParsingFilter(config, config["filter"])
    assert filter_obj.config == config
    assert len(filter_obj.parse_list) == 1  # Whitelist should be used

def test_parsing_filter_init_only_blacklist():
    config = {"filter": {"blacklist": ["opsdroid"]}}
    filter_obj = opsdroid.ParsingFilter(config, config["filter"])
    assert filter_obj.config == config
    assert len(filter_obj.parse_list) == 1  # Blacklist should be used

def test_parsing_filter_init_no_filter():
    config = {}
    filter_obj = opsdroid.ParsingFilter(config, config)
    assert filter_obj.parse_list == []  # No filter should be used

#ParsingFilter.filter
def test_parsing_filter_filter_no_filter():
    config = {}
    filter_obj = opsdroid.ParsingFilter(config, config)
    record = logging.LogRecord(name="opsdroid", level=logging.INFO, pathname="", lineno=0, msg="", args=(), exc_info=None)
    assert filter_obj.filter(record)  # Should return True

def test_parsing_filter_filter_whitelist():
    config = {"filter": {"whitelist": ["opsdroid"]}}
    filter_obj = opsdroid.ParsingFilter(config, config["filter"])
    record = logging.LogRecord(name="opsdroid", level=logging.INFO, pathname="", lineno=0, msg="", args=(), exc_info=None)
    assert filter_obj.filter(record)  # Should return True

def test_parsing_filter_filter_blacklist():
    config = {"filter": {"blacklist": ["opsdroid"]}}
    filter_obj = opsdroid.ParsingFilter(config, config["filter"])
    record = logging.LogRecord(name="opsdroid", level=logging.INFO, pathname="", lineno=0, msg="", args=(), exc_info=None)
    assert not filter_obj.filter(record)  # Should return False

#set_formatter_string
def test_set_formatter_string_with_formatter():
    config = {"formatter": "%(name)s:"}
    formatter_str = opsdroid.set_formatter_string(config)
    assert formatter_str == config["formatter"]

def test_set_formatter_string_extended():
    config = {"extended": True}
    formatter_str = opsdroid.set_formatter_string(config)
    assert ".%(funcName)s():" in formatter_str

def test_set_formatter_string_timestamp():
    config = {"timestamp": True}
    formatter_str = opsdroid.set_formatter_string(config)
    assert "%(asctime)s" in formatter_str

def test_set_formatter_string_extended_and_timestamp():
    config = {"extended": True, "timestamp": True}
    formatter_str = opsdroid.set_formatter_string(config)
    assert ".%(funcName)s():" in formatter_str
    assert "%(asctime)s" in formatter_str

def test_get_logging_level_critical():
    assert opsdroid.get_logging_level("critical") == logging.CRITICAL

def test_get_logging_level_error():
    assert opsdroid.get_logging_level("error") == logging.ERROR

def test_get_logging_level_warning():
    assert opsdroid.get_logging_level("warning") == logging.WARNING

def test_get_logging_level_debug():
    assert opsdroid.get_logging_level("debug") == logging.DEBUG

def test_get_logging_level_info():
    assert opsdroid.get_logging_level("info") == logging.INFO

def test_get_logging_level_default():
    assert opsdroid.get_logging_level("") == logging.INFO

def test_get_logging_level_invalid():
    with pytest.raises(ValueError):
        opsdroid.get_logging_level("invalid_level")

