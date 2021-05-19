import re
import sys
import logging
from plugin_collection import Plugin
sys.path.append('./plugins')
import helpers    # noqa: E402

log = logging.getLogger(__name__)


class CapabilityTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 'capability test'
        self.description = '''Check if non-root process has any additional capabilities'''

    def perform_operation(self, argument):
        ret = True
        log.info('    Checking capabilities')
        command = "ps -N -u root | tail -n +2"
        out, err = helpers.execute_command(command)

        nonroot_process_data = {}
        for line in out.split('\n'):
            if line:
                pid, _, _, pname = line.split()
                nonroot_process_data[pid] = pname

        pattern = re.compile("^Capabilities for `(\\d+)': = (.*)")
        command = "getpcaps " + ' '.join(list(nonroot_process_data))
        out, err = helpers.execute_command(command)
        for line in err.split('\n'):
            m = pattern.match(line)
            if m:
                log.warn("    {0:20} = {1}".format(nonroot_process_data[m.group(1)], m.group(2)))
                ret = False

        return ret
