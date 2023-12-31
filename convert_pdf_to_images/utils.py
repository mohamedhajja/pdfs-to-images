"""
Utility functions for converting PDF files to images and processing them.
"""

import os
from typing import List
from pdf2image.pdf2image import convert_from_path
from PIL import Image
import streamlit as st


def create_destination_folder(destination_dir: str) -> None:
    """
    Creates a destination folder if it does not exist.

    Args:
        destination_dir (str): The path of the destination directory.
    """
    os.makedirs(destination_dir, exist_ok=True)


def convert_pdf_to_images(file_path: str) -> List[Image.Image]:
    """
    Converts a PDF file to a list of images.

    Args:
        file_path (str): The path of the PDF file to convert.

    Returns:
        List[Image.Image]: A list of images converted from the PDF file.
    """
    return convert_from_path(file_path)


def save_grayscale_image(
    image: Image.Image, destination_dir: str, file_name: str
) -> None:
    """
    Converts an image to grayscale and saves it to the specified directory.

    Args:
        image (Image.Image): The image to convert to grayscale.
        destination_dir (str): The directory where the grayscale image will be saved.
        file_name (str): The name of the file to save the image as.
    """
    grayscale_image = image.convert("L")
    grayscale_image.save(os.path.join(destination_dir, file_name), "JPEG")


def process_pdf_files(root_dir: str, destination_dir: str, folder: str) -> None:
    """
    Processes all PDF files in a directory, converting them to grayscale images.

    Args:
        root_dir (str): The root directory containing PDF files.
        destination_dir (str): The destination directory for the converted images.
        folder (str): The name of the folder to store results.
    """
    create_destination_folder(destination_dir)
    progress_bar = st.progress(0)

    # Initialize unique ID for file naming
    unique_id = 1
    log_file_path = os.path.join(destination_dir, f"{folder}_name_changes_log.txt")

    # Get the total number of PDF files for progress calculation
    total_files = sum(
        1 for file in os.listdir(root_dir) if file.lower().endswith(".pdf")
    )

    # Processed files count
    processed_files = 0

    with open(log_file_path, "w") as log_file:
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if file.lower().endswith(".pdf"):
                images = convert_pdf_to_images(file_path)
                log_file.write(
                    f"{os.path.basename(file_path)} ==> {folder}_{unique_id}\n"
                )
                for i, image in enumerate(images):
                    new_file_name = f"{folder}_{unique_id}_page{i+1}.jpg"
                    save_grayscale_image(image, destination_dir, new_file_name)
                unique_id += 1

                # Update processed files count
                processed_files += 1

                # Update progress bar
                progress = int((processed_files / total_files) * 100)
                progress_bar.progress(progress)

    st.success("Conversion Completed!")
