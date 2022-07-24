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
    print(InputData)
    metElement: str = InputData.inputData["metElement"]
    date: list[str] = InputData.inputData["date"]
    border: list[float] = InputData.inputData["border"]
    Tm, tim, lat, lon, name, uni = GetMetData(metElement, date, border, namuni=True)
    all_mesh = get_all_mesh(lat, lon)

    # data_lim = {
    #     "TMP_mea":[-20,40],
    #     "TMP_max":[-20,40],
    #     "TMP_min":[-20,40],
    #     "APCP":[],
    #     "OPR":[0, 1], #binary data
    #     "SSD":[],
    #     "GSR":[],
    #     "DLR":[],
    #     "RH":[],
    #     "WIND":[],
    #     "SD":[],
    #     "SWE":[],
    #     "SFW":[]}

    response_json: dict = {}
    colourstep = cm.linear._colormaps["viridis"].scale(vmin=np.nanmin(Tm), vmax=np.nanmax(Tm))
    ndays, nlat, nlng = Tm.shape
    data = np.reshape(Tm, (ndays, nlat*nlng)).T
    all_latlng = list(map(lambda tuple: [[tuple[0], tuple[2]],[tuple[1], tuple[3]]], (map(mesh2bound, all_mesh))))
    for i in range(len(all_latlng)):
        meshcode = all_mesh[i]
        latlng = all_latlng[i]
        d = list(data[i])
        colorcode = ["#353535" if np.isnan(x) else colourstep(x) for x in d]
        response_json[meshcode] = {"border":latlng, "fillColor":colorcode}
    # with open("output.json", "w") as f:
    #     json.dump(response_json, f)
    return response_json


# Dockerfileからuvicorn(FastAPIサーバー）を起動する
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        reload=True,
        port=3000,
        log_level="debug",)