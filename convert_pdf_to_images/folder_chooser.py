"""
Module for handling folder selection in a Streamlit app.
This module contains a class and methods to facilitate the selection of source and 
destination folders in a Streamlit application, specifically for file conversion tasks.
"""

from typing import Optional
import tkinter as tk
from tkinter import filedialog
import streamlit as st


class FolderSelectionApp:
    """
    A class to encapsulate folder selection functionalities for a Streamlit application.
    """

    def __init__(self) -> None:
        self.source_dir: Optional[str] = None
        self.destination_dir: Optional[str] = None

    @staticmethod
    def select_folder() -> str:
        """
        Opens a dialog to select a folder and returns the selected folder's path.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder_path = filedialog.askdirectory(master=root)
        root.destroy()
        return folder_path

    def setup_source_folder_selection(self):
        """
        Setup and handle the source folder selection in the Streamlit app.
        """
        source_dir = st.session_state.get("source_folder_path", None)
        if st.button("Select Source Folder"):
            source_dir = self.select_folder()
            st.session_state["source_folder_path"] = source_dir
        if source_dir:
            st.write("Selected source folder path:", source_dir)
        return source_dir

    def setup_destination_folder_selection(self):
        """
        Setup and handle the destination folder selection in the Streamlit app.
        """
        destination_dir = st.session_state.get("destination_folder_path", None)
        if st.button("Select Destination Folder"):
            destination_dir = self.select_folder()
            st.session_state["destination_folder_path"] = destination_dir
        if destination_dir:
            st.write("Selected destination folder path:", destination_dir)
        return destination_dir

    @staticmethod
    def setup_folder_option() -> Optional[str]:
        """
        Sets up a select box for choosing a folder option in the Streamlit app.
        """
        return st.selectbox(
            "Choose the folder name for storing results:", ("train", "valid", "test")
        )

    @staticmethod
    def display_conversion_button() -> bool:
        """
        Displays a conversion button in the Streamlit app.
        """
        return st.button("Convert")
