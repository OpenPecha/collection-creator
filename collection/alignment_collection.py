from collection.collection import Collection
from views.view import ViewSerializer
from pathlib import Path
from typing import List
from items.alignment import Alignment

class AlignmentCollection(Collection):

    def __init__(self, title:str, items:List[Alignment], views:List[ViewSerializer], parent_dir: Path, id=None) -> None:
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
    
    def save_catalog(self, view_name):
        pass
    