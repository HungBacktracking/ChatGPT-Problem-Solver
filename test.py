import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load the pre-trained CLIP model and processor
model_name = "openai/clip-vit-base-patch16"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)

# Load and process the image
# image_path = "data/diagrams/diagram4.png"
image_path = os.path.join(os.path.dirname(__file__), "data", "diagrams", "diagram4.png")
image = Image.open(image_path)
inputs = processor(text=["a photo of", "a picture of"], images=image, return_tensors="pt")

# Forward pass to get the image embedding
outputs = model(**inputs)
image_embedding = outputs.logits_per_image
text_descriptions = [processor.decode(int(t), skip_special_tokens=True) for t in outputs.logits_per_text]

# Print the image embedding
print("Image Embedding Shape:", image_embedding.shape)
print("Image Embedding Values:", image_embedding)
print("Text Descriptions:", text_descriptions)

# You can also use the image embedding for downstream tasks like image classification or similarity checks with other images.
