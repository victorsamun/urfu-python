#!/usr/bin/env python3

import os
import signal


'''
def handle_sigchld(signum, stack):
    print("Got SIGCHLD:", signum, stack)
    got_child = True
    while got_child:
        try:
            got_child = os.waitpid(0, os.WNOHANG)
        except ChildProcessError:
            got_child = False


signal.signal(signal.SIGCHLD, handle_sigchld)
'''


pid = os.fork()
if pid:
    # Parent
    input()
else:
    # Child
    pass
