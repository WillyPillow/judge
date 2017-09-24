import subprocess

from dmoj.executors.base_executor import ScriptExecutor
import os

if os.name != 'nt':
    from dmoj.cptbox.handlers import ACCESS_DENIED


def do_write(debugger):
    if debugger.arg0 <= 2:
        return True
    # TCL doesn't seem to care if anything past 2 fails
    return ACCESS_DENIED(debugger)


class Executor(ScriptExecutor):
    ext = '.tcl'
    name = 'TCL'
    nproc = -1  # TCL uses a bunch of threads internally
    address_grace = 131072
    command = 'tclsh'
    syscalls = ['connect', 'access', 'getsockname', 'select',
                # TCL uses some handles internally
                ('write', do_write)]
    fs = [r'/etc/nsswitch\.conf$', '/etc/passwd$']
    test_program = '''\
gets stdin input
puts $input
'''

    @classmethod
    def get_runtime_versions(cls):
        # TCL is dangerous to fetch versions for, since some TCL versions ignore the --version flag and instead go
        # straight into the interpreter. Since version processes are ran without time limit, this is pretty bad since
        # it can hang the startup process. TCL versions without --version can't be reliably detected either, since
        # they also don't have --help.
        # Here, we just use subprocess to print the TCL version, and use that.
        process = subprocess.Popen([cls.get_command()], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        process.stdin.write('puts $tcl_version\n')
        process.stdin.close()
        retcode = process.poll()
        return ('tclsh', tuple(map(int, process.stdout.read().split('.'))) if not retcode else ()),

