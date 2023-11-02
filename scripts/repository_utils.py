import requests
from bs4 import BeautifulSoup

def fetch_huggingface_files(base_url, repo_path, file_extensions):
    """
    Fetches file names from the Hugging Face repository and returns a dictionary
    mapping file names to their URLs.
    
    Parameters:
        base_url (str): The base URL of the Hugging Face repository.
        repo_path (str): The path to the repository on Hugging Face.
        file_extensions (list): List of file extensions to search for.
    
    Returns:
        dict: A dictionary mapping file names to their URLs.
    """
    url = f'{base_url}/{repo_path}/tree/main'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all li elements containing a span, check if it's a file, and get the href
    files = {}
    for li in soup.find_all('li'):
        for span in li.find_all('span'):
            text = span.text
            if any(ext in text for ext in file_extensions):
                file_url = f'{base_url}/{repo_path}/resolve/main/{text}'
                files[text] = file_url
                
    return files

base_url = 'https://huggingface.co'
repo_path = 'lllyasviel/sd_control_collection'
file_extensions = ['.pth', 'safetensors', 'yaml']

SD_CONTROL_COLLECTION = fetch_huggingface_files(base_url, repo_path, file_extensions)
