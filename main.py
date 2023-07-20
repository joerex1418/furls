import re
import bs4
import json
import pathlib
import requests
from rich import print

root = pathlib.Path(__file__).parent

url = "https://furlscrochet.com/collections/current-odyssey-collection"

r = requests.get(url,verify=False)
soup = bs4.BeautifulSoup(r.text,"html.parser")

product_tags = soup.find("ul", attrs={"id": "main-collection-product-grid"})
script_tags: list[bs4.Tag] = product_tags.find_all("script")


products: list[dict] = []
for script_tag in script_tags:
    if "listProducts" in script_tag.text:
        jsonmatch = re.search(r"(?<=\"\]\=)(.*)", script_tag.text)
        if jsonmatch:
            jsonstring = jsonmatch.group().strip().strip(";").strip()
            jsonobject = json.loads(jsonstring)
            
            products.append(jsonobject)

with root.joinpath("jsonfile.json").open("w+") as fp:
    json.dump(products,fp,sort_keys=False)

for p in products:
    product_id = p["id"]
    product_title = p["title"]
    
    product_url = f"https://furlscrochet.com/products/{p['handle']}"
    
    product_price = str(p["price"])
    product_price = product_price[:-2] + "." + product_price[-2:]
    
    available = p["available"]
    status = "AVAILABLE" if available == True else "SOLD OUT"

    print(f"ID: {product_url}")
    print(f"Name: {product_title}")
    print(f"URL: {product_url}")
    print(f"Price: ${product_price}")
    print(f"Status: {status}")
    print()