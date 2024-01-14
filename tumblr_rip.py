import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename

def get_image_urls(blog_url, page_num):
    url = f"{blog_url}/page/{page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Extract the 'src' attribute from each image ta-g
    img_urls = [img['src'] for img in img_tags]

    return img_urls

def download_image(url, folder):
    # Send a GET request to the image URL
    response = requests.get(url)

    # The name of the image file will be the last part of the URL
    filename = url.split("/")[-1]

    # Sanitize the filename
    filename = sanitize_filename(filename)

    # Create the output folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Write the content of the response to a file in the output folder
    with open(os.path.join(folder, filename), 'wb') as file:
        file.write(response.content)

def main():
    blog_url = "https://worldstarhockey.tumblr.com"
    output_folder = "G:\\My Drive\\dataset-footage\\shamoncassette\\tumblr"
    page_num = 1

    while True:
        print(f"Scraping page {page_num}")
        img_urls = get_image_urls(blog_url, page_num)

        # If no image URLs were found on this page, we've reached the end of the blog
        if not img_urls:
            break

        # Download each image
        for url in img_urls:
            print(f"Downloading {url}")
            download_image(url, output_folder)

        # Go to the next page
        page_num += 1

if __name__ == "__main__":
    main()
