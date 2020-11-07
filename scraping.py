from random import random

from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import urllib

def downloadFile(id, soup):
    soup2 = soup.find("div", class_="m-slider")
    image = "https:" + soup2.find('img').get('src')
    imagefile = open("images/"+str(id) + ".jpeg", 'wb')
    imagefile.write(urllib.request.urlopen(image).read())
    imagefile.close()

def main():


    #nazwa,opis, zdjęcie, atrybuty kategorie: DVD Blueray: podkategorie: akcji, przygodowe itp

    categories = ["filmy-dvd", "filmy-blu-ray"]
    subcategories = ["animowanefamilijne", "dokumentalne", "dramat", "fantasysci-fi","horrorthriller",
                     "komediakomedia-romantyczna", "muzycznemusicale", "sensacyjneprzygodowe"]
    subcategories_name = ["Animowane/Familijne", "Dokumentalne", "Dramat", "Fantasy/Sci-Fi", "Horror/Thriller",
                          "Komedia/Komedia Romantyczna", "Muzyczne/Musicale", "Sensacyjne/Przygodowe"]
    id = 1


    # Zapis do pliku
    with open('products.csv', mode='w', encoding="UTF8", newline='') as csvfile:
        fieldnames = ["Product ID", "Active (0/1)", "Name *", "Categories (x,y,z...)", "Price tax excluded", "Tax rules ID", "Wholesale price", "On sale (0/1)", "Discount amount", "Discount percent", "Discount from (yyyy-mm-dd)", "Discount to (yyyy-mm-dd)", "Reference #", "Supplier reference #", "Supplier", "Manufacturer", "EAN13", "UPC", "Ecotax", "Width", "Height", "Depth", "Weight", "Delivery time of in-stock products", "Delivery time of out-of-stock products with allowed orders", "Quantity", "Minimal quantity", "Low stock level", "Send me an email", "Visibility", "Additional shipping cost", "Unity", "Unit price", "Summary", "Description", "Tags (x,y,z...)", "Meta title", "Meta keywords", "Meta description", "URL rewritten", "Text when in stock", "Text when backorder allowed", "Available for order (0 = No, 1 = Yes)", "Product available date", "Product creation date", "Show price (0 = No, 1 = Yes)", "Image URLs (x,y,z...)", "Image alt texts (x,y,z...)", "Delete existing images(0 = No, 1 = Yes)", "Feature(Name: Value: Position)", "Available online only(0 = No, 1 = Yes)", "Condition", "Customizable(0 = No, 1 = Yes)", "Uploadable files (0 = No, 1 = Yes)", "Text fields (0 = No, 1 = Yes)", "Out of stock action", "Virtual product", "File URL", "Number of allowed downloads", "Expiration date", "Number of days", "ID / Name of shop", "Advanced stock management", "Depends On Stock", "Warehouse", "Acessories(x, y, z...)"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for i, category in enumerate(categories):
            for j, subcategory in enumerate(subcategories):
                a=0
                #Pobierz html
                response = requests.get("https://mediamarkt.pl/filmy/"+category+"/"+subcategory)
                #Sparsuj kod źródłowy
                soup = BeautifulSoup(response.text, 'html.parser')
                # Szukaj produkty
                for product in soup.find_all("div", class_="m-productsBox_photo js-productsBox_photo g-posr"):

                    url = product.find('a', href=True)

                    # Przejdz na strone produktu
                    response_2 = requests.get("https://mediamarkt.pl" + url['href'])

                    soup2 = BeautifulSoup(response_2.text, 'html.parser')

                    name = soup2.find("h1", class_="m-typo m-typo_primary").text.replace('\n', '').replace('  ', '')
                    specifications = soup2.find_all("dd", class_="m-offerShowData_param js-offerShowData_row")
                    #author = specifications[3].text.replace('\n', '')
                    categories = specifications[2].text.replace('\n', '').replace('  ', '')
                    price = soup2.find("div", itemprop=price).replace(',', 'x')
                    #price = soup2.find("div", class_="m-productAction_btn").find("a")["data-price"]
                    quantity = int(random()*1000)



                    description = soup2.find("div", class_="widget text_editor")
                    if description is None:
                        description = soup2.find("span", itemprop="description")
                        if description is None:
                            description = "Description"
                        else:
                            description = description.text
                    else:
                        description = description.text

                    #downloadFile(id, soup2)

                    writer.writerow({'Product ID': id,
                                     "Active (0/1)": 1,
                                     'Name *': name,
                                     'Categories (x,y,z...)': i*8+j+1003,
                                     'Price tax excluded': str(float(price)/1.23),
                                     'Tax rules ID': 1,
                                     'Wholesale price': float(price)*0.9,
                                     'On sale (0/1)': 1,
                                     'Discount percent': 0, #punkt 12
                                     'Discount from (yyyy-mm-dd)': '2020-11-02',#punkt 12
                                     'Discount to (yyyy-mm-dd)': '2020-11-07',#punkt 12
                                     'Reference #': 'demo_'+str(id),
                                     'Supplier reference #': 'demo_'+str(id),#punkt 13
                                     'Supplier': "",#punkt 13
                                     'Quantity': quantity,
                                     'Minimal quantity': 1,
                                     'Send me an email': 0,
                                     'Visibility': 'both',
                                     'Additional shipping cost': '',#punkt 13
                                     'Description': description,
                                     'URL rewritten': url['href'].split("/")[-1],#replace/
                                     'Text when in stock': "Produkt dostępny",
                                     'Text when backorder allowed': "Zamówienie dozwolone",
                                     'Available for order (0 = No, 1 = Yes)': 1,
                                     'Show price (0 = No, 1 = Yes)': 1,
                                     'Feature(Name: Value: Position)': "Name: Value: Position",
                                     'Available online only(0 = No, 1 = Yes)': 0,
                                     'Condition': "new",
                                     'Acessories(x, y, z...)': "x, y, z",
                                     'Delete existing images(0 = No, 1 = Yes)': 1,
                                     'Customizable(0 = No, 1 = Yes)': 1,
                                     })
                    id = id + 1
                    a = a + 1
                    print(a)
                    if a > 0:
                        break






if __name__ == "__main__":
    main()
