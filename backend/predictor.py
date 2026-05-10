from aesthetics_predictor import AestheticsPredictorV1
from transformers import CLIPProcessor
import torch
from tqdm import tqdm


def load_predictor():
    """
    Loads the aesthetic predictor processor and model from hugging face.
    """
    model_path = "shunk031/aesthetics-predictor-v1-vit-large-patch14"
    predictor = AestheticsPredictorV1.from_pretrained(model_path)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    return processor, predictor


def score_img(processor, predictor, image):
    """
    Score a single image with the predictor.
    """
    predictor.eval()
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = predictor(**inputs)
    pred_score = outputs.logits.item()
    return pred_score


def score_batch_img(processor, predictor, images, batch_size=8):
    """
    Score a large quantity of images in batches.
    """
    all_preds = []

    predictor.eval()
    with torch.no_grad():
        for i in tqdm(range(0, len(images), batch_size)):
            batch_images = images[i:i + batch_size]
            inputs = processor(images=batch_images, return_tensors="pt")
            outputs = predictor(**inputs)
            preds = outputs.logits
            all_preds.append(preds.cpu())
    return torch.cat(all_preds, dim=0)
