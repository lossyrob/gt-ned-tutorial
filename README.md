# Tutorial Code for viewing PA NED data

This codebase is for a tutorial to view PA National Elevation Data.

### Quick Start

Make sure you have [GDAL](http://www.gdal.org/) installed. For a script to build and install gdal on Ubuntu, see [this gist](https://gist.github.com/lossyrob/4348503).

You'll also need the python-geotrellis package installed (https://pypi.python.org/pypi/python-geotrellis/0.1.0).
If you have pip, you can do this with "pip install python-geotrellis". This will install the gt-tool script that is used by getdata.py.

Clone this repository, and then run the getdata.py script. It will pull all the NED PA data, which is a lot of data, so if you want you can cut it off early to only see part of the data.

Do

```bash
./sbt run
```

to start the GeoTrellis server. Visit http://localhost:8880/admin, and you should see the downloaded data.
