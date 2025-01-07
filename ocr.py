from PIL import Image, ImageFilter, ImageOps
import pytesseract
import os
from correction import Correction



# Function to preprocess the image
def preprocess_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert("L")

    # Apply edge enhancement filter
    image = image.filter(ImageFilter.EDGE_ENHANCE)

    # Increase contrast
    image = ImageOps.autocontrast(image)

    # Perform thresholding
    image = image.point(lambda x: 0 if x < 128 else 255, '1')

    return image

# Function to perform OCR
def perform_ocr(image_path, lang="fra"):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    # Perform OCR
    text = pytesseract.image_to_string(preprocessed_image, lang=lang)
    # Correct the user's prompt
    corrected_text = Correction(text)
    return corrected_text

