#!/usr/bin/env python3
"""Main applicatoin that demonstrates the functionality of
the dynamic plugins and the PluginCollection class
"""

import logging
import logging.config
from plugin_collection import PluginCollection


def main():
    """main function that runs the application
    """
    logging.basicConfig(filename='result.log', level=logging.DEBUG)
    my_plugins = PluginCollection('plugins')
    my_plugins.perform_action(5)


if __name__ == '__main__':
    main()
