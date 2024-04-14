#!/usr/bin/env python

import sys

from .geojson import export_node, export_relation, export_way

HELP = """
Usage: osmexp [element] [id]

Arguments:
    element: The OSM element type, options: "rel", "way" or "node".
    id:      The OSM element ID: an integer number.

Output: A GeoJSON representation of the element.
"""

def main():

    if len(sys.argv) != 3 or (len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']):
        print(HELP)
        sys.exit()

    if sys.argv[1].lower() not in ['rel', 'way', 'node']:
        print('Unknown element type, please use "rel", "way" or "node".')
        sys.exit()

    if not sys.argv[2].isdigit():
        print('Element ID should be an integer.')
        sys.exit()

    element_type = sys.argv[1].lower()
    element_id = sys.argv[2]

    match element_type:
        case 'node':
            print(export_node(element_id))
        case 'way':
            print(export_way(element_id))
        case 'rel':
            print(export_relation(element_id))


if __name__ == '__main__':
    main()