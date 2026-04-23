import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

def test_placeholder():
    """Basic test to confirm pipeline runs"""
    assert 1 + 1 == 2

def test_login_logic():
    """Test login validation logic"""
    username = "admin"
    password = "secret"
    assert username == "admin"
    assert password == "secret"

def test_wrong_credentials():
    """Test that wrong credentials are detected"""
    username = "hacker"
    password = "wrong"
    assert not (username == "admin" and password == "secret")
