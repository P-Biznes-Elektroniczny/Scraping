import csv
import io
from prestapyt import PrestaShopWebServiceDict


# pip install --ignore-installed git+https://github.com/prestapyt/prestapyt.git@master


# Add category to prestashop
def create_category(prestashop, blank_category, names, links, deep):
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


# Add category tree to prestashop
def create_category_tree(prestashop):
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
    create_category(prestashop, blank_category, main_category_name, main_category_link, 2)
    # Categories
    create_category(prestashop, blank_category, categories_name, categories_link, 1000)
    # Subcategories
    create_category(prestashop, blank_category, subcategories_name, subcategories_link, 1001)
    create_category(prestashop, blank_category, subcategories_name, subcategories_link, 1002)


# Add image to product
def add_image(prestashop, image_id, product_id):
    file_name = 'images/' + str(image_id) + '.jpeg'
    fd = io.open(file_name, "rb")
    content = fd.read()
    fd.close()
    prestashop.add('/images/products/' + str(product_id), files=[('image', file_name, content)])


# Add attributes  and quantities to product
def add_combinations(prestashop, id_product):

    # Attributes
    # PL
    blank_combination = prestashop.get('combinations', options={'schema': 'blank'})
    blank_combination.update({'combination': {
        'id_product': str(id_product),
        'minimal_quantity': '1',
        'associations': {'product_option_values': {'product_option_value': {'id': '1'}}}}}
    )
    prestashop.add('combinations', blank_combination)
    # EN
    blank_combination.update({'combination': {
        'id_product': str(id_product),
        'minimal_quantity': '1',
        'associations': {'product_option_values': {'product_option_value': {'id': '2'}}}}}
    )
    prestashop.add('combinations', blank_combination)

    # Quantities
    blank_stock_available = prestashop.get('stock_availables', id_product * 3 - 1)
    blank_stock_available['stock_available']['quantity'] = 50
    prestashop.edit('stock_availables', blank_stock_available)

    blank_stock_available = prestashop.get('stock_availables', id_product * 3)
    blank_stock_available['stock_available']['quantity'] = 50
    prestashop.edit('stock_availables', blank_stock_available)


# Add products to prestashop
def add_products(prestashop):

    dict = {}
    product_features_dict = {}
    features, names = get_features()

    with open('products.csv', encoding="utf8") as csvfile:
        products = list(csv.reader(csvfile, delimiter=";"))
        blank_product = prestashop.get('products', options={'schema': 'blank'})

        for i in range(0, 568):
            print(i)

            # Categories
            categories = []
            dict["id"] = products[i][3].split("|")[0]
            categories.append(dict.copy())
            for j in range(1, len(products[i][3].split("|"))):
                dict["id"] = products[i][3].split("|")[j]
                categories.append(dict.copy())
            id_category_default = [x['id'] for x in categories]

            # Features
            product_features = []
            for product_feature in products[i][6].split('|'):
                for k, feature_name in enumerate(names):
                    if feature_name == product_feature.split('@')[0]:
                        product_features_dict["id"] = k + 1
                        break
                for k, feature in enumerate(features):
                    if feature == product_feature:
                        product_features_dict["id_feature_value"] = k + 1
                        break
                product_features.append(product_features_dict.copy())

            # Product
            blank_product.update({'product': {
                'id_manufacturer': '0',
                'id_default_combination': '1',
                'id_category_default': max(id_category_default),
                'id_tax_rules_group': '1',
                'reference': '1438245'+str(i),
                'supplier_reference': '982473182',
                'state': '1',
                'on_sale': '0',
                'price': str(round(float(products[i][4]), 3)),
                'wholesale_price': products[i][5],
                'customizable': '1',
                'active': '1',
                'show_condition': '1',
                'condition': 'new',
                'show_price': '1',
                'visibility': 'both',
                'available_for_order': '1',
                'link_rewrite': {'language': {'attrs': {'id': '2'}, 'value': products[i][2]}},
                'name': {'language': [{'attrs': {'id': '1'}, 'value': products[i][1]},
                                      {'attrs': {'id': '2'}, 'value': products[i][1]}]},
                'description': {'language': {'attrs': {'id': '2'}, 'value':products[i][7]}},
                'description_short': {'language': {'attrs': {'id': '2'}, 'value': 'Film'}},
                'available_now': {'language': {'attrs': {'id': '2'}, 'value': 'Produkt dostępny'}},
                'available_later': {'language': {'attrs': {'id': '2'}, 'value': 'Zamówienie dozwolone'}},
                'associations': {
                    'categories': {'attrs': {'nodeType': 'category', 'api': 'categories'}, 'category': categories},
                    #'combinations': {'attrs': {'nodeType': 'combination', 'api': 'combinations'},'combination': [{'id': '1'}, {'id': '2'}]},
                    #'product_option_values': {'attrs': {'nodeType': 'product_option_value', 'api': 'product_option_values'},'product_option_value': [{'id': '1'}, {'id': '2'}]},
                    'product_features': {'attrs': {'nodeType': 'product_feature', 'api': 'product_features'},'product_feature': product_features},
                    #'stock_availables': {'attrs': {'nodeType': 'stock_available', 'api': 'stock_availables'},'stock_available': [{'id': '869', 'id_product_attribute': '0'},{'id': '1125', 'id_product_attribute': '1'},{'id': '1126', 'id_product_attribute': '2'}]},
                    }}}

            )
            prestashop.add('products', blank_product)
            add_image(prestashop, products[i][0], i)
            add_combinations(prestashop, i)


# Add features to prestashop
def add_features(names, prestashop):
    blank = prestashop.get('product_features', options={'schema': 'blank'})
    for name in names:
        blank.update({'product_feature': {
            'name': {'language': {'attrs': {'id': '2'}, 'value': name}}}
        })
        prestashop.add('product_features', blank)
    return names


# Add feature values to prestashop
def add_values(prestashop, features, names):
    id_feature = 1
    blank = prestashop.get('product_feature_values', options={'schema': 'blank'})
    for i, feature in enumerate(features):
        print(i)
        for j, name in enumerate(names):
            if feature.split("@")[0] == name:
                id_feature = j + 1
                break
        blank.update({'product_feature_value': {
            'id_feature': str(id_feature),
            'value': {'language': {'attrs': {'id': '2'}, 'value': feature.split("@")[1]}}}
        })
        prestashop.add('product_feature_values', blank)


# Get features and feature values from products.csv
def get_features():
    features = []
    names = []
    with open('products.csv', encoding="utf8") as csvfile:
        products = list(csv.reader(csvfile, delimiter=";"))
        for i in range(1, len(products)):
            features += products[i][6].split('|')

        features = list(dict.fromkeys(features))
        for i, atr in enumerate(features):
            names.append(atr.split('@')[0])
        names = list(dict.fromkeys(names))
        return features, names


# Add feature tree to prestashop
def create_feature_tree(prestashop):
    features, names = get_features()
    add_features(names, prestashop)
    add_values(prestashop, features, names)


def main():
    prestashop = PrestaShopWebServiceDict('http://efilmy.best/api',
                                          'AZ2A2PZC183CQIEHI8KR3SC48E8CTA7T', )
    while 1:
        print("1 Create Category Tree")
        print("2 Add features")
        print("3 Add products")
        print("4 Exit")
        x = input()
        if x == '1':
            create_category_tree(prestashop)
        elif x == '2':
            create_feature_tree(prestashop)
        elif x == '3':
            add_products(prestashop)
        elif x == '4':
            break


if __name__ == "__main__":
    main()
