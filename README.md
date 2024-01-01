# Converting PDFs to Images Streamlit Application
![Capture d'écran 2024-01-01 140800](https://github.com/mohamedhajja/pdfs-to-images/assets/106828911/54af513e-5a66-4f74-8899-05a035519ffc)

## Overview

This is a Streamlit app that can convert multiple PDFs to grayscale images all at once.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or later
- Pip (Python package installer)

### Install Poetry

Poetry is used for dependency management and packaging.

```bash
pip install poetry
```

### External Dependencies
This application requires pdf2image, which in turn depends on the Poppler utilities. Follow these steps to install Poppler:

#### Windows
Download the latest binary of Poppler from https://poppler.freedesktop.org/.
Extract the downloaded files.
Add the bin directory from the extracted folder to your system's PATH environment variable.

#### Linux 
Install Poppler using apt:
```bash
sudo apt-get install poppler-utils
```

### Setup

After cloning the project, follow these steps:

#### Install Dependencies
Navigate to the project directory and run:

```bash
poetry install
```

Activate the Virtual Environment:

```bash
poetry shell
```

## Testing

Ensure your application runs correctly by performing tests:

- Unit Tests Using Pytest
```bash
pytest tests
```

- Test Coverage
```bash
pytest --cov=convert_pdf_to_images
```

- Test Coverage Report

Generate an HTML coverage report:

```bash
pytest --cov=convert_pdf_to_images --cov-report=html
```

