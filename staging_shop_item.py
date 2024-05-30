class StagingShopItem:
    def __init__(self, id_from_store:str, name:str, price:float, prod_image_links:list):
        self.id_from_store = id_from_store
        self.name = name
        self.price = price
        self.prod_image_links = prod_image_links
        self.last_extracted_at = None
        

    def print_basic_info(self):
        print(f"id_from_store: {self.id_from_store}")
        print(f"Name: {self.name}")
        print(f"Price: {self.price}")
        print(f"Product image links: {self.prod_image_links}")
        print(f'last extracted at: {self.last_extracted_at}')
