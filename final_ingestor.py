from sqlalchemy import create_engine
from sqlalchemy import text 
from sqlalchemy import MetaData, Table, insert, update
from sqlalchemy import select
import os
from dotenv import load_dotenv
import uuid

"""
When we start to ingest processed data what do we want,
    For a specific row in processed data,
        we want to check if this row already exists in the final DB
            if it does exist we need to check if any of the fields have been updated
                if there have been fields that have been updated
                    update fields and push the record change to the record change table
                else: do nothing move onto next row
            else 
                add the row to the table
    need to move statuses to archived if no longer found in extraction
"""
class FinalIngestor():
    def __init__(self, processed_data:list[dict]):
        self.processed_data = processed_data
        self.engine = self.connect_to_db()
        self.connection = self.engine.connect()
        self.meta_data = MetaData()
        self.items = Table("items", self.meta_data, autoload_with=self.engine)
        self.extractions = Table("extractions", self.meta_data, autoload_with=self.engine)
        self.sites = Table("sites", self.meta_data, autoload_with=self.engine)
        self.item_change_records = Table("item_change_records", self.meta_data, autoload_with=self.engine)
        print("Length of processed data:", len(self.processed_data))

    def ingest_data(self):
        import_error_rows = []
        self.update_db_discount_statuses(1)

        for i in range (len(self.processed_data)):
            row = self.processed_data[i]
            
            new_id = uuid.uuid4()
            row['id'] = new_id
            if i == 0:
                insert_extractions_query = self.insert_into_extractions_table(row)
                self.connection.execute(insert_extractions_query)
                self.connection.commit()

            dupe_query_results = self.return_dupe_in_db(row)
            print(dupe_query_results)

            if not dupe_query_results: #if list is empty (no dupe) add to db
                insert_item_query = self.craft_insert_items_query(row)
                self.connection.execute(insert_item_query)
            elif len(dupe_query_results) > 1:
                #import error more than one dupe potential multiple duplications
                print("UH OH MORE THAN ONE DUPLICATE COULD BE PRESENT FOR id from site:", row['id_from_site'])
                import_error_rows.append(row)
                continue
            else:
                #update row with information that the source resource returned
                update_query = self.craft_update_items_query(row, dupe_query_results[0][0])
                result = self.connection.execute(update_query)

            self.connection.commit()
        self.connection.close()
        self.engine.dispose()

    def update_db_discount_statuses(self, site_id:int):
        #use the same criteria as dupe criteria
        # id_from_site, item_name, sale_start

        active_discount_query = select(
            self.items.c.id,
            self.items.c.id_from_site,
            self.items.c.name,
            self.items.c.sale_start
        ).where(
            self.items.c.site_id == site_id and
            self.items.c.discount_status == 'ACTIVE'
        )

        #list of tuples
        query_results = self.connection.execute(active_discount_query).all()

        active_db_discount = {}
        for result in query_results:
            active_db_discount[result.id_from_site] = result

        extracted_db_discounts = {}
        for item in self.processed_data:
            extracted_db_discounts[item['id_from_site']] = item

        for result_item_id in active_db_discount:
            if result_item_id not in extracted_db_discounts:
                #mark as inactive
                result_dict = active_db_discount[result_item_id]
                id_to_update = result_dict.id

                print("ID TO UPDATE:", id_to_update)

                update_query = self.items.update() \
                .where(self.items.c.id == id_to_update) \
                .values(discount_status = 'INACTIVE')
                self.connection.execute(update_query)
                self.connection.commit()


    def return_dupe_in_db(self, row:dict) -> list:
        #dupe criteria
            #* id_from_site, item name, sale_start
        query = select(
            self.items.c.id,
            self.items.c.id_from_site, 
            self.items.c.name, 
            self.items.c.sale_start
            ).where(
            self.items.c.id_from_site == row['id_from_site'] and 
            self.items.c.name == row['item_name'] and 
            self.items.c.sale_start == row['sale_start_time']
            )
        query_result = self.connection.execute(query)

        return query_result.all()
    
    def insert_into_extractions_table(self, row):
        insert_query = insert(self.extractions).values(
            id=row['extraction_id']
        )

        return insert_query

    def craft_insert_items_query(self, row):
        insert_query = insert(self.items).values(
            id=row['id'],
            id_from_site=row['id_from_site'],
            name=row['item_name'],
            link=row['link_to_item'],
            base_price=row['base_price'],
            promo_price=row['promo_price'],
            gender=row['clothing_gender_category'],
            colors=row['item_colors'],
            sizes=row['item_sizes'],
            rating=row['ratings'],
            num_ratings = row['num_ratings'],
            sale_start = row['sale_start_time'],
            discount_status=row['discount_status'],
            site_id=row['site_id'],
            extraction_id = row['extraction_id'],
            image_links=row['image_links']
        )

        return insert_query

    def craft_update_items_query(self, row, id_to_update):
        update_query = self.items.update() \
        .where(self.items.c.id == id_to_update) \
        .values(
            id=row['id'],
            id_from_site=row['id_from_site'],
            name=row['item_name'],
            link=row['link_to_item'],
            base_price=row['base_price'],
            promo_price=row['promo_price'],
            gender=row['clothing_gender_category'],
            colors=row['item_colors'],
            sizes=row['item_sizes'],
            rating=row['ratings'],
            num_ratings = row['num_ratings'],
            sale_start = row['sale_start_time'],
            discount_status=row['discount_status'],
            site_id=row['site_id'],
            #extraction_id = row['extraction_id'],
            image_links=row['image_links']
        )

        return update_query
  
    def connect_to_db(self):
        load_dotenv()
        POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        POSTGRES_NAME = os.getenv('POSTGRES_NAME')

        connection_url = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
        engine = create_engine(connection_url, echo=False)

        return engine
    
def test_runner():

    row = {
        'id_from_site': "12345",
        'item_name': 'Example Item',
        'link_to_item': 'http://example.com/item',
        'base_price': 49.99,
        'promo_price': 39.99,
        'clothing_gender_category': 'Unisex',
        'item_colors': ['Red', 'Blue', 'Green'],
        'item_sizes': ['S', 'M', 'L', 'XL'],
        'ratings': 4.5,
        'num_ratings': 120,
        'sale_start_time': '2024-05-01',
        'discount_status': 'ACTIVE',
        'site_id': 1,
        'extraction_id': uuid.uuid4(),
        'image_links': [
            'http://example.com/image1.jpg',
            'http://example.com/image2.jpg'
        ]
    }

    mylist = []
    mylist.append(row)
    ingestion_object = FinalIngestor(mylist)

    ingestion_object.ingest_data()
# runner()
