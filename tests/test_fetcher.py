import pytest

from osmexp.fetcher import fetch


@pytest.mark.vcr()
def test_fetch_node_as_point():
    node = fetch(9589344640,'node').geometry()  # Outdoor seating.
    assert node.geom_type == 'Point'
    assert node.x, node.y == (12.3394685, 45.4331611)


@pytest.mark.vcr()
def test_fetch_open_way_as_linestring():
    way = fetch(398987317, 'way').geometry()  # Canal Grande.
    assert way.geom_type == 'LineString'
    assert len(way.coords) == 124
    assert way.length == 0.049109547915778894  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_closed_way_as_polygon():
    way = fetch(430963095, 'way').geometry()  # Column of Saint Mark.
    assert way.geom_type == 'Polygon'
    assert way.area == 0.000000003089739999806592  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_single_relation_as_polygon():
    rel = fetch(4817103, 'relation').geometry()  # Venice.
    assert rel.geom_type == 'GeometryCollection'
    assert rel.geoms[0].geom_type == 'Polygon'
    assert len(rel.geoms[0].exterior.coords) == 836
    assert round(rel.geoms[0].area,3) == round(0.0006893472015599638,3)  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_split_relation_as_many_polygons():
    rel = fetch(1850539, 'relation').geometry()  # Parque Estadual Paulo César Vinha
    assert rel.geom_type == 'GeometryCollection'
    assert len(rel.geoms) == 9
    assert {g.geom_type for g in rel.geoms} == {'Polygon'}
    assert round(sum(g.area for g in rel.geoms),3) == round(0.0013636500965699464,3)


@pytest.mark.vcr()
def test_fetch_self_crossing_relation_as_many_linestrings():
    rel = fetch(284570, 'relation').geometry()  # Suzuka
    assert rel.geom_type == 'GeometryCollection'
    assert len(rel.geoms) == 3
    assert {g.geom_type for g in rel.geoms} == {'LineString'}
    assert sum(g.area for g in rel.geoms) == 0
