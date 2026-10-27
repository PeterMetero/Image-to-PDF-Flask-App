# Image to PDF Flask App

A simple Flask web application that lets users upload multiple images, reorder them with drag-and-drop, and convert them into a single PDF file.

## Features

- Upload up to 30 images at a time
- Accepts PNG, JPG, and JPEG files
- Rearrange images before conversion
- Converts uploaded images into a PDF document
- Downloads the generated PDF
- Stores conversion metadata in SQLite using Flask-SQLAlchemy

## Tech Stack

- Python
- Flask
- Pillow
- Flask-SQLAlchemy
- SQLite
- HTML, CSS, JavaScript

## Project Structure

```text
Image to PDF Flask App/
├── app.py
├── README.md
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── uploads/
├── outputs/
├── tests/
│   └── test_app.py
└── instance/
```

## Requirements

Install the dependencies from the requirements file:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root, start the app:

```bash
python app.py
```

Then open the app in your browser:

```text
http://127.0.0.1:5000
```

## How it Works

1. The user uploads image files from the browser.
2. The app validates the file types.
3. Uploaded images are saved temporarily.
4. The user can drag and drop thumbnails to set the PDF page order.
5. The app combines the images into a PDF using Pillow.
6. The generated PDF is available for download.
7. Conversion details are stored in the SQLite database.

## Environment Notes

- The app creates the `uploads` and `outputs` folders automatically if they do not exist.
- The database file is stored as `conversions.db` in the project directory.
- The app runs in debug mode when started via `python app.py`.

## License

This project is for educational and personal use.
