# Menu Finder 
Leverages the OCR Engine and the Resource Scraper to provide OCR menu data given a website URL.

If PDFs contain menu data no images will be scanned. If multiple PDFs contain menu data they will be combined. Default is a depth of 5 for menu's searched and depth of 5 images.

Not multithreaded at this point.

## Sample usage
```
curl http://menu-crawler.herokuapp.com/menu_for_url?url=https://firehousepb.com/ 
```
### output
```
{
  "page_count": 7,
  "pages": [
    {
      "image_raw": base64EncodedJPG,
      "text": "Grilled or Crispy Buffalo Chicken, Romaine, Caesar\nDressing, Parmesan, Crushed Croutons, Duck Fat..."
    },
    ...
  ]
}
```

##requirements
```
sudo apt-get update
sudo apt-get -y install python3-pip
pip3 install beautifulsoup4 flask flask_cors waitress 
```
