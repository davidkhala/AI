from pathlib import Path

from mistralai import UploadFileOut, FileSchema, ListFilesOut

from davidkhala.ai.mistral import Client as MistralClient


class Client(MistralClient):
    def upload(self, path: Path, file_name=None) -> str:
        """
        specific schema is required
        - for [Text & Vision Fine-tuning](https://docs.mistral.ai/capabilities/finetuning/text_vision_finetuning)
        - for [Classifier Factory](https://docs.mistral.ai/capabilities/finetuning/classifier_factory)
        :param path:
        :param file_name:
        :return:
        """
        if not file_name:
            file_name = path.name
        assert file_name.endswith(".jsonl"), "Data must be stored in JSON Lines (.jsonl) files"
        with open(path, "rb") as content:
            res: UploadFileOut = self.client.files.upload(file={
                "file_name": file_name,
                "content": content
            })
        return res.id

    def paginate_files(self, page=0, size=100) -> ListFilesOut:
        return self.client.files.list(page=page, page_size=size)

    def ls(self, page_size=100) -> list[FileSchema]:
        has_next = True
        result = []
        while has_next:
            page = self.paginate_files(size=page_size)
            has_next = page.total == page_size
            result.extend(page.data)
        return result
