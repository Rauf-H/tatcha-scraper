import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    name: str
    description: str
    price: str

def scrape_tatcha_moisturizers():
    # URL of the moisturizers page
    url = "https://www.tatcha.co.uk/collections/moisturisers"
    
    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product containers
        products = []
        product_elements = soup.find_all('div', {'class': lambda x: x and 'product-card' in x})
        
        for product in product_elements:
            try:
                # Extract product name
                name = product.find('h2', {'class': 'product-card__title'}).text.strip()
                
                # Extract product description
                description = product.find('p', {'class': 'product-card__subtitle'}).text.strip()
                
                # Extract product price
                price = product.find('span', {'class': 'price'}).text.strip()
                
                # Create Product object and add to list
                products.append(Product(name=name, description=description, price=price))
                
            except AttributeError as e:
                print(f"Error extracting product details: {e}")
                continue
        
        return products
    
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def main():
    products = scrape_tatcha_moisturizers()
    
    print("\nTatcha Moisturizers:")
    print("-" * 50)
    
    for product in products:
        print(f"Name: {product.name}")
        print(f"Description: {product.description}")
        print(f"Price: {product.price}")
        print("-" * 50)

if __name__ == "__main__":
    main()
