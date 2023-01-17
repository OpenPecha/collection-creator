import csv

from collection.collection import Collection


class PechaCollection(Collection):

    def __init__(self) -> None:
        super().__init__()

    def save_catalog(self, view_name):
        catalog_file_path = self.collection_dir / f"Catelog_{view_name}.csv"
        field_names = ['FILE NAME', 'TITLE', 'OP ID', 'BDRC ID', 'VOLUME NUMBER']
        items = []
        for item in self.items:
            cur_item_infos = [
                item.base_name,
                item.title,
                item.id,
                item.bdrc_id,
                item.volume_number
            ]
            items.append(cur_item_infos)
        with open(catalog_file_path, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)   
            csvwriter.writerow(field_names) 
        
            # writing the data rows 
            csvwriter.writerows(items)
