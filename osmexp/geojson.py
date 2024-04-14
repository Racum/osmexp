import json

from shapely import get_parts, to_geojson
from shapely.geometry import MultiPolygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from .fetcher import fetch_node, fetch_relation, fetch_way


def right_hand_rule(geometry: BaseGeometry) -> BaseGeometry:
    'Enforces the "right hand rule" as defined by the GeoJSON spec (RFC-7946, Section 3.1.6).'
    if geometry.geom_type == 'Polygon':
        if not geometry.exterior.is_ccw:
            return orient(geometry, sign=1)
        return geometry
    if geometry.geom_type == 'MultiPolygon':
        return MultiPolygon([right_hand_rule(p) for p in geometry.geoms])
    return geometry


def export_node(node_id) -> str:
    if node := fetch_node(node_id):
        return to_geojson(node)
    return f'Error exporting node {node_id}.'


def export_way(way_id) -> str:
    if way := fetch_way(way_id):
        return to_geojson(right_hand_rule(way))
    return f'Error exporting way {way_id}.'


def wrap_feature(part):
    return {
        'type': 'Feature',
        'properties': {},
        'geometry': json.loads(to_geojson(right_hand_rule(part))),
    }


def export_relation(relation_id) -> str:
    if rel := fetch_relation(relation_id):
        return json.dumps({'type': 'FeatureCollection', 'features': [wrap_feature(p) for p in get_parts(rel)]})
    return f'Error exporting relation {relation_id}.'
