#!/bin/bash -ve

kliko-run kliko/simms --output simms  --tel meerkat
kliko-run kliko/meqtree-pipeliner --output meqtree-pipeliner --input simms
kliko-run kliko/wsclean --output wsclean --input meqtree-pipeliner
