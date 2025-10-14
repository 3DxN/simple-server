# Simple HTTPS server used for serving OME-Zarr data

Difference to the standard Simple HTTP Python server:
- Added permissive CORS settings
- Added support for HTTP range requests, to address issues with rendering of sharded OME-Zarr data. See: https://forum.image.sc/t/tools-for-converting-to-ome-zarr-v0-5/114369/31


## Invocation:
```
python server.py
```
No additional dependencies required.

Serving on port `5500` by default. A custom port can be specified by invoking:
```
python server.py [port number]
```

