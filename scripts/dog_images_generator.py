import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import tensorflow_datasets as tfds

load_dotenv()

def dog_images_download(breed_name, file_path, number=10):
    search_query = breed_name.replace('_', '+')
    search_url = f"https://www.google.com/search?q={search_query.replace('_', '+')}&udm=2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    images = soup.find_all("img", limit=number + 1)
    image_urls = []
    
    for img in images[1:number + 1]:
        url = img.get('data-src') or img.get('src')
        if url:
            image_urls.append(url)
    
    valid_extensions = ['jpg', 'jpeg', 'png']
    
    for i, url in enumerate(image_urls):
        try:
            # Follow the redirection to get the final image URL
            image_response = requests.get(url, headers=headers)
            if image_response.status_code == 200:
                content_type = image_response.headers['Content-Type']
                if content_type.split('/')[1] in valid_extensions:
                    image_extension = content_type.split('/')[1]
                    image_path = os.path.join(file_path, f"{breed_name}{i + 1}.{image_extension}")
                    with open(image_path, "wb") as f:
                        f.write(image_response.content)
                    print(f"Downloaded {image_path}")
                else:
                    print(f"Skipping invalid image URL: {url}")
            else:
                print(f"Failed to download image {i + 1} for {breed_name}: HTTP {image_response.status_code}")
        except Exception as e:
            print(f"Failed to download image {i + 1} for {breed_name}: {e}")
            
            
# Load dataste labels
dataset, info = tfds.load("stanford_dogs", with_info=True)
labels = info.features["label"].names
    
file_path=os.getenv("FILE_PATH")
    
    
# Iteration over all lables in stanford dogs dataset
for breed in labels:
    formatted_breed = "_".join(breed.split("-")[1:]).replace(" ", "_")
    # print(formatted_breed)
    # dog_images_download(formatted_breed, file_path)
    
    
def download_by_breed_name(breed_name):
    file_path = os.getenv("TEST")
    dog_images_download(breed_name, file_path, number=10)
    
download_by_breed_name("redbone_dog")