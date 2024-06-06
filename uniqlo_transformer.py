from base_transformer import *
import uuid
from datetime import datetime

class UniqloTransformer(BaseTransformer):
    def __init__(self, extraction_id):
        super().__init__(extraction_id=extraction_id)

    def transform_data(self):
        unprocessed_data = super().get_data_to_transform()
        processed_data = []
        for data_point in unprocessed_data:

            #TODO: Truncate/pad to 2 decimal points
            data_point['base_price'] = float(data_point['base_price'])
            data_point['promo_price'] = float(data_point['promo_price'])
            data_point['ratings'] = float(data_point['ratings'])

            data_point['extraction_id'] = uuid.UUID(data_point['extraction_id'])
            
            #converting UNIX timestamp to date

            #datetime is in current string format 2024-06-05 02:33:19.270915+00:00
            data_point['extraction_datetime'] = datetime.strptime(data_point['extraction_datetime'], "%Y-%m-%d %H:%M:%S")            


    
