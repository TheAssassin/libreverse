import os
import sys
from argparse import ArgumentParser

from flask_frozen import Freezer
from .app_factory import create_app


def main():
    parser = ArgumentParser("libreverse")
    subparsers = parser.add_subparsers()

    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("models_dir")
    freeze_parser.add_argument("out_dir", nargs="?")

    args = parser.parse_args()

    app_config = {}

    if "models_dir" in args:
        app_config["MODELS_DIR"] = args.models_dir

        if "out_dir" in args and args.out_dir:
            app_config["FREEZER_DESTINATION"] = os.path.abspath(args.out_dir)

        app = create_app(app_config)

        freezer = Freezer(app)

        freezer.freeze()
        return 0

    else:
        parser.print_usage()
        return 1


sys.exit(main())
