#!/usr/bin/env python3

import sys
import argparse
import os


from .geojson import export_node, export_relation, export_way

HELP = """
Usage: osmexp [element] [id]

Arguments:
    element: The OSM element type, options: "rel", "way" or "node".
    id:      The OSM element ID: an integer number.

Output: A GeoJSON representation of the element.
"""

def main():
    parser = argparse.ArgumentParser(description='Export OpenStreetMap data to GeoJSON', epilog='Output: A GeoJSON representation of the element.')
    parser.add_argument('element', help='The OSM element type, options: "rel", "way" or "node".')
    parser.add_argument('id', help='The OSM element ID: an integer number.')
    parser.add_argument('--dir', help='Write output to DIR/$featurename.json')
    args = parser.parse_args()
    
    if not args.element and args.id :
        print(HELP, file=sys.stderr)
        sys.exit()

    if args.element not in ['rel', 'way', 'node']:
        print('Unknown element type, please use "rel", "way" or "node".', file=sys.stderr)
        sys.exit()

    if not args.id.isdigit():
        print('Element ID should be an integer.', file=sys.stderr)
        sys.exit()

    element_type = args.element.lower()
    element_id = args.id
    output: str
    match element_type:
        case 'node':
            output = export_node(element_id)
        case 'way':
            output = export_way(element_id)
        case 'rel':
            output = export_relation(element_id)
    if not args.dir :
        print(output[0])
    else :
        f = open(os.path.join(args.dir, f'{output[1]}.json'), 'w')
        f.write(output[0])
        f.write('\n')
        f.close()

if __name__ == '__main__':
    main()
