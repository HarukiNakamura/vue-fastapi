import numpy as np
import numpy.ma as ma
from AMD_Tools3 import lalo2mesh

def get_all_mesh(lat: ma.core.MaskedArray, lon: ma.core.MaskedArray) -> list:
    all_combination: np.array = np.array(np.meshgrid(lat, lon)).T.reshape(-1, 2)
    all_mesh: list[str] = [lalo2mesh(*p) for p in all_combination]
    return all_mesh

def mesh2bound(meshcode: str):
    mc: str = "".join(meshcode.split("-"))
    mcl: int = len(mc)
    if mcl == 4:
        south_sec = int(mc[0:2]) * 2400
        south = south_sec / 3600
        west = int(mc[2:4]) + 100
        north = (south_sec + 2400) / 3600
        east = west + 1
    else:
        south_sec = int(mc[0:2]) * 2400 + int(mc[4]) * 300
        west_sec = (int(mc[2:4]) + 100) * 3600 + int(mc[5]) * 450

        if mcl == 6:
            north_sec = south_sec + 300
            east_sec = west_sec + 450
        else:
            south_sec += int(mc[6]) * 30
            west_sec += int(mc[7]) * 45
            north_sec = south_sec + 30
            east_sec = west_sec + 45
        south = south_sec / 3600
        west = west_sec / 3600
        north = north_sec / 3600
        east = east_sec / 3600
    return south, north, west, east