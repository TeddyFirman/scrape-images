from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import  Image
import time

PATH = "E:\\Bangkit\\Capstone\\Scrape\\chromedriver.exe"

webDriver = webdriver.Chrome(PATH)

def get_image(webDriver, delay, max_image):
    def scroll_down(webDriver):
        webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=watermelon+fresh&tbm=isch&ved=2ahUKEwjJuqTlndr3AhWFNLcAHXJKBsAQ2-cCegQIABAA&oq=watermelon+fresh&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBggAEAUQHjIGCAAQBRAeOgYIABAIEB5Q9yVYyDVgsjdoAHAAeAGAAdMCiAHREpIBBzMuNC4xLjSYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=xyF9Yom7CYXp3LUP8pSZgAw#imgrc=7dQMg9WuT216lM"
    webDriver.get(url)

    image_urls = set()
    skips = 0
    while len(image_urls) + skips < max_image:
        scroll_down(webDriver)

        thumbnails = webDriver.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_image]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = webDriver.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb")  as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print("Failed", e)

urls = get_image(webDriver, 1, 10)
for i, url in enumerate(urls):
    download_image("Dataset/", url, str(i) + ".jpg")
webDriver.quit()