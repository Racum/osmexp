import json

from shapely import get_parts, to_geojson
from shapely.geometry import MultiPolygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from .fetcher import fetch_node, fetch_relation, fetch_way


class ExportError(Exception):
    "Raised when an OSM element cannot be fetched or exported."


def right_hand_rule(geometry: BaseGeometry) -> BaseGeometry:
    'Enforces the "right hand rule" as defined by the GeoJSON spec (RFC-7946, Section 3.1.6).'
    if geometry.geom_type == 'Polygon':
        return orient(geometry, sign=1)
    if geometry.geom_type == 'MultiPolygon':
        return MultiPolygon([right_hand_rule(p) for p in geometry.geoms])
    return geometry


def export_node(node_id: int) -> str:
    node = fetch_node(node_id)
    if node is None:
        raise ExportError(f'Could not export node {node_id}.')
    return to_geojson(node)


def export_way(way_id: int) -> str:
    way = fetch_way(way_id)
    if way is None:
        raise ExportError(f'Could not export way {way_id}.')
    return to_geojson(right_hand_rule(way))


def wrap_feature(part: BaseGeometry) -> dict:
    return {
        'type': 'Feature',
        'properties': {},
        'geometry': json.loads(to_geojson(right_hand_rule(part))),
    }


def export_relation(relation_id: int) -> str:
    relation = fetch_relation(relation_id)
    if relation is None:
        raise ExportError(f'Could not export relation {relation_id}.')
    return json.dumps(
        {
            'type': 'FeatureCollection',
            'features': [wrap_feature(p) for p in get_parts(relation)],
        }
    )
