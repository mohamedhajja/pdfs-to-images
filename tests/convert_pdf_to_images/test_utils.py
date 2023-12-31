"""
This module contains tests for the PDF to image conversion utilities.
"""
from unittest.mock import patch, MagicMock, Mock
import os
from pathlib import Path
from PIL import Image
from convert_pdf_to_images.utils import (
    convert_pdf_to_images,
    create_destination_folder,
    save_grayscale_image,
    process_pdf_files,
)


def test_create_destination_folder(tmp_path: Path) -> None:
    """testing create_destination_folder function

    Args:
        tmp_path (str): temp path to test creation of folders
    """
    # tmp_path is a pytest fixture that provides a temporary directory unique to the test invocation
    destination = tmp_path / "new_folder"

    # Ensure the directory does not exist
    assert not destination.exists()

    # Call the function to test
    create_destination_folder(str(destination))

    # Check if the new directory was created
    assert destination.exists()


def test_create_existing_destination_folder(tmp_path: Path) -> None:
    """
    Test the behavior of the create_destination_folder function when the directory already exists.

    Args:
        tmp_path (Path): A Path object representing a temporary directory provided by pytest, used here
                         to create a test directory environment without affecting the actual file system.

    The function asserts the existence of the directory before and after the function call, ensuring
    the correct behavior of 'create_destination_folder' with existing directories.
    """
    # Create a directory
    existing_destination = tmp_path / "existing_folder"
    existing_destination.mkdir()

    # Ensure the directory exists
    assert existing_destination.exists()

    # Call the function, which should not raise any exception
    create_destination_folder(str(existing_destination))

    # Check if the directory still exists
    assert existing_destination.exists()


def test_convert_pdf_to_images(tmp_path: Path) -> None:
    """
    Test the conversion of a PDF file to images using the convert_pdf_to_images function.

    Args:
        tmp_path (Path): A Path object representing a temporary directory provided by pytest. It's used
                         to create a dummy PDF file without affecting the actual file system.

    The test asserts the correct behavior of the 'convert_pdf_to_images' function, particularly in
    terms of its interaction with the mocked 'convert_from_path' function and the nature of its output.
    """
    # Setup a dummy PDF file
    dummy_pdf: Path = tmp_path / "dummy.pdf"
    dummy_pdf.write_text("This is a dummy PDF content")

    # Mock the convert_from_path function to return a list of mock images
    mock_image = MagicMock(spec=Image.Image)
    with patch(
        "convert_pdf_to_images.utils.convert_from_path", return_value=[mock_image]
    ) as mock_convert:
        # Call the function with the dummy PDF path
        result = convert_pdf_to_images(str(dummy_pdf))

        # Assert that the mock was called with the dummy PDF path
        mock_convert.assert_called_once_with(str(dummy_pdf))

        # Assert that the result is a list of images
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(img, Image.Image) for img in result)


def test_save_grayscale_image(tmp_path: Path) -> None:
    """
    Test the save_grayscale_image function to ensure it properly converts and saves an image in grayscale.

    Args:
        tmp_path (Path): A Path object provided by pytest, representing a temporary directory for
                         testing purposes. It ensures that the test does not affect the actual file
                         system and provides isolation.

    The test asserts the correct behavior of the 'save_grayscale_image' function, particularly its
    ability to handle image conversion and saving operations as expected.
    """
    # Create a mock image object with a spec from an actual Image object
    mock_image = Mock(spec=Image.Image)

    # Set up the destination directory and file name
    destination_dir = str(tmp_path)
    file_name = "grayscale_image.jpg"

    # Mock the 'convert' method on the mock image
    mock_image.convert.return_value = mock_image

    # Call the function with the mock image
    save_grayscale_image(mock_image, destination_dir, file_name)

    # Check that the image convert method was called with "L" to convert to grayscale
    mock_image.convert.assert_called_once_with("L")

    # Construct the full path where the image would be saved
    full_file_path = os.path.join(destination_dir, file_name)

    # Check that the save method was called with the correct parameters
    mock_image.save.assert_called_once_with(full_file_path, "JPEG")


def test_save_grayscale_image_actual_file(tmp_path: Path) -> None:
    # Create an actual image with PIL for testing
    test_image = Image.new("RGB", (10, 10), color="red")

    # Set up the destination directory and file name
    destination_dir = str(tmp_path)
    file_name = "grayscale_image.jpg"

    # Call the function with the actual image
    save_grayscale_image(test_image, destination_dir, file_name)

    # Check if the file was saved
    saved_image_path = tmp_path / file_name
    assert saved_image_path.is_file()

    # Check if the saved image is in grayscale
    with Image.open(saved_image_path) as saved_image:
        assert saved_image.mode == "L"


@patch("convert_pdf_to_images.utils.st")
@patch("convert_pdf_to_images.utils.save_grayscale_image")
@patch("convert_pdf_to_images.utils.convert_pdf_to_images")
@patch("convert_pdf_to_images.utils.os.listdir")
@patch("convert_pdf_to_images.utils.create_destination_folder")
def test_process_pdf_files(
    mock_create_destination_folder: MagicMock,
    mock_listdir: MagicMock,
    mock_convert_pdf_to_images: MagicMock,
    mock_save_grayscale_image: MagicMock,
    mock_st: MagicMock,
    tmp_path: Path,
) -> None:
    """
    Test the processing of PDF files into grayscale images.

    Args:
        mock_create_destination_folder (MagicMock): A mock for the 'create_destination_folder' function.
        mock_listdir (MagicMock): A mock for the 'os.listdir' function to list files in a directory.
        mock_convert_pdf_to_images (MagicMock): A mock for the 'convert_pdf_to_images' function.
        mock_save_grayscale_image (MagicMock): A mock for the 'save_grayscale_image' function.
        mock_st (MagicMock): A mock for streamlit components, used for displaying progress and success messages.
        tmp_path (Path): A Path object representing a temporary directory provided by pytest.
    """
    # Setup the directory structure and dummy files
    root_dir: Path = tmp_path / "root_dir"
    root_dir.mkdir()
    destination_dir: Path = tmp_path / "destination_dir"
    destination_dir.mkdir()
    dummy_pdf: Path = root_dir / "dummy.pdf"
    dummy_pdf.write_text("This is a dummy PDF content")

    # Setup mocks
    mock_listdir.return_value = [dummy_pdf.name]
    mock_image: MagicMock = MagicMock(spec=Image.Image)
    mock_convert_pdf_to_images.return_value = [mock_image]
    progress_bar: MagicMock = MagicMock()
    mock_st.progress.return_value = progress_bar

    # Call the function
    process_pdf_files(str(root_dir), str(destination_dir), "output_folder")

    # Verify
    mock_create_destination_folder.assert_called_once_with(str(destination_dir))
    assert mock_listdir.call_count == 2, "os.listdir should be called twice"
    mock_convert_pdf_to_images.assert_called_once_with(str(dummy_pdf))
    mock_save_grayscale_image.assert_called()
    assert mock_save_grayscale_image.call_count == len(
        mock_convert_pdf_to_images.return_value
    )
    progress_bar.progress.assert_called()
    mock_st.success.assert_called_once_with("Conversion Completed!")

    # Check log file creation and content
    log_file_path: Path = destination_dir / "output_folder_name_changes_log.txt"
    assert log_file_path.exists()
    with open(log_file_path, "r", encoding="utf-8") as log_file:
        log_content: str = log_file.read()
        assert "dummy.pdf ==> output_folder_1\n" in log_content
