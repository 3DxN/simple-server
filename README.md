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


## Alternatives

[ome_zarr_py](https://github.com/ome/ome-zarr-py) implements a CLI tool for serving and viewing Zarr files (Invocation: `ome_zarr view [OMEZarrFile]`). This may be more convenient to use in some circumstances, as it opens the image through the ngff-validator frontend, from where multiple viewers (Vizarr, Vol-E, Neuroglancer, napari) are available at a mouseclick to display a Zarr image. 

