# System Benchmarking Test Runner

Implementing GIM idea - [2020-12312](https://gim.net.nokia.com/servlet/hype/IMT?documentTableId=6414346273185627169&userAction=Browse&templateName=&documentId=9f22964de54ba0c5b869b9404d5e8978)


This contains set of benchmarking tests that can be run verify the system against known issues.\
Intention of this project is to automate [CIS](https://www.cisecurity.org/cis-benchmarks/) benchmarking tests.


# Usage

TODO

# Extension

This is plugin based architecture.
One can add their own tests as a plugin. Main program runs all the plugins it found.

To add new plugin, it has to inherit base calss `Plugin`.\
It shuld also impliment `__init__` and `perform_operation` methods.

Base class:
```python
class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.short = 'UNKNOWN'
        self.description = 'UNKNOWN'

    def perform_operation(self, argument):
        """This is the method that the framework will call
        from all the plugins it found
        """
        raise NotImplementedError
```

New plugin should do:

```python
class SomeSimpleTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 'short description'
        self.description = '''Some details description'''

    def perform_operation(self, argument):
        ret = True
        #do some tests
        return ret
```

# Configuration

Test customizations can be done using the `config.json` file, like disabling the test, giving additional inputs to the tests etc.

Default format:

```json
   "TestClassName":{
      "active":true,
      "allow_failure":false,
      "type":"basic",
      "description":"Some test",
      "additional_input":{
            "anything that should be parsed by plugin"
      }
   }
```
`TestClassName` here is the class name that is implemented by the plugin

`active`: If set to `false` test is not run\
`allow_failure`: If set to `true`, test failure is ignored\
`type`: Optional field to indicate the test type\
`description`: Optional field to describe the test\
`additional_input`: Optional field to supply additional inputs to the test like some exceptions to be considered while testing
