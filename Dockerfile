# Use the official GDAL base image
FROM osgeo/gdal:ubuntu-small-3.6.2


# Set the environment variable for GDAL

# Install GDAL development libraries
RUN apt-get update && apt-get install -y \
    libgdal-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set GDAL library path explicitly
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV LD_LIBRARY_PATH=/usr/lib
