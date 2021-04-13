#!/usr/bin/python3
# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import asyncio
import locale
import shlex
import subprocess
import sys
import time

from asyncio.subprocess import PIPE, DEVNULL, STDOUT
from contextlib import closing


@asyncio.coroutine
def main(transport):
    cmd = [
        sys.executable,
        "-Walways::ResourceWarning",
        "-Walways::RuntimeWarning",
        "examples/%s/server.py" % transport
    ]

    print("Testing transport '%s' ..." % transport)
    print("  Running:", *[shlex.quote(arg) for arg in cmd])
    promise = asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=STDOUT, stdin=DEVNULL)
    server = yield from promise

    read_cmd = False
    while True:
        try:
            line = yield from asyncio.wait_for(server.stdout.readline(), 10.)
        except asyncio.TimeoutError:
            line = None
        if not line:
            print("  Server exited during prolog")
            return 1
        line = line.decode(locale.getpreferredencoding(False)).rstrip('\r\n')
        print("    [server]", line, flush=True)
        if read_cmd:
            client_cmd = shlex.split(line)
            break
        elif line.startswith('READY'):
            read_cmd = True

    print("  Running:", *[shlex.quote(arg) for arg in client_cmd])
    client = subprocess.Popen(client_cmd,
                              encoding="utf-8", errors="replace",
                              stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)

    try:
        stdout, dummy_ = client.communicate(timeout=60.)
    except subprocess.TimeoutExpired:
        client.terminate()
        server.terminate()
        time.sleep(2)
        client.kill()
        server.kill()
        print("  Client timeout")
        return 1

    for line in stdout.splitlines():
        print("    [client]", line)

    if client.returncode != 0:
        print("  Error in client (%d)" % client.returncode)

    try:
        yield from asyncio.wait_for(server.wait(), 10.)
    except asyncio.TimeoutError:
        server.terminate()
        time.sleep(2)
        server.kill()

    stdout, dummy_ = yield from asyncio.wait_for(server.communicate(), 10.)
    for line in stdout.decode(locale.getpreferredencoding(False)).splitlines():
        print("    [server]", line)

    if server.returncode != 0:
        print("  Error in server (%d)" % server.returncode)

    res = max(client.returncode, server.returncode)
    if not res:
        print("  Done")
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("transport", type=str, help="Transport to test")
    args = parser.parse_args()

    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    asyncio.get_child_watcher()
    with closing(loop):
        sys.exit(loop.run_until_complete(main(args.transport)))
