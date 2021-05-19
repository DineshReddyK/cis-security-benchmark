import os
import sys
import logging
from plugin_collection import Plugin
sys.path.append('./plugins')
import helpers    # noqa: E402

log = logging.getLogger(__name__)


class EtcFileTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = '/etc files perm test'
        self.description = '''Check permissions of /etc/{passwd,group,shadow,fstab,inittab,hosts,service} '''

    def perform_operation(self, argument):
        ret = True
        # default etc file test
        root_etc_files = ['/etc/passwd',
                          '/etc/group',
                          '/etc/shadow',
                          '/etc/fstab',
                          '/etc/inittab',
                          '/etc/hosts',
                          '/etc/service']
        log.info("etc file permission test running...")
        for f in root_etc_files:
            try:
                s = os.stat(f)
                if s.st_uid != 0 or s.st_gid != 0:
                    log.warn(f'    {f} is not owned by root:root')
                    ret = False

                mode = oct(s.st_mode)[-3:]
                if f == '/etc/shadow':
                    if mode != '640' and mode != '600' and mode != '000':
                        log.warn(f'   {f} has excess permissions -> {mode}')
                        ret = False
                elif mode != '644':
                    log.warn(f'    {f} dont have permission 644')
                    ret = False
            except Exception as e:
                log.warn(f'    Could not check - {f}. {e}')
        return ret


class WritableTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 'write permissions test'
        self.description = '''Check if world or group writable files or directories exist'''

    def world_writable_files_dirs(self):
        log.info('    Checking world writable files/directories')
        findCriteria = "-xdev -perm /002 ! type l"
        offendingFiles = helpers.find_files_with_bad_permissions(findCriteria, excepts=[])
        if offendingFiles:
            log.warn(f'    Offending files/directories : {offendingFiles}')
            return False
        return True

    def group_writable_files_root_user(self):
        log.info('    Checking group writable files/directories owned by root')
        findCriteria = "-xdev -user 0 ! -group 0 -perm /020"
        offendingFiles = helpers.find_files_with_bad_permissions(findCriteria, excepts=[])
        if offendingFiles:
            log.warn(f'    Offending files/directories : {offendingFiles}')
            return False
        return True

    def perform_operation(self, argument):
        test1 = self.world_writable_files_dirs()
        test2 = self.group_writable_files_root_user()
        return test1 and test2


class OrphanTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 'Orphaned test'
        self.description = '''Check if orphaned files or directories exist'''

    def perform_operation(self, argument):
        log.info('    Checking orphaned files/dirs')
        findCriteria = "\\( -nouser -o -nogroup \\)"
        offendingFiles = helpers.find_files_with_bad_permissions(findCriteria, excepts=[])
        if offendingFiles:
            log.warn(f'    Offending files/directories : {offendingFiles}')
            return False
        return True


class SbitTest(Plugin):
    def __init__(self):
        super().__init__()
        self.short = 's-bit test'
        self.description = 'Check if s-uid or s-gid files exist'

    def perform_operation(self, argument):
        log.info('    Checking suid/sgid files')
        findCriteria = "\\( -perm -4000 -o -perm -2000 \\) -type f"
        offendingFiles = helpers.find_files_with_bad_permissions(findCriteria, excepts=[])
        if offendingFiles:
            log.warn(f'    Offending files/directories : {offendingFiles}')
            return False
        return True
