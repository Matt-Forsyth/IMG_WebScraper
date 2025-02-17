import os
import requests
from bs4 import BeautifulSoup

def fetch_image_urls(query, max_images=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    image_urls = []
    page = 0
    
    while len(image_urls) < max_images:
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&start={page * 20}"
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            print("Failed to fetch images.")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        image_elements = soup.find_all("img")
        
        for img in image_elements:
            if "data-src" in img.attrs:
                image_urls.append(img["data-src"])
            elif "src" in img.attrs:
                image_urls.append(img["src"])
            if len(image_urls) >= max_images:
                break
        
        page += 1  # Move to next page if more images are needed
    
    return image_urls[:max_images]

def get_next_filename(base_folder):
    index_file = os.path.join(base_folder, "index.txt")
    os.makedirs(base_folder, exist_ok=True)
    
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            index = int(f.read().strip())
    else:
        index = 0
    
    return index, index_file

def download_images(image_urls):
    base_folder = "Scraped Content"
    start_index, index_file = get_next_filename(base_folder)
    
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                filename = f"{start_index + i}.png"
                with open(os.path.join(base_folder, filename), "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    
    # Update index file
    with open(index_file, "w") as f:
        f.write(str(start_index + len(image_urls)))

def main():
    query = input("Enter search query: ")
    max_images = int(input("Enter number of images to download: "))
    
    print("Fetching image URLs...")
    image_urls = fetch_image_urls(query, max_images)
    
    if not image_urls:
        print("No images found.")
        return
    
    print("Downloading images...")
    download_images(image_urls)
    print("Download complete.")

if __name__ == "__main__":
    main()  # Version 1 persistent indexing,scrapes images from google search(downloads thumbnails 😥 working on fix)
