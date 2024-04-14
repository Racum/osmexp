import json

import pytest

from osmexp.geojson import export_node, export_relation, export_way


@pytest.mark.vcr()
def test_export_node():
    geojson = json.loads(export_node(9589344640))
    assert geojson['type'] == 'Point'
    assert geojson['coordinates'] == [12.3394685, 45.4331611]


@pytest.mark.vcr()
def test_export_open_way():
    geojson = json.loads(export_way(398987317))
    assert geojson['type'] == 'LineString'


@pytest.mark.vcr()
def test_export_closed_way():
    geojson = json.loads(export_way(430963095))
    assert geojson['type'] == 'Polygon'


@pytest.mark.vcr()
def test_export_single_relation():
    geojson = json.loads(export_relation(4817103))
    assert geojson['type'] == 'FeatureCollection'
    assert len(geojson['features']) == 1
    assert {f['geometry']['type'] for f in geojson['features']} == {'Polygon'}


@pytest.mark.vcr()
def test_export_split_relation():
    geojson = json.loads(export_relation(1850539))
    assert geojson['type'] == 'FeatureCollection'
    assert len(geojson['features']) == 9
    assert {f['geometry']['type'] for f in geojson['features']} == {'Polygon'}


@pytest.mark.vcr()
def test_export_self_crossing_relation():
    geojson = json.loads(export_relation(284570))
    assert geojson['type'] == 'FeatureCollection'
    assert len(geojson['features']) == 3
    assert {f['geometry']['type'] for f in geojson['features']} == {'LineString'}
