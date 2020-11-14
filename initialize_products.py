import csv
import io
import os
from random import random
from prestapyt import PrestaShopWebServiceDict


# pip install --ignore-installed git+https://github.com/prestapyt/prestapyt.git@master


def createCategory(prestashop, blank_category, names, links, deep):
    for i in range(0, len(names)):
        blank_category.update({'category': {
            'id_parent': deep,
            'active': '1',
            'name': {
                'language': [{'attrs': {'id': '2'}, 'value': names[i]}]},
            'link_rewrite': {
                'language': [{'attrs': {'id': '2'}, 'value': links[i]}]}
        }})
        prestashop.add('categories', blank_category)


def createCategoryTree(prestashop):
    # prestashop.delete('categories', 1000)

    main_category_name = ["Filmy"]
    categories_name = ["DVD", "Blu-Ray"]
    subcategories_name = ["Animowane/Familijne", "Dokumentalne", "Dramat", "Fantasy/Sci-Fi", "Horror/Thriller",
                          "Komedia/Komedia Romantyczna", "Muzyczne/Musicale", "Sensacyjne/Przygodowe"]

    main_category_link = ["filmy"]
    categories_link = ["filmy-dvd", "filmy-blu-ray"]
    subcategories_link = ["animowanefamilijne", "dokumentalne", "dramat", "fantasysci-fi", "horrorthriller",
                          "komediakomedia-romantyczna", "muzycznemusicale", "sensacyjneprzygodowe"]

    blank_category = prestashop.get('categories', options={'schema': 'blank'})
    print(blank_category)

    # Film
    createCategory(prestashop, blank_category, main_category_name, main_category_link, 2)
    # Dvd BluRay
    createCategory(prestashop, blank_category, categories_name, categories_link, 1000)
    createCategory(prestashop, blank_category, subcategories_name, subcategories_link, 1001)
    createCategory(prestashop, blank_category, subcategories_name, subcategories_link, 1002)


def addImg(prestashop):
    files = next(os.walk("./images"))[2]
    for i in range(1, len(files) + 1):
        file_name = 'images/' + str(i) + '.jpeg'
        fd = io.open(file_name, "rb")
        content = fd.read()
        fd.close()
        try:
            prestashop.add('/images/products/' + str(i), files=[('image', file_name, content)])
        except:
            os.remove("images/" + str(i) + '.jpeg')


def createCombinationsFile():

    with open('combinations.csv', mode='w', encoding="utf8", newline='') as csvfile:
        fieldnames = ["Product ID*", "Product Reference", "Attribute (Name:Type:Position)*", "Value (Value:Position)*",
                      "Supplier reference",
                      "Reference", "EAN13", "UPC", "Wholesale price", "Impact on price", "Ecotax", "Quantity",
                      "Minimal quantity", "Low stock level", "Impact on weight", "Default (0 = No, 1 = Yes)",
                      "Combination available date", "Image position", "Image URLs (x,y,z...)",
                      "Image alt texts (x,y,z...)", "ID / Name of shop", "Advanced Stock Managment", "Depends on stock",
                      "Warehouse"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        files = next(os.walk("./images"))[2]
        print(files)
        for file in files:
            quantity = int(random() * 500)
            writer.writerow({'Product ID*': file.split('.')[0],
                             "Attribute (Name:Type:Position)*": "Wersja językowa:radio:0",
                             "Value (Value:Position)*": "PL:0",
                             "Quantity": quantity * 2,
                             'Default (0 = No, 1 = Yes)': 1,
                             })
            writer.writerow({'Product ID*': file.split('.')[0],
                             "Attribute (Name:Type:Position)*": "Wersja językowa:radio:0",
                             "Value (Value:Position)*": "EN:0",
                             "Quantity": quantity,
                             })


def main():
    prestashop = PrestaShopWebServiceDict('http://efilmy.best/api',
                                          'AZ2A2PZC183CQIEHI8KR3SC48E8CTA7T', )
    while 1:
        print("1 Create Category Tree")
        print("2 Create Combinations File")
        print("3 Add Images to Products")
        print("4 Exit")
        x = input()
        if x == '1':
            createCategoryTree(prestashop)
        elif x == '2':
            createCombinationsFile()
        elif x == '3':
            addImg(prestashop)
        elif x == '4':
            break


if __name__ == "__main__":
    main()
