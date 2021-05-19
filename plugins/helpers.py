import re
import subprocess


def execute_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    return output.decode("utf-8"), err.decode("utf-8")


def find_files_with_bad_permissions(criteria, excepts=[]):
    # arguments:
    #       criteria    additional options for the find command
    #       excepts     exceptions to ignore with the test cases. '*' at the end means
    #                   to ignore everything which contains the specified string
    #                   in its path.
    exceptions = [e.replace('*', '.*') for e in excepts]
    command = "sudo find / %s -print 2> /dev/null" % (criteria)
    output, err = execute_command(command)
    hitList = finalList = list([_f for _f in output.splitlines() if _f])

    for hit in hitList:
        for exception in exceptions:
            if re.match(exception, hit):
                finalList.remove(hit)
                break

    return finalList
