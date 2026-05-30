# osmexp - OpenStreetMap GeoJSON Exporter

The [OSM API](https://wiki.openstreetmap.org/wiki/API_v0.6) uses a specific format for their geometric primitive types based on nodes, ways and relations; and those unfortunately don’t translate 1:1 with [GeoJSON types](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1), thus a conversion is needed.

## Installation:

Make sure you have at least Python 3.11, and install it with:

```
$ pip install osmexp
```

The only requirements are `Requests` and `Shapely`.

## Usage

For all exports, this is the format:

```
$ osmexp [element_type] [element_id]
```

Where `element_type` can be `node`, `way` or `rel` (for "relation"). And the ID is the numerical identifier used by OSM, if you don’t know how to get the OSM ID, [follow this article](https://racum.blog/articles/osm-to-geojson/#features-on-openstreetmap).

The output is set to `STDOUT`, and it is recommended to be piped into a file or another command. On failure, an error message is sent to `STDERR` and the process exits with a non-zero status.

### Exporting Nodes:

```
$ osmexp node 9589344640 > outdoor_seating.geojson
```

This returns a GeoJSON with a `Point` as a root type.

### Exporting Ways:

```
$ osmexp way 398987317 > canal_grande.geojson
```

This returns a GeoJSON with a `LineString` as a root type if the line is “open” or `Polygon` if the line is “closed”.

### Exporting Relations:

```
$ osmexp rel 4817103 > venice.geojson
```

This returns a GeoJSON with a `FeatureCollection` as a root, and the internal features as `LineString` or `Polygon`, depending if they can self-close, or fail the polygon transformation by other means (self crossing, etc).

## Development

Clone the repository and install in editable mode with the `dev` extras (tests, linter):

```
$ pip install -e '.[dev]'
```

All dependencies are declared in `pyproject.toml`; there are no separate requirements files.

Run the test suite (it replays recorded HTTP responses, so no network is needed):

```
$ pytest
```

Lint and format with [Ruff](https://docs.astral.sh/ruff/):

```
$ ruff check .
$ ruff format .
```

## License

This library is released under the **3-Clause BSD License**.

**tl;dr**: *"free to use as long as you credit me"*.
