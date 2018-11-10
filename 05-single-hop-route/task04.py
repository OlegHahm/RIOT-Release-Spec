#! /usr/bin/env python3
import sys
import os
import argparse
sys.path.append("../testutils")

from iotlab import IoTLABNode, IoTLABExperiment  # noqa: E402
from common import SingleHopNode, single_hop_run, print_results  # noqa: E402

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('riotbase', nargs='?',
                   help='Location of RIOT folder')
    args = p.parse_args()
    riotbase = args.riotbase

    if not riotbase:
        p.print_help()
        sys.exit(1)

    os.chdir(os.path.join(riotbase, "tests/gnrc_udp"))

    # Create IoTLAB experiment (TODO: Return addresses)
    exp = IoTLABExperiment("RIOT-release-test-05-04",
                           [IoTLABNode(extra_modules=["gnrc_pktbuf_cmd"]),
                            IoTLABNode(extra_modules=["gnrc_pktbuf_cmd"])])

    N = 10

    try:
        addr = exp.nodes_addresses
        iotlab_cmd = "make IOTLAB_NODE={} BOARD=iotlab-m3 term"
        source = SingleHopNode(iotlab_cmd.format(addr[0]))
        dest = SingleHopNode(iotlab_cmd.format(addr[1]))
        results = []

        ip_src = None
        ip_dest = "beef::1/64"
        src_route = "::"
        dest_route = "::"
        disable_rdv = True
        count = 10
        tolerance = 1

        for i in range(N):
            source.reboot()
            dest.reboot()

            packet_loss, buf_source, buf_dest = single_hop_run(
                    source, dest, ip_src, ip_dest, src_route,
                    dest_route, disable_rdv, count)
            results.append([packet_loss, buf_source, buf_dest])

            assert(packet_loss < tolerance)
            assert(buf_source)
            assert(buf_dest)
            print("OK")
        print_results(results)
    except Exception as e:
        print(str(e))
        print("Test failed!")
    finally:
        exp.stop()