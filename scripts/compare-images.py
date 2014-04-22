#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import sys

from more_itertools import grouper
from phash import cross_correlation, image_digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar="IMAGE_FILE", nargs="+")
    parser.add_argument('--threshold', type=float, default=0.90)
    args = parser.parse_args()

    if len(args.files) % 2 != 0:
        parser.error("Files must be provided in pairs")

    failures = 0

    # TODO: don't punt on media type detection:
    for img_1, img_2 in grouper(2, args.files):
        digest_1 = image_digest(img_1)
        digest_2 = image_digest(img_2)

        pcc = cross_correlation(digest_1, digest_2)

        if pcc >= args.threshold:
            status = 'pass'
            log_f = sys.stdout
        else:
            status = 'FAIL'
            log_f = sys.stderr
            failures += 1

        print('%s\t%s\t%s\t%0.3f' % (status, img_1, img_2, pcc), file=log_f)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
