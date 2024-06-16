from fastapi import FastAPI, UploadFile
from osgeo import gdal
import io
from pixels_correction import restore_broken_pixels
import numpy as np

app = FastAPI()

@app.post("/api/")
async def add_task(file: UploadFile):
    content = await file.read()
    file_bytes = io.BytesIO(content)
    
    vsi_filename = f'/vsimem/{file.filename}'

    gdal.FileFromMemBuffer(vsi_filename, file_bytes.getvalue())
    
    crop_arr = gdal.Open(vsi_filename).ReadAsArray()

    crop_arr = np.transpose(crop_arr, (1, 2, 0))
    corrected_image, report = restore_broken_pixels(crop_arr.copy())
    print(report)

    gdal.Unlink(vsi_filename)

    return {
        "report": report
    }