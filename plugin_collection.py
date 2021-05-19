import os
import json
import inspect
import pkgutil

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'


class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.short = 'UNKNOWN'
        self.description = 'UNKNOWN'

    def perform_operation(self, argument):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError


class PluginCollection(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.reload_plugins()
        self.reload_config()

    def reload_config(self):
        with open("./config.json") as f:
            self.config = json.load(f)

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        print(f'Looking for plugins under package {self.plugin_package}')
        self.walk_package(self.plugin_package)

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=[''])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__,
                                                         imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=[''])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Plugin) & (c is not Plugin):
                        print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)

    def perform_action(self, argument):
        """Perform action from all the plgins
        """
        print()
        print('Performing action on all plugins')
        for plugin in self.plugins:
            print("*"*80)
            if plugin.__class__.__name__ not in self.config:
                print(f'    Plugin {plugin.__class__.__name__} is not configured and will not run')
                continue
            plugin_config = self.config[plugin.__class__.__name__]
            if not plugin_config["active"]:
                print(f'    Plugin {plugin.__class__.__name__} is disabled')
                continue

            print(f'Running {plugin.short}')
            if plugin.perform_operation(plugin_config["additional_input"]):
                print(f'    {OKGREEN}{plugin.description} - OK {ENDC}')
            else:
                if plugin_config["allow_failure"]:
                    print(f'    {WARNING}{plugin.description} - FAILED -OK {ENDC}')
                else:
                    print(f'    {FAIL}{plugin.description} - FAILED {ENDC}')
