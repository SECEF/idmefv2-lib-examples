# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import pathlib

def parse_args(prog):
    parser = argparse.ArgumentParser(description="Start the demo %s" % prog)
    parser.add_argument("--tmpdir", type=pathlib.Path, help="Temporary directory to use")
    parser.add_argument("--address", default="127.0.0.1:0",
                        help="address:port to use (defaults to 127.0.0.1 and a random port)")
    parser.add_argument("--mime", help="MIME content type to use during serialization")
    return parser.parse_args()
