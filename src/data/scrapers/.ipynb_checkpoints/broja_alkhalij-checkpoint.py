import requests
from bs4 import BeautifulSoup
import time

response = requests.get("https://brojalkhalij.com/en/collections/men/products/sauvage-elixir?   variant=53027064611136")
soup = BeautifulSoup(response.text, "html.parser")

print("Collection Status Code:", response.status_code)

notes = {}
body = soup.body
print(body.prettify())