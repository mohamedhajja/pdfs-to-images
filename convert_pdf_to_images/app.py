"""
Main module for a Streamlit app that converts PDFs to images.
"""

import streamlit as st
from folder_chooser import FolderSelectionApp
from utils import process_pdf_files


def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    st.title("PDF to Image Converter")

    app = FolderSelectionApp()

    source_dir = app.setup_source_folder_selection()
    destination_dir = app.setup_destination_folder_selection()
    folder_option = app.setup_folder_option()

    if app.display_conversion_button():
        if source_dir and destination_dir:
            process_pdf_files(source_dir, destination_dir, folder_option)
        else:
            st.error("Please specify both source and destination paths")


if __name__ == "__main__":
    main()
