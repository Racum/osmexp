#!/usr/bin/env python

import argparse
import sys

from .geojson import ExportError, export_node, export_relation, export_way

EXPORTERS = {
    'node': export_node,
    'way': export_way,
    'rel': export_relation,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='osmexp',
        description='Export an OpenStreetMap element as GeoJSON to STDOUT.',
    )
    parser.add_argument('element', choices=EXPORTERS, help='The OSM element type.')
    parser.add_argument('id', type=int, help='The OSM element ID (an integer).')
    args = parser.parse_args()

    try:
        print(EXPORTERS[args.element](args.id))
    except ExportError as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
