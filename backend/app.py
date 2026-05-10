import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from main import (
    load_predictor,
    run_single_design_gallery_optimization
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clip_processor, clip_predictor = load_predictor()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/automatic-editor")
async def automatic_editor(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_image_path, params = run_single_design_gallery_optimization(
        input_path,
        OUTPUT_DIR
    )

    return {
        "image_url": "http://localhost:8000/enhanced-image",
        "params": params
    }


@app.get("/enhanced-image")
def get_enhanced_image():
    return FileResponse(os.path.join(OUTPUT_DIR, "enhanced_image.jpg"))