from openpecha.serializers.hfml import HFMLSerializer

from serializers.serialize import ViewSerializer


class HFMLViewSerializer(ViewSerializer):

    def serialize(self, pecha, output_dir):
        serializer = HFMLSerializer(opf_path=pecha.pecha_path)
        serializer.apply_layers()
        serialized_results = serializer.get_result()
        for base_name, hfml_text in serialized_results.items():
            (output_dir / f"{base_name}.txt").write_text(hfml_text, encoding='utf-8')