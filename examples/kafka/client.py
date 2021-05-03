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
    msg['Version'] = '2.0.3'
    msg['ID'] = str(uuid.uuid4())
    msg['CreateTime'] = now
    msg['StartTime'] = now
    msg['Category'] = ['Attempt.Login']
    msg['Description'] = 'Someone tried to login as root from 12.34.56.78 '\
                         'port 1806 using the password method'
    msg['Severity'] = 'Medium'
    msg['Analyzer'] = {
        'IP': '127.0.0.1',
        'Name': 'prelude-lml',
        'Model': 'My Log Analyzer v0.0.1',
        'Category': ['LOG'],
        'Data': ['Log'],
        'Method': ['Signature'],
    }
    msg['Source'] = [
        {
            'IP': '12.34.56.78',
            'Port': [1806],
        }
    ]
    msg['Target'] = [
        {
            'IP': '23.34.45.56',
            'Port': [22],
            'Service': 'sshd',
        }
    ]

    transport = get_transport('kafka://%s/' % args.address, content_type=args.mime)
    transport.set_parameter('producer_topic', 'idmefv2-example-topic')
    transport.start()
    transport.send_message(msg)
    transport.stop()


if __name__ == '__main__':
    args = parse_args("client")
    main(args)
