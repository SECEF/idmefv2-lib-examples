# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import sys
import tempfile

from args import parse_args
from idmeftransport import get_transport
from os.path import dirname, join
from queue import Queue, Empty


def main(args):
    print("READY - You may now start the client like so:", flush=True)
    print("\t", sys.executable, join(dirname(__file__), "client.py"), *sys.argv[1:], "--tmpdir", str(args.tmpdir), flush=True)

    queue = Queue()
    transport = get_transport('file://%s' % args.tmpdir, queue, args.mime)
    transport.set_parameter("interval", 1)
    transport.start()
    try:
        message = queue.get(timeout=30)
    except Empty:
        print("No message received", file=sys.stderr)
        sys.exit(1)
    else:
        print("OK:", message)
        queue.task_done()
    finally:
        transport.stop()
    queue.join()


if __name__ == '__main__':
    args = parse_args("server")
    if args.tmpdir is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            args.tmpdir = tmpdir
            main(args)
    else:
        main(args)
