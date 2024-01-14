import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_images(url, save_path, delay=1):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
    except requests.exceptions.RequestException as e:
        print(f"Error while requesting URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for i, img in enumerate(img_tags, start=1):
        img_url = img.get("src")
        if img_url:
            img_url = urljoin(url, img_url)  # Handles both relative and absolute URLs
            try:
                img_response = requests.get(img_url, stream=True)
                img_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image from {img_url}: {e}")
                continue

            # Determine file extension based on the Content-Type
            content_type = img_response.headers["content-type"]
            if content_type == "image/jpeg":
                file_extension = "jpg"
            elif content_type == "image/png":
                file_extension = "png"
            elif content_type == "image/gif":
                file_extension = "gif"
            else:
                print(f"Unsupported image type: {content_type}")
                continue

            file_name = f"image_{i}.{file_extension}"
            with open(os.path.join(save_path, file_name), "wb") as out_file:
                for chunk in img_response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            time.sleep(delay)  # Delay in seconds


# Usage
URL = "https://frameset.app/stills?search=Chris+Cunningham"
SAVE_PATH = "C:\\Users\\diego\\Desktop\\frameset"
DELAY = 1
download_images(URL, SAVE_PATH, DELAY)
