from bs4 import BeautifulSoup
import requests
import csv
import urllib
import pandas as pd


def download_file(id, soup):
    soup2 = soup.find("div", class_="m-slider")
    image = "https:" + soup2.find('img').get('src')
    try:
        image_file = open("images/" + str(id) + ".jpeg", 'wb')
        image_file.write(urllib.request.urlopen(image).read())
        image_file.close()
    except:
        print("urllib error")


def delete_duplicates():
    data = pd.read_csv('products.csv', sep=';', header=0, encoding='utf8', engine='python')
    data.sort_values("Name", inplace=True)
    data.drop_duplicates(subset="Name", keep="first", inplace=True)
    data.to_csv('products.csv', sep=';', index=False)


def create_products_file():

    categories = ["filmy-dvd", "filmy-blu-ray"]
    subcategories = ["animowanefamilijne", "dokumentalne", "dramat", "fantasysci-fi", "horrorthriller",
                     "komediakomedia-romantyczna", "muzycznemusicale", "sensacyjneprzygodowe"]
    subsubcategories_names = [["Animowany", "Familijny"], ["Dokumentalny", ""], ["Dramat", ""],
                              ["Fantasy", "Sciencefiction"],
                              ["Horror", "Thriller"], ["Komedia", "Romans"], ["Muzyczny", "Musical"],
                              ["Sensacja", "Przygodowy"]]
    id = 1

    # Save to file
    with open('products.csv', mode='w', encoding="utf8", newline='') as csvfile:
        fieldnames = ["Id", "Name", "Link", "Categories", "Price", "Wholesale price", "Features", "Description"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for i, category in enumerate(categories):
            for j, subcategory in enumerate(subcategories):
                a = 0
                # Download html
                response = requests.get(
                    "https://mediamarkt.pl/filmy/" + category + "/" + subcategory + "?sort=0&limit=100&page=1")

                # Parse html
                soup = BeautifulSoup(response.text, 'html.parser')

                # Search for products
                for product in soup.find_all("div", class_="m-offerBox_box"):

                    url = product.find('a', href=True)

                    # Go to the product page
                    response_2 = requests.get("https://mediamarkt.pl" + url['href'])

                    # Parse html
                    soup2 = BeautifulSoup(response_2.text.replace("<br>", "\n"), 'html.parser')

                    # Name
                    name = soup2.find("h1", class_="b-ofr_headDataTitle").text.replace('\n', '').replace('  ', '')

                    # Attributes
                    specifications_names = soup2.find_all("dt", class_="m-offerShowData_name js-offerShowData_row")
                    specifications_params = soup2.find_all("dd", class_="m-offerShowData_param js-offerShowData_row")

                    if specifications_params[0] is None:
                        features = ""
                    else:
                        features = "Producent@" + specifications_params[0].text.replace('\n', '') + "|"

                    for k in range(len(specifications_names)):
                        if specifications_names[k].text.replace('\n', '') == "Gatunek":
                            subsubcategories = specifications_params[k].text.replace('\n', '')

                        params = specifications_params[k].find_all("span")

                        if specifications_names[k].text.replace('\n', '') == "Dodatkowo na płycie" and len(
                                params[0].text) > 255:
                            continue

                        for param in params:
                            features +=specifications_names[k].text.replace('\n', '') + "@" + param.text\
                                .replace('\n', '').replace('  ', '').replace('\r', ' ')+ "|"
                    features = features[:-1]

                    # Price
                    price = soup2.find("div", class_="m-priceBox_price").text.replace('zł', '').replace(' ', '').replace('\n', '').replace(',', '.').replace('-', '0')

                    # Description
                    description = soup2.find("div", class_="widget text_editor")

                    if description is None:
                        description = soup2.find("span", itemprop="description")
                        if description is None:
                            description = soup2.find("div",
                                                     class_="b-offerRWD_descriptionInner js-offerRWD_descriptionInner")
                            if description is None:
                                description = "Description"
                            else:
                                description = "<p>" + description.find("p").text.replace('\n', '<br>').replace('\t', ' ').replace('\r', ' ') + "</p>"
                        else:
                            description = "<p>" + description.text.replace('\n', '<br>').replace('\t', ' ').replace('\r', ' ') + "</p>"
                    else:
                        description = "<p>" + description.text.replace('\n', '<br>').replace('\t', ' ').replace('\r', ' ') + "</p>"

                    # Categories
                    film_category = str(i * 8 + j + 1003) + "|" + str(1000 + i + 1) + "|" + str(1000)
                    for subsubcategory in subsubcategories.split(','):
                        subsubcategory = subsubcategory.replace('\n', '').replace(' ', '')
                        for k, subsubcategory_name in enumerate(subsubcategories_names):
                            if subsubcategory == subsubcategory_name[0] or subsubcategory == \
                                    subsubcategory_name[1]:
                                film_category += "|" + str(i * 8 + k + 1003)
                    film_category_list = list(dict.fromkeys(film_category.split('|')))
                    film_category = '|'.join(film_category_list)

                    # Image
                    download_file(id, soup2)

                    # Save product in products.csv
                    writer.writerow({"Id": id,
                                     "Name": name,
                                     "Link": url['href'].split("/")[-1],
                                     "Categories": film_category,
                                     "Price": str(round(float(price) / 1.23, 4)),
                                     "Wholesale price": round((float(price) / 1.23) * 0.9, 2),
                                     "Features": features,
                                     "Description": description,
                                     })
                    id += 1
                    a += 1
                    print(id - 1)
                    # Only 50 products per category
                    if a > 50:
                        break


def main():
    
    create_products_file()
    delete_duplicates()


if __name__ == "__main__":
    main()
