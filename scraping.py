from bs4 import BeautifulSoup
import requests
import csv
import urllib


def downloadFile(id, soup):
    soup2 = soup.find("div", class_="m-slider")
    image = "https:" + soup2.find('img').get('src')
    imagefile = open("images/" + str(id) + ".jpeg", 'wb')
    imagefile.write(urllib.request.urlopen(image).read())
    imagefile.close()


def createProductsFile():
    categories = ["filmy-dvd", "filmy-blu-ray"]
    subcategories = ["animowanefamilijne", "dokumentalne", "dramat", "fantasysci-fi", "horrorthriller",
                     "komediakomedia-romantyczna", "muzycznemusicale", "sensacyjneprzygodowe"]
    id = 1

    # Zapis do pliku
    with open('products.csv', mode='w', encoding="utf8", newline='') as csvfile:
        fieldnames = ["Product ID", "Active (0/1)", "Name *", "Categories (x,y,z...)", "Price tax excluded",
                      "Tax rules ID", "Wholesale price", "On sale (0/1)", "Discount amount", "Discount percent",
                      "Discount from (yyyy-mm-dd)", "Discount to (yyyy-mm-dd)", "Reference #", "Supplier reference #",
                      "Supplier", "Manufacturer", "EAN13", "UPC", "Ecotax", "Width", "Height", "Depth", "Weight",
                      "Delivery time of in-stock products",
                      "Delivery time of out-of-stock products with allowed orders", "Quantity", "Minimal quantity",
                      "Low stock level", "Send me an email", "Visibility", "Additional shipping cost", "Unity",
                      "Unit price", "Summary", "Description", "Tags (x,y,z...)", "Meta title", "Meta keywords",
                      "Meta description", "URL rewritten", "Text when in stock", "Text when backorder allowed",
                      "Available for order (0 = No, 1 = Yes)", "Product available date", "Product creation date",
                      "Show price (0 = No, 1 = Yes)", "Image URLs (x,y,z...)", "Image alt texts (x,y,z...)",
                      "Delete existing images(0 = No, 1 = Yes)", "Feature(Name: Value: Position)",
                      "Available online only(0 = No, 1 = Yes)", "Condition", "Customizable(0 = No, 1 = Yes)",
                      "Uploadable files (0 = No, 1 = Yes)", "Text fields (0 = No, 1 = Yes)", "Out of stock action",
                      "Virtual product", "File URL", "Number of allowed downloads", "Expiration date", "Number of days",
                      "ID / Name of shop", "Advanced stock management", "Depends On Stock", "Warehouse",
                      "Acessories(x, y, z...)"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for i, category in enumerate(categories):
            for j, subcategory in enumerate(subcategories):
                a = 0
                # Pobierz html
                response = requests.get("https://mediamarkt.pl/filmy/" + category + "/" + subcategory)

                # Sparsuj kod źródłowy
                soup = BeautifulSoup(response.text, 'html.parser')
                # Szukaj produkty
                for product in soup.find_all("div", class_="m-offerBox_box"):

                    url = product.find('a', href=True)

                    # Przejdz na strone produktu
                    response_2 = requests.get("https://mediamarkt.pl" + url['href'])

                    soup2 = BeautifulSoup(response_2.text, 'html.parser')

                    name = soup2.find("h1", class_="b-ofr_headDataTitle").text.replace('\n', '').replace('  ', '')
                    specifications_names = soup2.find_all("dt", class_="m-offerShowData_name js-offerShowData_row")
                    specifications_params = soup2.find_all("dd", class_="m-offerShowData_param js-offerShowData_row")
                    features = ""
                    for k in range(len(specifications_names)):
                        # print(specifications_names[k].text.replace('\n', ''))
                        if specifications_names[k].text.replace('\n', '') == "Producent":
                            features += "Producent:" + specifications_params[k].text.replace('\n', '') + ":" + str(
                                k) + ","
                        elif specifications_names[k].text.replace('\n', '') == "Reżyseria":
                            features += "Reżyseria:" + specifications_params[k].text.replace('\n', ' ') + ":" + str(
                                k) + ","
                        elif specifications_names[k].text.replace('\n', '') == "Czas trwania [min]":
                            features += "Czas trwania [min]:" + specifications_params[k].text.replace('\n',
                                                                                                      '') + ":" + str(
                                k) + ","
                        elif specifications_names[k].text.replace('\n', '') == "Kraj produkcji":
                            features += "Kraj Produkcji:" + specifications_params[k].text.replace('\n', '').split(",")[
                                0] + ":" + str(k) + ","
                        elif specifications_names[k].text.replace('\n', '') == "Rok produkcji":
                            features += "Rok Produkcji:" + specifications_params[k].text.replace('\n', '') + ":" + str(
                                k) + ","

                    price = soup2.find("div", class_="b-ofrBox_cta").find("a")["data-offer-price-net"]

                    description = soup2.find("div", class_="widget text_editor")
                    if description is None:
                        description = soup2.find("span", itemprop="description")
                        if description is None:
                            description = "Description"
                        else:
                            description = description.text
                    else:
                        description = description.text

                    downloadFile(id, soup2)

                    writer.writerow({'Product ID': id,
                                     "Active (0/1)": 1,
                                     'Name *': name,
                                     'Categories (x,y,z...)': str(i * 8 + j + 1003) + "," + str(
                                         1000 + i + 1) + "," + str(1000),
                                     'Price tax excluded': str(price),  # str(round(float(price)/1.23, 2)),
                                     'Tax rules ID': 1,
                                     'Wholesale price': round((float(price) / 1.23) * 0.9, 2),
                                     'On sale (0/1)': 0,
                                     'Reference #': 'demo_' + str(id),
                                     'Supplier reference #': 'demo_' + str(id),  # punkt 13
                                     'Supplier': "",  # punkt 13
                                     'Minimal quantity': 1,
                                     'Send me an email': 0,
                                     'Visibility': 'both',
                                     'Additional shipping cost': '',  # punkt 13
                                     'Summary': 'Film',
                                     'Description': description,
                                     'URL rewritten': url['href'].split("/")[-1],  # replace/
                                     'Text when in stock': "Produkt dostępny",
                                     'Text when backorder allowed': "Zamówienie dozwolone",
                                     'Available for order (0 = No, 1 = Yes)': 1,
                                     'Show price (0 = No, 1 = Yes)': 1,
                                     'Feature(Name: Value: Position)': features,
                                     'Available online only(0 = No, 1 = Yes)': 0,
                                     'Condition': "new",
                                     'Delete existing images(0 = No, 1 = Yes)': 1,
                                     'Customizable(0 = No, 1 = Yes)': 1,
                                     })
                    id += 1
                    a += 1
                    print(id)
                    if a > 3:
                        break


def main():
    createProductsFile()


if __name__ == "__main__":
    main()
