#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import base64


def main():

    # Load this source file and strip the header.
    initial_data = open(sys.argv[1], 'rt').read()

    encoded_data = base64.b64encode(initial_data)

    print("url(data:image/png;base64," + encoded_data + ");")


if __name__ == '__main__':
    main()
