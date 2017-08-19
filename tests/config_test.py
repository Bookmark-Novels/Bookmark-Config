import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bookmark_config import Config

CONSUL_TOKEN = os.environ['CONSUL_TOKEN']

def test_connect_gatekeeper():
    test_config = Config('access.consul.dev.bookmark.services', CONSUL_TOKEN)
    assert test_config.get_boolean('gatekeeper', 'config', 'debug') is True

def test_key_does_not_exist():
    test_config = Config('access.consul.dev.bookmark.services', CONSUL_TOKEN)
    assert test_config.get_string('fiaejfjoijfaidfdoifd') is None

def test_root_key():
    test_config = Config('access.consul.dev.bookmark.services', CONSUL_TOKEN, root_key='gatekeeper')
    assert test_config.get_boolean('config', 'debug') is True

    test_config = Config('access.consul.dev.bookmark.services', CONSUL_TOKEN, root_key='gatekeeper/config')
    assert test_config.get_boolean('debug') is True
