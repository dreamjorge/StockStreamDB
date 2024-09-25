import pytest
from unittest.mock import patch
import sys

# Simulate the 'create' command
def test_cli_create():
    test_args = [
        "cli.py", "create", 
        "AAPL", "Apple Inc.", 
        "Technology", "Consumer Electronics", 
        "150", "2023-09-01"
    ]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main
        main()

# Simulate the 'get' command
def test_cli_get():
    test_args = ["cli.py", "get", "AAPL"]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main
        main()

# Simulate the 'update' command
def test_cli_update():
    test_args = [
        "cli.py", "update", 
        "AAPL", "Apple Corporation", 
        "Technology", "Consumer Electronics", 
        "160", "2023-10-01"
    ]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main
        main()

# Simulate the 'delete' command
def test_cli_delete():
    test_args = ["cli.py", "delete", "AAPL"]
    with patch.object(sys, 'argv', test_args):
        from src.interfaces.cli.cli import main
        main()
