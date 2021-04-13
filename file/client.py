# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import uuid
from datetime import datetime
from idmefv2 import Message
from idmefv2_transport import get_transport
from args import parse_args


def main(args):
    print("READY", flush=True)

    now = datetime.now().isoformat('T')
    msg = Message()
    msg['Version'] = '0.1'
    msg['ID'] = str(uuid.uuid4())
    msg['CreateTime'] = now
    msg['DetectTime'] = now
    msg['CategoryRef'] = 'ENISA'
    msg['Category'] = []
    msg['Description'] = 'Someone tried to login as root from 12.34.56.78 '\
                         'port 1806 using the password method'
    msg['Severity'] = 'medium'
    msg['Ref'] = []
    msg['Agent'] = {
        'Name': 'prelude-lml',
        'ID': str(uuid.uuid4()),
        'Category': ['LOG'],
        'IP4': '127.0.0.1',
        'IP6': '::1',
    }
    msg['Source'] = []
    msg['Target'] = []

    transport = get_transport('file://%s' % args.tmpdir, content_type=args.mime)
    transport.start()
    transport.send_message(msg)
    transport.stop()


if __name__ == '__main__':
    args = parse_args("client")
    main(args)
