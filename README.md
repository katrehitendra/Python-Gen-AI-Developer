# Python-Gen-AI-Developer

## Citation Extractor
This Flask application fetches data from a paginated API, identifies response sources, and returns citations based on cosine similarity. It preprocesses the input text, tokenizes it, removes stop words, and calculates the similarity between the response and source texts.

## Installation
Clone this repository to your local machine:
git clone (https://github.com/katrehitendra/Python-Gen-AI-Developer.git)

## Install the required Python packages:
pip install flask nltk requests

## Run the Flask app:
python app.py

## Usage
Access the app in your browser at http://127.0.0.1:5000/.
Enter the input text and submit the form.
The app will fetch data from the API, process it, and display the citations.

## Files
app.py: The main Flask application.
templates/index.html: HTML template for the input form.
templates/results.html: HTML template to display the citations.
## API Endpoint
The app uses the following API endpoint for fetching data:

Base URL: https://devapi.beyondchats.com/api/get_message_with_sources

## Adjusting Threshold
cosine similarity threshold (currently set to 0.7) can be adjusted in the get_citations function to control the confidence level for matching sources.
