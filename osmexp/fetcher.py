import itertools
from http import HTTPStatus

import requests
from shapely import get_parts, polygonize_full
from shapely.geometry import GeometryCollection, LineString, Point, Polygon

API_URL = 'https://www.openstreetmap.org/api/0.6'


def parse_nodes_ways(elements: list[dict]) -> tuple[list[dict], list[dict]]:
    nodes = {e['id']: Point(e['lon'], e['lat']) for e in elements if e['type'] == 'node'}
    ways = [LineString([nodes[n] for n in e['nodes']]) for e in elements if e['type'] == 'way']
    return list(nodes.values()), ways


def fetch_node(node_id: int) -> Point | None:
    response = requests.get(f'{API_URL}/node/{node_id}.json')
    if response.status_code != HTTPStatus.OK:
        return None
    return parse_nodes_ways(response.json()['elements'])[0][0]


def fetch_way(way_id: int) -> LineString | Polygon | None:
    response = requests.get(f'{API_URL}/way/{way_id}/full.json')
    if response.status_code != HTTPStatus.OK:
        return None
    _, ways = parse_nodes_ways(response.json()['elements'])
    way = ways[0]
    return Polygon(way) if way.is_closed and way.is_ring else way


def fetch_relation(relation_id: int) -> GeometryCollection | None:
    response = requests.get(f'{API_URL}/relation/{relation_id}/full.json')
    if response.status_code != HTTPStatus.OK:
        return None
    _, ways = parse_nodes_ways(response.json()['elements'])
    cases = [get_parts(p) for p in polygonize_full(ways) if p]
    parts = list(itertools.chain(*cases))
    return GeometryCollection(parts)
