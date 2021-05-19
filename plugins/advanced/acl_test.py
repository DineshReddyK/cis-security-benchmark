import re
import sys
from plugin_collection import Plugin
sys.path.append('./plugins')
import helpers    # noqa: E402


class ACLTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 'ACL test'
        self.description = '''Check if others have access(through ACL) to root owned files '''
        self.userre = re.compile("^user:(.+):.w.")
        self.groupre = re.compile("^group:(.+):.w.")
        self.filere = re.compile("^# file: (.+)")
        self.effective = re.compile("#effective:.w.")
        self.data = {}

    def set_basedon_effective_perms(self, filename, line):
        if "effective" in line:
            if self.effective.search(line):
                # non-root user has write access
                self.data[filename] = self.data[filename] + line.strip() + ","
        else:
            # non-root user has write access
            self.data[filename] = self.data[filename] + line.strip() + ","

    def perform_operation(self, argument):
        ret = True
        command = "find ./ -user 0 | xargs getfacl --skip-base > /tmp/unwanted_acls"
        out, err = helpers.execute_command(command)
        for line in open("/tmp/unwanted_acls", "r"):
            f = self.filere.match(line)
            if f:
                filename = "/" + f.group(1)
                self.data[filename] = ""
            else:
                u = self.userre.match(line)
                if u:
                    if u.group(1) != "root":
                        self.set_basedon_effective_perms(filename, line)
                else:
                    g = self.groupre.match(line)
                    if g:
                        if g.group(1) != "root":
                            self.set_basedon_effective_perms(filename, line)

        for key, val in self.data.items():
            if val:
                command = 'ls -ld %s | awk \'{print $1"|"$3":"$4}\'' % key
                out, err = helpers.execute_command(command)
                if out:
                    print("%s|%s|%s" % (key, out.strip(), val))

        return ret
