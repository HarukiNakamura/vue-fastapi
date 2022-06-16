from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from pydantic import BaseModel

from AMD_Tools3 import GetMetData
from my_utils import get_all_mesh, mesh2bound

import branca.colormap as cm
import numpy as np


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class InputData(BaseModel):
    # InputData.inputData["metElement"] => str
    # InputData.inputData["date"] => list[str]
    # InputData.inputData["border"] list[float]
    inputData: dict
@app.post("/api/result")
def index1(InputData: InputData):
    metElement: str = InputData.inputData["metElement"]
    date: list[str] = InputData.inputData["date"]
    border: list[float] = InputData.inputData["border"]
    Tm, tim, lat, lon, name, uni = GetMetData(metElement, date, border, namuni=True)
    all_mesh = get_all_mesh(lat, lon)
    j = 0
    data = Tm[j].flatten()
    colourstep = cm.linear._colormaps["viridis"].scale(vmin=min(data), vmax=max(data))
    geojson = {"type": "FeatureCollection", "features": []}
    colorcode = ["#353535" if np.isnan(x) else colourstep(x) for x in data]
    for i in range(len(all_mesh)):
        meshcode = all_mesh[i]
        s, n, w, e = mesh2bound(meshcode)  
        geojson_dict = {
        "type":"Feature",
        "properties": {"meshcode":meshcode, "eledata":str(data[i]), "fillcolor":colorcode[i]},
        "geometry": {"type": "Polygon","coordinates": [[[w, s],[e, s],[e, n],[w, n],[w, s]]]}
        }
        geojson["features"].append(geojson_dict)
    return geojson


# Dockerfileからuvicorn(FastAPIサーバー）を起動する
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        reload=True,
        port=3000,
        log_level="debug",)