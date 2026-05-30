import itertools

import requests
from shapely import get_parts, polygonize_full
from shapely.geometry import GeometryCollection, LineString, Point, Polygon

API_URL = 'https://api.openstreetmap.org/api/0.6'
USER_AGENT = 'osmexp/0.2.0 (+https://github.com/racum/osmexp)'
TIMEOUT = 30
MIN_LINESTRING_NODES = 2


def fetch_elements(path: str) -> list[dict] | None:
    "Fetches an OSM API endpoint and returns its `elements`, or `None` on any failure."
    try:
        response = requests.get(
            f'{API_URL}/{path}',
            headers={'User-Agent': USER_AGENT},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        elements = response.json().get('elements')
    except (requests.RequestException, ValueError):
        return None
    return elements or None


def parse_geometries(elements: list[dict]) -> tuple[dict[int, Point], dict[int, LineString]]:
    "Builds Shapely geometries keyed by OSM id: nodes as `Point`, ways as `LineString`."
    nodes = {e['id']: Point(e['lon'], e['lat']) for e in elements if e['type'] == 'node'}
    ways = {
        e['id']: LineString([nodes[n] for n in e['nodes']])
        for e in elements
        if e['type'] == 'way' and len(e['nodes']) >= MIN_LINESTRING_NODES
    }
    return nodes, ways


def fetch_node(node_id: int) -> Point | None:
    elements = fetch_elements(f'node/{node_id}.json')
    if elements is None:
        return None
    nodes, _ = parse_geometries(elements)
    return next(iter(nodes.values()), None)


def fetch_way(way_id: int) -> LineString | Polygon | None:
    elements = fetch_elements(f'way/{way_id}/full.json')
    if elements is None:
        return None
    _, ways = parse_geometries(elements)
    way = next(iter(ways.values()), None)
    if way is None:
        return None
    return Polygon(way) if way.is_ring else way


def fetch_relation(relation_id: int) -> GeometryCollection | None:
    elements = fetch_elements(f'relation/{relation_id}/full.json')
    if elements is None:
        return None
    _, ways = parse_geometries(elements)
    relation = next((e for e in elements if e['type'] == 'relation'), None)
    if relation is None:
        return None

    outer, inner = [], []
    for member in relation['members']:
        if member['type'] != 'way':
            continue
        line = ways.get(member['ref'])
        if line is None:
            continue
        (inner if member['role'] == 'inner' else outer).append(line)

    outer_polygons, *outer_leftovers = polygonize_full(outer)
    inner_rings = [p.exterior for p in get_parts(polygonize_full(inner)[0])]

    parts = []
    for polygon in get_parts(outer_polygons):
        holes = [ring for ring in inner_rings if polygon.contains(ring)]
        parts.append(Polygon(polygon.exterior, holes) if holes else polygon)

    # Ways that could not be assembled into polygons (e.g. self-crossing) stay as lines.
    parts.extend(itertools.chain.from_iterable(get_parts(leftover) for leftover in outer_leftovers))

    return GeometryCollection(parts)
