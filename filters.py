import requests
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import matplotlib.colors as mcolors

filters = {
    "Lee": {},
    "Rosco": {}
}

# ------------ Lee ------------

url_lee = "https://leefilters.com/lighting/colour-effect-lighting-filters/"
response = requests.get(url_lee)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

for colour_item in soup.select(".colours-list__colour"):
    # Référence
    reference = colour_item.find("span").text.strip()
    
    # Hexadécimale
    colour_style = colour_item['style']
    hex_color = colour_style.split('#')[-1][:6]
    
    filters["Lee"][reference] = f"#{hex_color}"

print("Données des filtres LEE extraites.")

# ------------ Rosco ------------

driver = webdriver.Chrome()
url_rosco = "https://emea.rosco.com/fr/products/catalog/supergel"
driver.get(url_rosco)

input("Cliquez sur 'Display All Items' manuellement, puis appuyez sur Entrée pour continuer...")

time.sleep(2)

filter_elements = driver.find_elements(By.CSS_SELECTOR, ".product-roscolux")
for colour_item in filter_elements:
    # Référence
    reference_text = colour_item.find_element(By.CSS_SELECTOR, ".desc p a").text.strip()
    reference_number = re.sub(r"^R(\d+).*", r"\1", reference_text).zfill(3)

    # Hexadécimal
    color_span = colour_item.find_element(By.CSS_SELECTOR, ".image a span[style*='background']")
    rgba_color = color_span.value_of_css_property("background-color")

    rgba_values = re.findall(r"\d+", rgba_color)
    if len(rgba_values) >= 3:
        r, g, b = map(int, rgba_values[:3])
        hex_color = mcolors.to_hex((r/255, g/255, b/255))
        
        filters["Rosco"][reference_number] = hex_color

print("Données des filtres Rosco extraites.")

with open('filters.json', 'w') as json_file:
    json.dump(filters, json_file, indent=4)

print("Données extraites et sauvegardées dans 'filters.json'")

driver.quit()
