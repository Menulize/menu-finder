import json
import requests

import pdb

from flask import Flask, request 
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

resource_scraper_host = 'https://resource-scraper.herokuapp.com/'
ocr_host = 'https://ocr.gallodigital.com/'

@app.route("/check")
def check():
    return json.dumps({})

def ocr_pdf(url, dpi=200):
    # Step 1: Download the PDF
    pdf_content = requests.get(url).content
    # Step 2: OCR the PDF
    response = requests.post(ocr_host + "pdf_to_text", data=pdf_content, params={ "dpi": dpi, "jpgs": True }) 
    return response.json()['pages']

def ocr_image(url, dpi=200):
    # Step 1: Download the PDF
    image_content = requests.get(url).content
    # Step 2: OCR the PDF
    response = requests.post(ocr_host + "img_to_text", data=image_content, params={ "dpi": dpi }) 
    return response.json()['pages']

def is_menu_page(text):
    menu_words = ['menu', 'lunch', 'dinner', 'breakfast', 'drinks', 'surcharge', 
        'cheese', 'salad', 'burger', 'curry', 'vegan', 'onion', 'soup', 'dessert',
        'beer', 'wine']

    for word in menu_words:
        if word in text.lower():
            return True
    return False

@app.route("/menu_for_url", methods = ['GET'])
def menu_for_url():
    url = request.args.get("url") 
    dpi = request.args.get("dpi", default=200) 
    max_crawl_depth = request.args.get("max_crawl_depth", default=2)
    max_image_limit = request.args.get("max_image_limit", default=5)
    max_pdf_limit = request.args.get("max_image_limit", default=5)

    response = requests.get(resource_scraper_host + "get_resources", params={ "url": url }) 
    resource_urls = response.json()
    
    # 1st OCR menu pdfs
    menu_pages = []
    for pdf_url in resource_urls['pdf_urls'][:max_pdf_limit]:
        pages = ocr_pdf(pdf_url)
        if len(list(filter(lambda page: is_menu_page(page['text']), pages))) > 0:
            menu_pages.append(pages)

    if len(menu_pages) == 0:
        # If we have an image with the word menu in it then we have succeeded, else we OCR all the images we found...
        for image_url in resource_urls["img_urls"][:max_image_limit]:
            pages = ocr_image(image_url)
            if len(list(filter(lambda page: is_menu_page(page['text']), pages))) > 0:
                menu_pages.append(pages)
    
    return json.dumps({ "page_count": len(menu_pages), "pages": menu_pages })

if __name__ == "__main__":
    app.run(port=8080)
