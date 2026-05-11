import os
import shutil
import time
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from main import (
    load_predictor,
    run_single_design_gallery_optimization,
    run_design_gallery_step
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
DESIGN_UPLOAD_DIR = "design_uploads"
DESIGN_OUTPUT_DIR = "design_outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DESIGN_UPLOAD_DIR, exist_ok=True)
os.makedirs(DESIGN_OUTPUT_DIR, exist_ok=True)

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

@app.post("/design-gallery")
async def design_gallery(file: UploadFile = File(...)):
    request_id = str(uuid.uuid4())

    input_path = os.path.join(DESIGN_UPLOAD_DIR, f"{request_id}_{file.filename}")
    output_dir = os.path.join(DESIGN_OUTPUT_DIR, request_id)

    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    gallery_options = run_design_gallery_step(
        input_path,
        output_dir,
        step=0.12
    )

    options = []

    for i, option in enumerate(gallery_options):
        options.append({
            "image_url": f"http://localhost:8000/design-gallery/image/{request_id}/option_{i}.jpg",
            "changed_param": option["changed_param"],
            "direction": option["direction"],
            "params": option["params"]
        })

    return {"options": options}


@app.get("/design-gallery/image/{request_id}/{filename}")
def get_design_gallery_image(request_id: str, filename: str):
    image_path = os.path.join(DESIGN_OUTPUT_DIR, request_id, filename)
    return FileResponse(image_path)