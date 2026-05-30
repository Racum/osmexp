import pytest

from osmexp.fetcher import fetch_node, fetch_relation, fetch_way


@pytest.mark.vcr()
def test_fetch_node_as_point():
    node = fetch_node(9589344640)  # Outdoor seating.
    assert node.geom_type == 'Point'
    assert (node.x, node.y) == (12.3394685, 45.4331611)


@pytest.mark.vcr()
def test_fetch_open_way_as_linestring():
    way = fetch_way(398987317)  # Canal Grande.
    assert way.geom_type == 'LineString'
    assert len(way.coords) == 125
    assert way.length == pytest.approx(0.049109547915808335)  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_closed_way_as_polygon():
    way = fetch_way(430963095)  # Column of Saint Mark.
    assert way.geom_type == 'Polygon'
    assert way.area == pytest.approx(3.089739999806592e-09)  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_single_relation_as_polygon():
    rel = fetch_relation(4817103)  # Venice.
    assert rel.geom_type == 'GeometryCollection'
    assert rel.geoms[0].geom_type == 'Polygon'
    assert len(rel.geoms[0].exterior.coords) == 849
    assert rel.geoms[0].area == pytest.approx(0.0006893646889149643)  # Point units, not meters.


@pytest.mark.vcr()
def test_fetch_split_relation_as_many_polygons():
    rel = fetch_relation(1850539)  # Parque Estadual Paulo César Vinha
    assert rel.geom_type == 'GeometryCollection'
    assert len(rel.geoms) == 9
    assert {g.geom_type for g in rel.geoms} == {'Polygon'}
    assert sum(g.area for g in rel.geoms) == pytest.approx(0.0013636596847249436)


@pytest.mark.vcr()
def test_fetch_self_crossing_relation_as_many_linestrings():
    rel = fetch_relation(284570)  # Suzuka
    assert rel.geom_type == 'GeometryCollection'
    assert len(rel.geoms) == 2
    assert {g.geom_type for g in rel.geoms} == {'LineString'}
    assert sum(g.area for g in rel.geoms) == 0
