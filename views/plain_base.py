from pathlib import Path
from openpecha.core.pecha import OpenPechaFS

from items.pecha import Pecha
from views.view import ViewSerializer



class PlainBaseViewSerializer(ViewSerializer):

    def serialize(self, pecha: Pecha, output_dir: Path):
        opf_obj = OpenPechaFS(path=pecha.pecha_path)
        for base_name, base_components in opf_obj.components.items():
            base_text = opf_obj.get_base(base_name)
            (output_dir / f"{base_name}.txt").write_text(base_text, encoding='utf-8')