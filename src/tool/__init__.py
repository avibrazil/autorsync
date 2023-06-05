#!/usr/bin/env python

# Used only when testing locally
# import sys
# sys.path.insert(0,'..')

import argparse
import pathlib
import logging
import autorsync

def prepare_logging(level=logging.INFO):
    # Switch between INFO/DEBUG while running in production/developping:

    # Configure logging

    FORMATTER = logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s")
    HANDLER = logging.StreamHandler()
    HANDLER.setFormatter(FORMATTER)

    loggers=[
        logging.getLogger('__main__'),
        logging.getLogger('autorsync'),
    ]

    for logger in loggers:
        logger.addHandler(HANDLER)
        logger.setLevel(level)

    return loggers[0]



def prepare_args():
    parser = argparse.ArgumentParser(
        prog='autosync',
        description='Sync pre-configured folders with rsync'
    )

    parser.add_argument(
        '-c', '--config-file',
        dest='config_file',
        required=False,
        default=pathlib.Path.home() / 'autorsync.yaml',
        help='Path to config file'
    )

    parser.add_argument(
        '-p', '--profiles',
        dest='profiles',
        required=False,
        default=None,
        help='Comma-separated list of profiles to execute'
    )

    parser.add_argument(
        '-l', '--list',
        dest='list',
        action=argparse.BooleanOptionalAction,
        required=False,
        default=False,
        help='List profiles and details without executing them'
    )

    parser.add_argument(
        '-n', '--dry-run',
        dest='simulate',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Force simulation only, regardless of what is defined in the profile'
    )

    parser.add_argument(
        '-d', '--debug',
        dest='debug',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Be more verbose and output messages to console.'
    )

    return parser.parse_args()





def main():
    # Read environment and command line parameters
    args=prepare_args()

    # Setup logging
    global logger
    if args.debug:
        logger=prepare_logging(logging.DEBUG)
    else:
        logger=prepare_logging()


    profiles=autorsync.RSyncProfiles(args.config_file)


    if args.list:
        print(profiles)
    else:
        profiles.run(args.profiles,simulate=args.simulate)


if __name__ == "__main__":
    main()
