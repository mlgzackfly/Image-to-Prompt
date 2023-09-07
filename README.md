# Image to Prompt

This Django project is designed to allow users to upload AI-generated images and then provide text prompts that could have led to the image's creation.

## Project Structure

The project structure consists of the following main folders and files:

- `media`: This directory is used to temporarily store uploaded user images.
- `reversal`: This directory contains the main Django app.
- `reversal/model`: This folder contains the machine learning models used for generating image embeddings.
- `reversal/db.csv`: This file contains the dataset used for comparing image embeddings to find text prompts.
- `reversal/similarity.py`: This script is used to divide uploaded images into 384 embedded vectors.
- `static`: This directory contains static files such as images and JavaScript.
- `template/reversal`: This folder contains the main HTML templates for the web application.

## Setup

To set up this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` in the project root directory.
3. Run `python manage.py migrate` to set up the database.
4. Start the development server using `python manage.py runserver`.
5. Navigate to `http://localhost:8000` in your web browser to view the application.

## Usage

Once the application is running, users can upload an AI-generated image and the application will generate 384 embedded vectors for the image. The application will then compare the embedded vectors to the dataset in db.csv to find the most similar text prompts. These prompts will be displayed to the user on the web page.

## Credits

This project was created by Marco. It uses the following open-source libraries:

- Django
- TensorFlow
- NumPy
- Pandas