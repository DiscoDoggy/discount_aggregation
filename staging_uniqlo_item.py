from staging_shop_item import *

class StagingUniqloItem(StagingShopItem):
    def __init__(self, json_api_response):
        self.fields_dict = self.parse_json()
        # super().__init__(id_from_store, name, price, prod_images)
    def parse_json(self):
        parsed_json_items = []

        #this is an array of items ['items'] maps to an array of dicts
        unparsed_json_items = self.json_api_response["result"]["items"]
        
        for item in unparsed_json_items:
            parsed_json_item = {}
            
            parsed_json_item['id_from_api'] = item['productId']
            parsed_json_item['item_name'] = item['name']

            parsed_json_item['base_price'] = item['prices']['base']['value']
            parsed_json_item['promo_price'] = item['prices']['promo']['value']

            parsed_json_item['clothing_gender'] = item['genderName']
            parsed_json_item['clothing_gender_category'] = item['genderCategory']

            parsed_json_item['item_colors'] = self.parse_colors(item['colors'])

            parsed_json_item['ratings'] = item['rating']['average']
            parsed_json_item['num_ratings'] = item['rating']['count']

            parsed_json_item['sale_start_time'] = item['effectiveTime']['start']

    def parse_colors(self, colors_dict:dict) -> list:
        colors_list = colors_dict['colors']
        color_names = []

        color_names = [color_name['filterCode'] for color_name in colors_list]

        return color_names





