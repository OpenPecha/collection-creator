class ViewSerializer:

    def __init__(self) -> None:
        pass

    
    def serialize(self, pecha, output_dir):
        return NotImplementedError("Please implement your serializer")

class View:

    def __init__(self, name: str, serializer_class: ViewSerializer) -> None:
        self.name = name
        self.serializer_class = serializer_class
    
    def to_dict(self)-> dict:
        return {
            'name': self.name,
            'serializer_class': self.serializer_class.__name__
        }