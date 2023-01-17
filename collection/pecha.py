import csv
from pathlib import Path
from typing import List

from collection.collection import Collection
from views.view import ViewSerializer


class PechaCollection(Collection):

    def __init__(self, title:str, items, views:List[ViewSerializer], parent_dir: Path, id=None) -> None:
        super().__init__(
            title=title,
            items=items,
            views=views,
            parent_dir=parent_dir,
            id=id
            )

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
