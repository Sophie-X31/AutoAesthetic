from PIL import Image, ImageEnhance
import numpy as np
from predictor import score_img, score_batch_img


# ---------------------------------------------- CROP --------------------------------------------

def generate_smart_crops(img):
    """
    Generate a variety of cropped images.
    """
    w, h = img.size
    crops = []

    def crop_box(x1, y1, x2, y2, label):
        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(w, int(x2))
        y2 = min(h, int(y2))

        if x2 > x1 and y2 > y1:
            crop = img.crop((x1, y1, x2, y2))
            crops.append((label, crop))

    # original
    crops.append(("original", img))

    # Center crops / zoom levels
    crop_box(w*0.05, h*0.05, w*0.95, h*0.95, "center_90")
    crop_box(w*0.10, h*0.10, w*0.90, h*0.90, "center_80")
    crop_box(w*0.15, h*0.15, w*0.85, h*0.85, "center_70")
    crop_box(w*0.20, h*0.20, w*0.80, h*0.80, "center_60")

    # Rule of thirds large quadrants
    third_w, third_h = w / 3, h / 3

    crop_box(0, 0, 2*third_w, 2*third_h, "thirds_top_left")
    crop_box(third_w, 0, w, 2*third_h, "thirds_top_right")
    crop_box(0, third_h, 2*third_w, h, "thirds_bottom_left")
    crop_box(third_w, third_h, w, h, "thirds_bottom_right")

    # Subject placed on thirds, but wider crops
    crop_box(0, 0, w*0.85, h, "subject_left_wide")
    crop_box(w*0.15, 0, w, h, "subject_right_wide")
    crop_box(0, 0, w, h*0.85, "subject_top_wide")
    crop_box(0, h*0.15, w, h, "subject_bottom_wide")

    # Horizontal emphasis
    crop_box(0, 0, w, h*0.55, "top_55")
    crop_box(0, 0, w, h*0.65, "top_65")
    crop_box(0, h*0.35, w, h, "bottom_65")
    crop_box(0, h*0.45, w, h, "bottom_55")

    # Vertical emphasis
    crop_box(0, 0, w*0.55, h, "left_55")
    crop_box(0, 0, w*0.65, h, "left_65")
    crop_box(w*0.35, 0, w, h, "right_65")
    crop_box(w*0.45, 0, w, h, "right_55")

    # Reduce sky / reduce ground for outdoor photos
    crop_box(0, h*0.10, w, h, "less_sky_10")
    crop_box(0, h*0.15, w, h, "less_sky_15")
    crop_box(0, h*0.20, w, h, "less_sky_20")

    crop_box(0, 0, w, h*0.90, "less_ground_10")
    crop_box(0, 0, w, h*0.85, "less_ground_15")
    crop_box(0, 0, w, h*0.80, "less_ground_20")

    # Slight off-center crops for small reframing adjustments
    crop_box(w*0.05, h*0.00, w*0.95, h*0.90, "slight_up")
    crop_box(w*0.05, h*0.10, w*0.95, h, "slight_down")
    crop_box(w*0.00, h*0.05, w*0.90, h*0.95, "slight_left")
    crop_box(w*0.10, h*0.05, w, h*0.95, "slight_right")

    # Tighter portrait-style crops
    crop_box(w*0.15, h*0.05, w*0.85, h, "portrait_center_tall")
    crop_box(w*0.10, h*0.05, w*0.80, h, "portrait_left_tall")
    crop_box(w*0.20, h*0.05, w*0.90, h, "portrait_right_tall")

    return crops


def choose_best_crop(img, predictor, processor):
    """
    Select the cropping method that gets the highest score.
    """
    crop_options = generate_smart_crops(img)
    scores = score_batch_img(processor, predictor, images=[crop for _, crop in crop_options])

    idx = scores.argmax().item()
    best_score = scores[idx].item()
    best_label, best_crop = crop_options[idx]

    print(f"Best crop: {best_label} | Score: {best_score:.4f}")
    return best_crop, best_score, best_label


# --------------------------------------------- METRICS --------------------------------------------

def adjust_shadows(img, factor=1.0):
    arr = np.asarray(img).astype(np.float32) / 255.0
    mask = np.clip((0.5 - arr) * 2, 0, 1)
    arr = arr + mask * (factor - 1.0) * 0.5
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))


def adjust_highlights(img, factor=1.0):
    arr = np.asarray(img).astype(np.float32) / 255.0
    mask = np.clip((arr - 0.5) * 2, 0, 1)
    arr = arr + mask * (factor - 1.0) * 0.5
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))


def adjust_temperature(img, warmth=0.0):
    """
    warmth > 0 = warmer
    warmth < 0 = cooler
    Suggested range: -0.15 to 0.15
    """
    arr = np.asarray(img).astype(np.float32)

    arr[:, :, 0] *= (1 + warmth)      # red
    arr[:, :, 2] *= (1 - warmth)      # blue

    arr = np.clip(arr, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def optimize_options(img, options, make_candidate, name, predictor, processor):
    """
    Helper function to find the best adjustment of a metric on a given image.
    """
    candidates = [make_candidate(img, value) for value in options]
    scores = score_batch_img(processor, predictor, images=candidates)

    idx = scores.argmax().item()
    best_score = scores[idx].item()
    best_value, best_img = options[idx], candidates[idx]

    print(f"Best {name}: {best_value} | Score: {best_score:.4f}")
    return best_img, best_score, best_value


def optimize_brightness(img, predictor, processor):
    options = [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]

    return optimize_options(
        img,
        options,
        lambda im, v: ImageEnhance.Brightness(im).enhance(v),
        "brightness",
        predictor,
        processor
    )


def optimize_contrast(img, predictor, processor):
    options = [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]

    return optimize_options(
        img,
        options,
        lambda im, v: ImageEnhance.Contrast(im).enhance(v),
        "contrast",
        predictor,
        processor
    )


def optimize_color(img, predictor, processor):
    options = [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]

    return optimize_options(
        img,
        options,
        lambda im, v: ImageEnhance.Color(im).enhance(v),
        "saturation/color",
        predictor,
        processor
    )


def optimize_sharpness(img, predictor, processor):
    options = [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]

    return optimize_options(
        img,
        options,
        lambda im, v: ImageEnhance.Sharpness(im).enhance(v),
        "sharpness",
        predictor,
        processor
    )


def optimize_shadows(img, predictor, processor):
    options = [0.85, 0.95, 1.0, 1.05, 1.15, 1.25]

    return optimize_options(
        img,
        options,
        lambda im, v: adjust_shadows(im, factor=v),
        "shadows",
        predictor,
        processor
    )


def optimize_highlights(img, predictor, processor):
    options = [0.75, 0.85, 0.95, 1.0, 1.05, 1.15]

    return optimize_options(
        img,
        options,
        lambda im, v: adjust_highlights(im, factor=v),
        "highlights",
        predictor,
        processor
    )


def optimize_temperature(img, predictor, processor):
    options = [-0.12, -0.08, -0.04, 0.0, 0.04, 0.08, 0.12]

    return optimize_options(
        img,
        options,
        lambda im, v: adjust_temperature(im, warmth=v),
        "temperature",
        predictor,
        processor
    )


# ----------------------------------- INDEPENDENT OPTIMIZATION ----------------------------------------------

def optimize_by_order(img, predictor, processor):
    """
    Find the best adjustment of each metric independently in order.
    """

    results = {}

    # Original score
    original_score = score_img(processor, predictor, img)
    results["original_score"] = original_score
    print(f"Original score: {original_score:.4f}")

    # 1. Crop
    img, crop_score, crop_label = choose_best_crop(img, predictor, processor)
    results["crop"] = crop_label
    results["crop_score"] = crop_score

    # 2. Brightness
    img, _, brightness_value = optimize_brightness(img, predictor, processor)
    results["brightness"] = brightness_value

    # 3. Contrast
    img, _, contrast_value = optimize_contrast(img, predictor, processor)
    results["contrast"] = contrast_value

    # 4. Saturation
    img, _, color_value = optimize_color(img, predictor, processor)
    results["saturation"] = color_value

    # 5. Sharpness
    img, _, sharpness_value = optimize_sharpness(img, predictor, processor)
    results["sharpness"] = sharpness_value

    # 6. Shadows
    img, _, shadows_value = optimize_shadows(img, predictor, processor)
    results["shadows"] = shadows_value

    # 7. Highlights
    img, _, highlights_value = optimize_highlights(img, predictor, processor)
    results["highlights"] = highlights_value

    # 8. Temperature
    img, _, temp_value = optimize_temperature(img, predictor, processor)
    results["temperature"] = temp_value

    # Final score
    final_score = score_img(processor, predictor, img)
    results["final_score"] = final_score

    return img, results


# ------------------------------------------ DESIGN GALLERY -------------------------------------------------


def apply_params(img, params):
    edited = img.copy()

    edited = ImageEnhance.Brightness(edited).enhance(params["brightness"])
    edited = ImageEnhance.Contrast(edited).enhance(params["contrast"])
    edited = ImageEnhance.Color(edited).enhance(params["saturation"])
    edited = ImageEnhance.Sharpness(edited).enhance(params["sharpness"])

    edited = adjust_shadows(edited, factor=params["shadows"])
    edited = adjust_highlights(edited, factor=params["highlights"])
    edited = adjust_temperature(edited, warmth=params["temperature"])

    return edited


def optimize_by_directional_steps(img, predictor, processor, step=0.05, max_iters=50):
    """
    Find the best combination of metric adjustments using the Design Gallery approach.
    """
    params = {
        "brightness": 1.0,
        "contrast": 1.0,
        "saturation": 1.0,
        "sharpness": 1.0,
        "shadows": 1.0,
        "highlights": 1.0,
        "temperature": 0.0
    }

    bounds = {
        "brightness": (0.6, 1.5),
        "contrast": (0.6, 1.6),
        "saturation": (0.5, 1.8),
        "sharpness": (0.5, 2.0),
        "shadows": (0.5, 1.8),
        "highlights": (0.5, 1.5),
        "temperature": (-0.25, 0.25)
    }

    current_img = apply_params(img, params)
    current_score = score_img(processor, predictor, current_img)

    print(f"Starting score: {current_score:.4f}")

    for iteration in range(max_iters):
        best_candidate_img = current_img
        best_candidate_score = current_score
        best_candidate_params = params.copy()
        best_change = None

        for param_name in params:
            for direction in [-step, step]:
                candidate_params = params.copy()
                candidate_params[param_name] += direction

                low, high = bounds[param_name]

                if not (low <= candidate_params[param_name] <= high):
                    continue

                candidate_img = apply_params(img, candidate_params)
                candidate_score = score_img(processor, predictor, candidate_img)

                if candidate_score > best_candidate_score and candidate_score > current_score + 0.003:
                    best_candidate_score = candidate_score
                    best_candidate_img = candidate_img
                    best_candidate_params = candidate_params
                    best_change = (param_name, direction)

        if best_change is None:
            print(f"Stopped at iteration {iteration}. No change improved the image.")
            break

        params = best_candidate_params
        current_img = best_candidate_img
        current_score = best_candidate_score

        print(
            f"Iter {iteration + 1}: "
            f"{best_change[0]} {'+' if best_change[1] > 0 else '-'}{step} "
            f"→ score {current_score:.4f} | params: {params}"
        )

    return current_img, current_score, params