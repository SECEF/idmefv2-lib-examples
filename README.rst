IDMEFv2 examples
################

This repository contains a few examples of IDMEFv2 clients and servers based on the
`IDMEFv2 modelization library <https://github.com/SECEF/idmefv2-lib-model>` and
`IDMEFv2 transport library <https://github.com/SECEF/idmefv2-lib-transport>`.

It is part of the `SECEF <https://www.secef.net/>` project and serves both as
an illustration of the libraries' usage and as unit and integration tests
for the libraries.

You can find more information about the previous version (v1) of the
Intrusion Detection Message Exchange Format in
`RFC 4765 <https://tools.ietf.org/html/rfc4765>`.

You can also visit https://www.secef.net/ for more information about
IDMEFv2's status and development progress.

Installation
============

The following prerequisites must be installed on your system in order to use
the examples contained in this repository:
* The ``make`` command (usually available from the system package named ``make``)
* Python 3.6 or later
* The Python `idmef <https://github.com/SECEF/idmefv2-lib-model>` package
* The Python `idmeftransport <https://github.com/SECEF/idmefv2-lib-transport>`
  package
* A working (local) Kafka installation (only required if you want to try
  the Kafka transport implementation). It is expected that the Kafka server
  is using the default configuration (no ACLs, default network ports, automatic
  topic creation/configuration, etc.)

Usage
=====

The simplest way to run the examples in this repository is to run the ``make``
command with no arguments:

..  sourcecode:: sh

    make

For each available transport implementation, the command will:
* Start a server for the given transport
* Wait until the server is fully initialized
* Spawn a client that sends an IDMEFv2 message using that transport
* Make sure that the IDMEFv2 message was properly received by the server

Alternatively, you can pass the name of a specific transport implementation
(in lowercase) to only run the example associated with the given transport, e.g.

..  sourcecode:: sh

    make http

Contributions
=============

All contributions must be licensed under the BSD 2-clause license.
See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask
that new contributors subscribe to the `SECEF mailing list
<https://www.freelists.org/list/secef>` as a way to introduce themselves.
