#!/usr/bin/env python3

# Libraries
##############################################################################
import socket
import ssl
import warnings
from argparse import ArgumentParser
##############################################################################

# Disable Deprecation Warning
##############################################################################
warnings.filterwarnings("ignore", category=DeprecationWarning)
##############################################################################

# Global Values
##############################################################################
PROTOCOLS = {
    ssl.TLSVersion.SSLv3:"SSL v3 [Insecure]",
    ssl.TLSVersion.TLSv1:"TLS 1.0 [Insecure]",
    ssl.TLSVersion.TLSv1_1:"TLS 1.1 [Insecure]",
    ssl.TLSVersion.TLSv1_2:"TLS 1.2",
    ssl.TLSVersion.TLSv1_3:"TLS 1.3"
}
DESCRIPTION = "The program that allows you detect SSL Protocol Versions"
##############################################################################

# Main
##############################################################################
if __name__ == '__main__':
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "-hn",
        "--hostname", 
        type=str, 
        help="Hostname", 
        required=True
    )
    parser.add_argument(
        "-p",
        "--port", 
        type=str, 
        help="Port number", 
        required=False
    )
    args = parser.parse_args()

    host = args.hostname # Get hostname from input
    
    if args.port:
        port = args.port
    else:
        port = 443

    for k,v in PROTOCOLS.items():
        ctx = ssl.create_default_context()
        ctx.minimum_version = k
        ctx.maximum_version = k
        ctx.check_hostname  = False
        ctx.verify_mode     = ssl.CERT_NONE

        try:
            with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                s.connect((host, port))
                print("Connected with",v)
        except:
            print("Not connected with",v)
##############################################################################