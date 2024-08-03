# Image Segregation Tool Using Feature Comparison (ISTFC)

## Introduction

The Image Segregation Tool Using Feature Comparison (ISTFC) is a powerful application designed to help users upload and segregate images based on feature comparison. This tool allows users to upload a batch of images, receive a unique URL for access, and use a single portrait to find and download all images containing the queried individual.

## Features

- **Upload Images**: Upload a folder of images for processing.
- **Unique URL**: Receive a unique URL to access and share your uploaded images.
- **Query by Image**: Use a single image to find all matched images.
- **Download Matched Images**: Easily download all matched images with a single click.

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.6 or higher
- `pip` (Python package installer)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ISTFC.git
cd ISTFC
```

### Step 2: Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Download and Install System Dependencies
 - For Ubuntu/Debian-based Systems:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libboost-all-dev
sudo apt-get install python3-dev
```
 - For macOS:

```bash
xcode-select --install
```
 - For Windows:

Install Visual Studio Build Tools from Visual Studio website.
### Step 5: Run the Application
```bash
flask run
```
The application will be accessible at http://127.0.0.1:5000/.

Accessing the Application on a Mobile Device
To access the application on your mobile device, ensure your mobile device is connected to the same network as your local machine. Find your local machine's IP address and run the Flask application with it:

```bash
flask run --host=0.0.0.0
```
Now you can access the application from your mobile device by navigating to http://<your-local-machine-ip>:5000/.

## Usage
1. Open the application in your web browser.
2. Upload a folder containing your images.
3. Receive a unique URL to access the uploaded images.
4. Use a query image to find all matching images.
5. Download the matched images with a single click.