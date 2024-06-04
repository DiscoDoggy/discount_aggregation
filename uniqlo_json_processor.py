from json_processor import *

class UniqloJsonProcessor(JsonProcessor):
    def __init__(self):
        super().__init__()

    def parse_json(self, json_res):
        processed_json_items_list = []
        #this is an array of items ['items'] maps to an array of dicts
        unparsed_json_items = json_res["result"]["items"]
        
        #refactor into a single function
        for item in unparsed_json_items:
            parsed_json_item = {}
            
            parsed_json_item['id_from_api'] = item['productId']
            parsed_json_item['link_to_item'] = self.create_item_link(item)
            parsed_json_item['item_name'] = item['name']

            parsed_json_item['base_price'] = item['prices']['base']['value']
            parsed_json_item['promo_price'] = item['prices']['promo']['value']

            parsed_json_item['clothing_gender'] = item['genderName']
            parsed_json_item['clothing_gender_category'] = item['genderCategory']

            parsed_json_item['item_colors'] = self.parse_colors(item['colors'])
            parsed_json_item['item_sizes'] = self.parse_sizes(item['sizes'])

            parsed_json_item['ratings'] = item['rating']['average']
            parsed_json_item['num_ratings'] = item['rating']['count']

            parsed_json_item['sale_start_time'] = item['representative']['flags']['priceFlags'][0]['effectiveTime']['start']

            parsed_json_item['image_links'] = self.parse_images(item)

            processed_json_items_list.append(parsed_json_item)

        return processed_json_items_list

    def parse_colors(self, colors_dict:dict[str, list]) -> list:
        # print(colors_dict)
        # colors_list = colors_dict['colors']
        color_names = []

        color_names = [color_name['filterCode'] for color_name in colors_dict]

        return color_names
    
    def parse_sizes(self, sizes_dict:dict[str, list]) -> list:
        
        return [size["name"] for size in sizes_dict]
        
    
    def create_item_link(self, item_json:dict) -> str:
        """
        Uniqlo API does not provide the link to the product page of each product that is on discount.
        This function is going to, based on product information, create the link to the specific product page

        example product page link: https://www.uniqlo.com/us/en/products/E466775-000/00?colorDisplayCode=01&sizeDisplayCode=003
            * E466775-000 is the product ID
            * 00 is the price group
        price group, color display code, and size display code will need to be found from the JSON item
        """

        base_link = "https://www.uniqlo.com/us/en/products"
        product_id = item_json['productId']
        price_group = item_json['priceGroup']
        color_disp_code = item_json['representative']['color']['displayCode']
        size_display_code = item_json['sizes'][0]['displayCode']

        url_to_product = f"{base_link}/{product_id}/{price_group}?colorDisplayCode={color_disp_code}&sizeDisplayCode={size_display_code}"

        return url_to_product
        
    
    def parse_images(self, item:dict) -> list[str]:
        images_dict = item['images']['main']
        image_links = []

        for image_code in images_dict:
            image_link = images_dict[image_code]['image']
            image_links.append(image_link)

        return image_links