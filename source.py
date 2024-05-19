import requests
import re
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# remove urls from text
def extract_urls(text):
    # Define a regular expression pattern to match URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\\\(\\\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Use re.findall() to extract all URLs from the input string
    urls = re.findall(url_pattern, text)
    return urls

def preprocess_text(text, stemmer, stop_words):
  # Tokenize, lowercase, remove stop words, and stem
  for url in extract_urls(text):
    text.replace(url,"")
  tokens = [stemmer.stem(w.lower()) for w in nltk.word_tokenize(text) if w not in stop_words]
  return " ".join(tokens)

def get_citations(api_url):
  """
  Fetches data from paginated API, identifies response sources, and returns citations.

  Args:
      api_url (str): Base URL of the paginated API.

  Returns:
      list: List of dictionaries containing citations for each response-sources pair.
  """
  citations = []
  url = api_url
  while url:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-200 status codes
    data = response.json()
    
    for item in data["data"]["data"]:
      responses = item["response"]
      sources = item["source"]
      stemmer = PorterStemmer()
      stop_words = stopwords.words('english')
      matched_sources = []

      # Preprocess response and source text (using NLP libraries)
      response_text = preprocess_text(responses, stemmer, stop_words)
      source_contexts = [preprocess_text(source["context"], stemmer, stop_words) for source in sources]

        # TF-IDF vectorization
      vectorizer = TfidfVectorizer()
      response_vector = vectorizer.fit_transform([response_text])
      source_vector = vectorizer.transform(source_contexts)

      # Calculate the cosine similarity 
      
      for i,source in enumerate(sources):
        cos_similarity = cosine_similarity(response_vector, source_vector[i])
        if cos_similarity > 0.7:  # Adjust threshold for desired confidence
          matched_sources.append({"id": source["id"], "link": extract_urls(source['context'])}) 
      citations.append({"response":responses,"citations": matched_sources})
    
    url = data.get("next")  # Get URL for next page if available

  return citations


if __name__ == "__main__":
# Example usage
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    citations = get_citations(api_url)

    # Print the citations for each response-sources pair
    for item in citations:
        print(f"Response: {item['response']}")
        print(f"Citations: {item['citations']}")
        print("---")
