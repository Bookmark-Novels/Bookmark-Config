import json

from consul import Consul

__all__ = ['AlreadyInitializedError', 'Config']

class AlreadyInitializedError(Exception):
    """Thrown in the event that the user tries to load the config again.
    """
    pass

class Config(object):
    """A class for fetching configuration values from Consul.
    Overrides may be specified in the form of a JSON file path.
    """
    def __init__(self, consul_host, port=80):
        """Constructor for a Config object.

        Args:
            consul_host (required): The host for the Consul KV store.
            port (default=80): The port to use when connecting to Consul.
        """
        self.consul = Consul(host=consul_host, port=port)
        self.config = None

    def load(self, root_key='', override_file=None):
        """Initializes the Config object. This method should only
        be called once per Config. Empty key folders will be ignored during
        the loading process.

        Args:
            root_key (default=''): A string specifying the root key prefix
                                   to use when reading from Consul. By default,
                                   everything will be loaded unless this is specified.
            override_file (default=None): A string path specifying a JSON override
                                          file to load. This file can be used to
                                          override shared configuration values for
                                          development purposes. If this is None then
                                          no override will be loaded.
        Raises:
            AlreadyInitializedError: This is raised in the event that a user tries
                                     to load the Config object more than once.
        """
        if self.config is not None:
            raise AlreadyInitializedError('This Config is already initialized.')

        index, data = self.consul.kv.get(root_key, recurse=True)

        self.config = {}

        for item in data:
            if item['Value'] is None:
                continue

            self.config[item['Key']] = item['Value'].decode('utf-8')

        if override_file is None:
            return

        with open(override_file) as f:
            lines = f.readlines()
            override_data = json.loads(''.join(lines))
            override_data = __flatten__(override_data)
            self.config.update(override_data)

    def getString(self, *args):
        """Returns a configuration string given a variadic list of key paths.

        Returns:
            A string value for the given key. None is returned if the key does
            not exist.
        """
        return self.config.get(__format_key__(args))

    def getInteger(self, *args):
        """Returns a configuration integer given a variadic list of key paths.

        Returns:
            An integer value for the given key. None is returned if the key does
            not exist.
        Raises:
            ValueError: Raised in the event that the specified key is not an integer.
        """
        value = self.getString(*args)

        if value is None:
            return None

        return int(value)

    def getFloat(self, *args):
        """Returns a configuration float given a variadic list of key paths.

        Returns:
            An float value for the given key. None is returned if the key does
            not exist.
        Raises:
            ValueError: Raised in the event that the specified key is not a float.
        """
        value = self.getString(*args)

        if value is None:
            return None

        return float(value)

    def getBoolean(self, *args):
        """Returns a configuration integer given a variadic list of key paths.

        Booleans are defined to be either "true" or "false" in either uppercase,
        lowercase, or mixed-case.

        Returns:
            An boolean value for the given key. None is returned if the key does
            not exist.
        Raises:
            ValueError: Raised in the event that the specified key is not a boolean.
        """
        value = self.getString(*args)

        if value is None:
            return None

        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise ValueError(
                'Unable to parse boolean from string value: {}. Valid values are true and false.'.format(value)
            )

    def __str__(self):
        return json.dumps(self.config)

def __flatten__(json_dict):
    flattened_dict = {}

    def flatten(key, val):
        if isinstance(val, dict):
            for k, v in val.items():
                new_key = k if key is None else '{}.{}'.format(key, k)
                flatten(new_key, v)
        else:
            flattened_dict[key] = val

    flatten(None, json_dict)

    return flattened_dict

def __format_key__(key_parts):
    return '/'.join(key_parts)
