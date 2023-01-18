from collection.collection import Collection
from views.view import ViewSerializer
from pathlib import Path
from typing import List
from items.alignment import Alignment

class AlignmentCollection(Collection):

    def __init__(self, title:str, items:List[str], views:List[ViewSerializer], parent_dir: Path, id=None) -> None:
        items = self.get_items_obj(items)
        super().__init__(
            title=title,
            items=items,
            views=views,
            parent_dir=parent_dir,
            id=id
            )
        self.type_of_layers = set()
        self.no_of_text = 0
        self.no_of_aligned_seg = 0
        self.read_me=[]
        self.lang_seg_count = {}
    
    def get_items_obj(self,items:List[str]):
        items_obj = []
        for item in items:
            item_obj = Alignment(item)
            items_obj.append(item_obj)
        return items_obj

    
    def save_catalog(self, view_name):
        pass
    