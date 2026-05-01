import torch
from transformers import AutoProcessor, AutoModelForVision2Seq


def load_vlm():
    """
    Load the small vision-language processor and model from hugging face.
    """
    model_path = "HuggingFaceTB/SmolVLM-256M-Instruct"
    processor = AutoProcessor.from_pretrained(model_path)
    model = AutoModelForVision2Seq.from_pretrained(model_path, torch_dtype=torch.float32)
    return processor, model


def generate_response(processor, model, image):
    """
    Generate response using the given VLM.
    """

    # Prompt
    prompt = """You are a professional photography instructor. 
    Analyze the provided image and give constructive, beginner-friendly feedback.
    Structure your response in the following sections:

    1. Overall Impression (1-2 sentences)
    2. What Works Well (bullet points)
    3. What Could Be Improved (bullet points)
    4. How to Improve (actionable steps the user can apply next time in 1-3 sentences)

    Focus on:
    - Composition (framing, subject placement, distractions)
    - Lighting (exposure, shadows, highlights, direction of light)
    - Color (white balance, saturation)
    - Sharpness and focus
    - Mood and storytelling

    Be specific, practical, and avoid vague statements."""

    # Format Input
    message = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    prompt_formatted = processor.apply_chat_template(message, add_generation_prompt=True)
    inputs = processor(text=prompt_formatted, images=image, return_tensors="pt")

    # Generate Response
    output = model.generate(**inputs, max_new_tokens=500)
    output_trim = output[:, inputs["input_ids"].shape[1]:] # remove prompt from response
    response = processor.batch_decode(
        output_trim,
        skip_special_tokens=True
    )
    # print(processor.batch_decode(output, skip_special_tokens=True))
    return response[0].strip()