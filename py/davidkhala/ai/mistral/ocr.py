import base64
import json
from pathlib import Path

from davidkhala.ml.ocr.interface import FieldProperties as BaseFieldProperties
from mistralai import ImageURLChunk, ResponseFormat, JSONSchema

from davidkhala.ai.mistral import Client as MistralClient


class FieldProperties(BaseFieldProperties):
    description: str = ""


class Client(MistralClient):
    def process(self, file: Path, schema: dict[str, FieldProperties] = None) -> list[dict]|dict:
        """
        Allowed formats are JPEG, PNG, WEBP, GIF, MPO, HEIF, AVIF, BMP, TIFF
        """
        with open(file, "rb") as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        options = {}
        if schema:
            required = [k for k, _ in schema.items() if _.required]
            properties = {k: {'type': v.type, 'description': v.description} for k, v in schema.items()}
            options['document_annotation_format'] = ResponseFormat(
                type='json_schema',
                json_schema=JSONSchema(
                    name='-',
                    schema_definition={
                        "required": required,
                        "properties": properties
                    },
                    strict=True
                )
            )

        ocr_response = self.client.ocr.process(
            model="mistral-ocr-latest",
            document=ImageURLChunk(image_url=f"data:image/jpeg;base64,{content}"),
            include_image_base64=True,
            **options,
        )
        if schema:
            return json.loads(ocr_response.document_annotation)
        return [{'markdown': page.markdown, 'images': page.images} for page in ocr_response.pages]
