import os
import csv
import json
from PIL import Image
from predictor import load_predictor, score_batch_img
from vlm import load_vlm, generate_response
from optimizer import choose_best_crop, optimize_by_directional_steps, optimize_by_order, generate_design_gallery_options


# --------------------------------------------- HELPER FUNCTIONS -------------------------------------------------

def load_images(image_dir):
    filenames = [f for f in os.listdir(image_dir)]
    images = [Image.open(os.path.join(image_dir, f)).convert("RGB") for f in filenames]
    return filenames, images


# ------------------------------------------ USE CASE 1: Rank Photo --------------------------------------------

def rank_images(input_path):
    filenames, images = load_images(input_path)
    scores = score_batch_img(clip_processor, clip_predictor, images)
    return sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)


# ----------------------------------------- USE CASE 2: Optimize Photo ------------------------------------------


def critique_batch_images(input_path):
    filenames, images = load_images(input_path)

    critique = dict()
    for filename, img in zip(filenames, images):
        print(f"Evaluating {filename}...")
        response = generate_response(vlm_processor, vlm_model, img)
        print(response)
        critique[filename] = response
    return critique


def run_batch_independent_optimization(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    filenames, images = load_images(input_path)

    for filename, img in zip(filenames, images):
        print(f"Processing {filename}...")
        best_img, results = optimize_by_order(img, clip_predictor, clip_processor)

        best_img.save(os.path.join(output_path, filename), quality=95)

        base, _ = os.path.splitext(filename)
        result_path = os.path.join(output_path, base + "_result.csv")
        with open(result_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value"])
            for k, v in results.items():
                writer.writerow([k, v])
    
    print("Finished running.")


def run_batch_design_gallery_optimization(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    filenames, images = load_images(input_path)

    for filename, img in zip(filenames, images):
        print(f"Processing {filename}...")
        best_crop, _, _ = choose_best_crop(img, clip_predictor, clip_processor)
        best_img, best_score, best_params = optimize_by_directional_steps(
            best_crop,
            clip_predictor, clip_processor,
            step=0.05, max_iters=50
        )
        best_params["final_score"] = best_score

        best_img.save(os.path.join(output_path, filename), quality=95)

        base, _ = os.path.splitext(filename)
        result_path = os.path.join(output_path, base + "_result.csv")
        with open(result_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value"])
            for k, v in best_params.items():
                writer.writerow([k, v])
    
    print("Finished running.")

def run_design_gallery_step(input_image_path, output_path, step=0.12, current_params=None):
    os.makedirs(output_path, exist_ok=True)

    img = Image.open(input_image_path).convert("RGB")

    gallery_options = generate_design_gallery_options(
        img,
        current_params=current_params,
        step=step
    )

    metadata = []

    for i, option in enumerate(gallery_options):
        filename = f"option_{i}.jpg"

        option["image"].save(
            os.path.join(output_path, filename),
            quality=95
        )

        metadata.append({
            "image": filename,
            "changed_param": option["changed_param"],
            "direction": option["direction"],
            "params": option["params"]
        })

    with open(os.path.join(output_path, "gallery_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    return gallery_options


# -------------------------------------------- TESTING --------------------------------------------------

if __name__ == "__main__":
    #clip_processor, clip_predictor = load_predictor()
    #vlm_processor, vlm_model = load_vlm()

    # ranking = rank_images("../wedding_testset")
    # print(ranking)

    # critique = critique_batch_images("../street_testset")

    # run_batch_independent_optimization("../single_testset", "../output_order")

    # run_batch_design_gallery_optimization("../single_testset", "../output_gallery")

    run_design_gallery_step(
        "../single_testset/test.jpg",
        "../manual_design"
    )
    
