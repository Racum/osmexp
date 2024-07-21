import itertools
from http import HTTPStatus

import requests
from shapely import get_parts, polygonize_full
from shapely.geometry import GeometryCollection, LineString, Point, Polygon

API_URL = 'https://www.openstreetmap.org/api/0.6'

class Feature :
    def parse_nodes_ways(self, elements: list[dict]) -> tuple[list[dict], list[dict]]:
        nodes = {e['id']: Point(e['lon'], e['lat']) for e in elements if e['type'] == 'node'}
        ways = [LineString([nodes[n] for n in e['nodes']]) for e in elements if e['type'] == 'way']
        return list(nodes.values()), ways

    def __init__(self, elements: list[dict], tp: str) -> None :
        self.nodes, self.ways = self.parse_nodes_ways(elements)
        self.type = tp
        for e in elements:
            if e['type'] == self.type :
                if 'name' in e['tags'] :
                    self.name = e['tags']['name']
                else:
                    self.name = ''
                break
    def geometry(self) -> Point | LineString | Polygon | GeometryCollection:
        if self.type == 'node' :
            return self.nodes[0]
        elif self.type == 'way' :
            way = self.ways[0]
            return Polygon(way) if way.is_closed and way.is_ring else way
        else :
            cases = [get_parts(p) for p in polygonize_full(self.ways) if p]
            parts = list(itertools.chain(*cases))
            return GeometryCollection(parts)
            
def fetch(feature_id: int, feature_type: str) -> Feature | None :
    response: requests.Response
    if feature_type == 'node' :
        response = requests.get(f'{API_URL}/{feature_type}/{feature_id}.json')
    else :
        response = requests.get(f'{API_URL}/{feature_type}/{feature_id}/full.json')
    if response.status_code != HTTPStatus.OK:
        return None
    return Feature(response.json()['elements'], feature_type)

