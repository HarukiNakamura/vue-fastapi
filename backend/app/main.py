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
    all_mesh:list[str] = get_all_mesh(lat, lon)

    json: dict = {}
    for i in range(len(Tm)):
        data = Tm[i].flatten()
        colourstep = cm.linear._colormaps["viridis"].scale(vmin=min(data), vmax=max(data))
        colorcode = ["#353535" if np.isnan(x) else colourstep(x) for x in data]
        geojson: dict = {"type": "FeatureCollection", "features": []}
        for j in range(len(all_mesh)):
            meshcode: str = all_mesh[j]
            s, n, w, e = mesh2bound(meshcode)  
            geojson_dict = {
            "type":"Feature",
            "properties": {"meshcode":meshcode, "eledata":str(data[j]), "fillcolor":colorcode[j]},
            "geometry": {"type": "Polygon","coordinates": [[[w, s],[e, s],[e, n],[w, n],[w, s]]]}
            }
            geojson["features"].append(geojson_dict)
        json[str(i)] = {"time":str(tim[i]).split(" ")[0], "geojson":geojson}
    return json



# Dockerfileからuvicorn(FastAPIサーバー）を起動する
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        reload=True,
        port=3000,
        log_level="debug",)