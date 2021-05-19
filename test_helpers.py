import json
import unittest
import plugins.helpers


class TestHelperMethods(unittest.TestCase):

    def test_execute_command(self):
        cmd = "ls"
        out, err = plugins.helpers.execute_command(cmd)
        self.assertTrue(out)


class TestConfigFile(unittest.TestCase):

    def test_config_file(self):
        with open("./config.json") as f:
            json.load(f)


if __name__ == '__main__':
    unittest.main()
