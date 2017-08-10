import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bookmark_config import Config

def test_connect_gatekeeper():
    test_config = Config('gatekeeper.consul.dev.bookmark.services')
    test_config.load()

    assert test_config.getBoolean('gatekeeper', 'config', 'debug') is True
