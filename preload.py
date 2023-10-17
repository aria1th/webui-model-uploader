import os

def preload(parser):
    parser.add_argument(
        "--basic-auth-file",
        help="config file to load / save, if not specified, behavior depends on --api-aux-auth or --api-auth",
        default=None
    )

    # api-aux-auth is a comma separated list of user:password
    parser.add_argument(
        "--api-aux-auth",
        help="comma separated list of user:password for auxiliary authentication",
        default=None
    )