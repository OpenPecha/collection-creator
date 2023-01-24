from .view import ViewSerializer,View
from openpecha.utils import load_yaml,_mkdir,download_pecha
from pathlib import Path
from typing import List

class TextPairView(View):
    def __init__(self, name: str, serializer_class: ViewSerializer) -> None:
        super().__init__(name, serializer_class)

    def save_catalog(self, collection_dir: Path, items: List):
        pass


class TextPairSerializer(ViewSerializer):        

    def __init__(self):
        self.type_of_layers = set()
        self.no_of_text = 0
        self.no_of_aligned_seg = 0
        self.read_me=[]
        self.lang_seg_count = {}

    def serialize(self, pecha, output_dir:Path):
        views,alignment_meta = self.parse_opa(pecha)
        self.write_view(views,output_dir,pecha)
        #readme = self.create_readme()
        #Path(f"{collection_id}/readme.md").write_text(readme)
    
    def write_view(self,views,output_dir:Path,opa):
        _mkdir(output_dir)
        for view in views:
            for lang,text in view.items():
                view_file_path = f"{output_dir.as_posix()}/{opa.id}-{lang}.txt"
                Path(view_file_path).write_text(text)

    def update_lang_seg_count(self,lang):
        if lang not in self.lang_seg_count.keys():
            self.lang_seg_count[lang] = 1
        else:
            self.lang_seg_count[lang]+=1 


    def get_item(self,id,output=None):
        path = download_pecha(pecha_id=id,out_path=output)
        return path
    
    def get_layers(self,segment_sources):
        item_to_layer={}
        """"
        item_to_layer={"pecha_id":{
            "base":base_text,
            "segment_layer":segment_layer
        }}
        """
        for pecha_id in segment_sources.keys():
            base = segment_sources[pecha_id]["base"]
            pecha_path = self.get_item(pecha_id)
            base_text = Path(pecha_path / f"{pecha_id}.opf/base/{base}.txt").read_text(encoding="utf-8")
            segment_layer = load_yaml(Path(pecha_path /f"{pecha_id}.opf/layers/{base}/Segment.yml"))
            meta = load_yaml(Path(pecha_path /f"{pecha_id}.opf/meta.yml"))
            item_to_layer.update({pecha_id:{
                "base":base_text,
                "segment_layer":segment_layer,
                "meta":meta
            }})
        
        return item_to_layer

    def parse_opa(self,opa):
        views = []
        opa_file_path = self.get_item(opa.id)
        alignment_bases = self.get_alignment_base(opa_file_path / f"{opa_file_path.name}.opa")
        for alignment_base in alignment_bases:
            alignment = load_yaml(alignment_base)
            view = self.get_view(alignment)
            views.append(view)
        alignment_meta = load_yaml(opa_file_path / f"{opa_file_path.name}.opa/meta.yml")
        return views,alignment_meta
    

    def get_alignment_base(self,opa_path:Path):
        alignment_files = []
        for file in opa_path.iterdir():
            if file.name != "meta.yml":
                alignment_files.append(file)

        return alignment_files

    def get_view(self,alignment):
        view = {}
        """
        view = {
            "lang":text
        }
        """
        segment_sources = alignment["segment_sources"]
        segment_pairs = alignment["segment_pairs"]
        item_to_layer = self.get_layers(segment_sources)
        self.no_of_text+=len(segment_sources.keys())
        
        
        for ann_id in segment_pairs.keys():
            for pecha_id,seg_id in segment_pairs[ann_id].items():
                base_text = item_to_layer[pecha_id]["base"]
                segment_ann = item_to_layer[pecha_id]["segment_layer"]["annotations"]
                span = segment_ann[seg_id]["span"]
                segment_text = base_text[span["start"]:span["end"]]
                lang = segment_sources[pecha_id]["language"]
                if lang not in view.keys():
                    view.update({lang:segment_text})
                else:
                    view.update({lang:view[lang]+"\n"+segment_text}) 
                self.update_lang_seg_count(lang)
            self.no_of_aligned_seg+=1
        return view

    