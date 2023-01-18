from pathlib import Path
from typing import List
from abc import ABC,abstractmethod

from openpecha.core.ids import get_collection_id
from openpecha.utils import dump_yaml

from views.view import ViewSerializer


class Collection(ABC):

    def __init__(self, title:str, items:List[str], views:List[ViewSerializer], parent_dir: Path, id=None) -> None:
        self.id = id or get_collection_id()
        self.title = title
        self.views = views
        self.items = items
        self.collection_dir = parent_dir / self.id
        self.collection_dir.mkdir(parents=True, exist_ok=True)
        
    
    """
    cant save collection file be abstract method
    """
    @abstractmethod
    def get_items_obj():
        pass

    def save_collection_file(self):
        collection_file_path = self.collection_dir / f"{self.id}.yml"
        views = []
        for view in self.views:
            views.append(view.to_dict())
        items = []
        for item in self.items:
            items.append(item.id)
        collection = {
            'views': views,
            'collection': {
                'id': self.id,
                'title': self.title,
                'items': items
            }
        }
        dump_yaml(collection, collection_file_path)

    
    def save_view(self, view: ViewSerializer):
        view_dir = self.collection_dir / view.name
        view_dir.mkdir(parents=True, exist_ok=True)
        serializer = view.serializer_class()

        for item in self.items:
            serializer.serialize(item, view_dir)


    def save_views(self):
        for view in self.views:
            self.save_view(view)
    
    def save_catalog(self, view_name):
        return NotImplementedError("Please implement the saving of catelog.")

    
    def save_collection(self):
        self.save_collection_file()
        self.save_views()
        for view in self.views:
            self.save_catalog(view_name=view.name)