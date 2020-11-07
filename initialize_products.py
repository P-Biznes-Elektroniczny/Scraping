import csv
import io

from prestapyt import PrestaShopWebServiceDict

#pip install --ignore-installed git+https://github.com/prestapyt/prestapyt.git@master


def categoryCreate(prestashop, blank_category, names, links, deep):

    for i in range(0, len(names)):
        blank_category.update({'category': {
            'id_parent': deep,
            'active': '1',
            'name': {
                'language': [{'attrs': {'id': '1'}, 'value': names[i]}, {'attrs': {'id': '2'}, 'value': names[i]}]},
            'link_rewrite': {
                'language': [{'attrs': {'id': '1'}, 'value': links[i]}, {'attrs': {'id': '2'}, 'value': links[i]}]}
        }})
        prestashop.add('categories', blank_category)

def categoryTree(prestashop):
    #prestashop.delete('categories', 10)

    main_category_name = ["Filmy"]
    categories_name = ["DVD", "Blu-Ray"]
    subcategories_name = ["Animowane/Familijne", "Dokumentalne", "Dramat", "Fantasy/Sci-Fi", "Horror/Thriller",
                          "Komedia/Komedia Romantyczna", "Muzyczne/Musicale", "Sensacyjne/Przygodowe"]

    main_category_link = ["filmy"]
    categories_link = ["filmy-dvd", "filmy-blu-ray"]
    subcategories_link = ["animowanefamilijne", "dokumentalne", "dramat", "fantasysci-fi","horrorthriller",
                     "komediakomedia-romantyczna", "muzycznemusicale", "sensacyjneprzygodowe"]

    blank_category = prestashop.get('categories', options={'schema': 'blank'})
    print(blank_category)

    #Film
    categoryCreate(prestashop, blank_category, main_category_name, main_category_link, 2)
    #Dvd BluRay
    categoryCreate(prestashop, blank_category, categories_name, categories_link, 1000)
    categoryCreate(prestashop, blank_category, subcategories_name, subcategories_link, 1001)
    categoryCreate(prestashop, blank_category, subcategories_name, subcategories_link, 1002)

def addNewProduct(prestashop):

    with open('products.csv', encoding="utf16") as csvfile:
        products = list(csv.reader(csvfile))
        blank_product = prestashop.get('products', options={'schema': 'blank'})
        print(blank_product)

        for i in range(1, 2):


            blank_product.update({
                'product': { 'id_supplier': '0',
                             'id_category_default': str(int(products[i][3])*6+int(products[i][4])+1003),
                             'new': '',
                             'cache_default_attribute': '1',
                             'id_default_image': {'attrs': {'notFilterable': 'true'}, 'value': '1'},
                             'id_default_combination': {'attrs': {'notFilterable': 'true'}, 'value': '1'},
                             'id_tax_rules_group': '1',
                             'position_in_category': {'attrs': {'notFilterable': 'true'}, 'value': ''},
                             'type': {'attrs': {'notFilterable': 'true'}, 'value': 'simple'},
                             'id_shop_default': '1',
                             'reference': 'demo_1',
                             'supplier_reference': '',
                             'location': '',
                             'quantity_discount': '0',
                             'ean13': '',
                             'isbn': '',
                             'upc': '',
                             'cache_is_pack': '0',
                             'cache_has_attachments': '0',
                             'is_virtual': '0',
                             'state': '1',
                             'additional_delivery_times': '1',
                             'delivery_in_stock': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'delivery_out_stock': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'on_sale': '0',
                             'online_only': '0',
                             'ecotax': '0.000000',
                             'minimal_quantity': '1',
                             'low_stock_threshold': '',
                             'low_stock_alert': '0',
                             'price': '23.900000',
                             'wholesale_price': '0.000000',
                             'unity': '',
                             'unit_price_ratio': '0.000000',
                             'additional_shipping_cost': '0.00',
                             'customizable': '0',
                             'text_fields': '0',
                             'uploadable_files': '0',
                             'active': '1',
                             'redirect_type': '301-category',
                             'id_type_redirected': '0',
                             'available_for_order': '1',
                             'available_date': '0000-00-00',
                             'show_condition': '0',
                             'condition': 'new',
                             'show_price': '1',
                             'indexed': '1',
                             'visibility': 'both',
                             'advanced_stock_management': '0',
                             'date_add': '2020-10-17 16:57:34',
                             'date_upd': '2020-10-17 16:57:34',
                             'quantity': 3,
                             'pack_stock_type': '3',
                             'meta_description': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'meta_keywords': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'meta_title': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': 'hummingbird-printed-t-shirt'}, {'attrs': {'id': '2'}, 'value': 'hummingbird-printed-t-shirt'}]},
                             'name': {'language': [{'attrs': {'id': '1'}, 'value': products[i][1]}, {'attrs': {'id': '2'}, 'value': products[i][1]}]},
                             'description': {'language': [{'attrs': {'id': '1'}, 'value': '<p><span style="font-size:10pt;font-style:normal;"><span style="font-size:10pt;font-style:normal;">Symbol of lightness and delicacy, the hummingbird evokes curiosity and joy.</span><span style="font-size:10pt;font-style:normal;"> Studio Design\' PolyFaune collection features classic products with colorful patterns, inspired by the traditional japanese origamis. To wear with a chino or jeans. The sublimation textile printing process provides an exceptional color rendering and a color, guaranteed overtime.</span></span></p>'}, {'attrs': {'id': '2'}, 'value': '<p><span style="font-size:10pt;font-style:normal;"><span style="font-size:10pt;font-style:normal;">Symbol of lightness and delicacy, the hummingbird evokes curiosity and joy.</span><span style="font-size:10pt;font-style:normal;"> Studio Design\' PolyFaune collection features classic products with colorful patterns, inspired by the traditional japanese origamis. To wear with a chino or jeans. The sublimation textile printing process provides an exceptional color rendering and a color, guaranteed overtime.</span></span></p>'}]},
                             'description_short': {'language': [{'attrs': {'id': '1'}, 'value': '<p><span style="font-size:10pt;font-style:normal;">Regular fit, round neckline, short sleeves. Made of extra long staple pima cotton. </span></p>\n<p></p>'}, {'attrs': {'id': '2'}, 'value': '<p><span style="font-size:10pt;font-style:normal;">Regular fit, round neckline, short sleeves. Made of extra long staple pima cotton. </span></p>\n<p></p>'}]},
                             'available_now': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'available_later': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'associations': {'categories': {'attrs': {'nodeType': 'category', 'api': 'categories'}, 'category': {'id': '2'}}, 'images': {'attrs': {'nodeType': 'image', 'api': 'images'}, 'image': [{'id': '1'}, {'id': '2'}]}, 'combinations': {'attrs': {'nodeType': 'combination', 'api': 'combinations'}, 'combination': [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}, {'id': '6'}, {'id': '7'}, {'id': '8'}]}, 'product_option_values': {'attrs': {'nodeType': 'product_option_value', 'api': 'product_option_values'}, 'product_option_value': [{'id': '1'}, {'id': '8'}, {'id': '11'}, {'id': '2'}, {'id': '3'}, {'id': '4'}]}, 'product_features': {'attrs': {'nodeType': 'product_feature', 'api': 'product_features'}, 'product_feature': [{'id': '1', 'id_feature_value': '4'}, {'id': '2', 'id_feature_value': '8'}]}, 'tags': {'attrs': {'nodeType': 'tag', 'api': 'tags'}, 'value': ''}, 'stock_availables': {'attrs': {'nodeType': 'stock_available', 'api': 'stock_availables'}, 'stock_available': [{'id': '1', 'id_product_attribute': '0'}, {'id': '20', 'id_product_attribute': '1'}, {'id': '21', 'id_product_attribute': '2'}, {'id': '22', 'id_product_attribute': '3'}, {'id': '23', 'id_product_attribute': '4'}, {'id': '24', 'id_product_attribute': '5'}, {'id': '25', 'id_product_attribute': '6'}, {'id': '26', 'id_product_attribute': '7'}, {'id': '27', 'id_product_attribute': '8'}]}, 'accessories': {'attrs': {'nodeType': 'product', 'api': 'products'}, 'value': ''}, 'product_bundle': {'attrs': {'nodeType': 'product', 'api': 'products'}, 'value': ''}}
                    }})
            prestashop.add('products', blank_product)



def addImg(prestashop):
    for i in range(1, 65):
        file_name = 'images/' + str(i) + '.jpeg'
        fd = io.open(file_name, "rb")
        content = fd.read()
        fd.close()
        prestashop.add('/images/products/' + str(i), files=[('image', file_name, content)])

def main():
    prestashop = PrestaShopWebServiceDict('http://efilmy.best/api',
                                          'AZ2A2PZC183CQIEHI8KR3SC48E8CTA7T', )

    #categoryTree(prestashop)
    #addImg(prestashop)

    #addNewProduct(prestashop)


if __name__ == "__main__":
    main()