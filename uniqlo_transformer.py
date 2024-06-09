from base_transformer import *
import uuid
from datetime import datetime
import re

class UniqloTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()

    def transform_data(self, extraction_id):
        unprocessed_data = super().get_data_to_transform(extraction_id)
        processed_data = []
        for data_point in unprocessed_data:

            #TODO: Truncate/pad to 2 decimal points
            data_point['base_price'] = float(data_point['base_price'])
            data_point['promo_price'] = float(data_point['promo_price'])
            data_point['ratings'] = float(data_point['ratings'])
            data_point['extraction_id'] = uuid.UUID(data_point['extraction_id'])
            #converting UNIX timestamp to date
            data_point['sale_start_time'] = datetime.fromtimestamp(data_point['sale_start_time']).date()
            
            #datetime is in current string format 2024-06-05 02:33:19.270915+00:00
            pattern = r'^.*(?=\.)'
            data_point['extraction_datetime'] = re.match(pattern, data_point['extraction_datetime']).group(0)
            data_point['extraction_datetime'] = datetime.strptime(data_point['extraction_datetime'], "%Y-%m-%d %H:%M:%S")            

            processed_data.append(data_point)

        return processed_data
    
