import io
import uuid

from fastapi import FastAPI, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import cv2
from osgeo import gdal
from pixels_correction import restore_broken_pixels
import numpy as np

app = FastAPI()

app.mount("/storage", StaticFiles(directory="./storage"), name="storage")

STORAGE_DIR = 'storage'


@app.post("/api")
async def correct_image(file: UploadFile, request: Request):
    content = await file.read()
    file_bytes = io.BytesIO(content)

    vsi_filename = f'/vsimem/{file.filename}'

    gdal.FileFromMemBuffer(vsi_filename, file_bytes.getvalue())

    crop_arr = gdal.Open(vsi_filename).ReadAsArray()

    crop_arr = np.transpose(crop_arr, (1, 2, 0))
    corrected_image, report = restore_broken_pixels(crop_arr.copy())

    gdal.Unlink(vsi_filename)

    storage_filename = f'{STORAGE_DIR}/{uuid.uuid4()}.tif'

    cv2.imwrite(storage_filename, corrected_image)

    return {
        'image_url': f'{request.base_url}{storage_filename}', 'corrected_pixels': report
    }
