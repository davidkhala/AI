import os
import unittest
from unittest import skipIf
from davidkhala.huggingface.transformers import Pipeline
from davidkhala.huggingface.transformers.auto import Model

@skipIf(os.environ.get('CI'), 'Length operation')
class PipelineTestCase(unittest.TestCase):
    def test_sample(self):
        """
        Use a pipeline as a high-level helper
        """

        p = Pipeline("text-generation", "Qwen/Qwen2.5-1.5B")
        r = p.call("the secret to baking a really good cake is ")
        print(list(r))


class AutoModelTestCase(unittest.TestCase):
    def test_sample(self):
        model = Model.load("Qwen/Qwen2.5-1.5B")

@skipIf(os.environ.get('CI'), 'experiment')
class DSOCRTest(unittest.TestCase):
    def test_setup(self):
        from transformers import AutoModel, AutoTokenizer
        import torch
        import os
        os.environ["CUDA_VISIBLE_DEVICES"] = '0'
        model_name = 'deepseek-ai/DeepSeek-OCR'

        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModel.from_pretrained(model_name, _attn_implementation='flash_attention_2', trust_remote_code=True,
                                          use_safetensors=True)
        # TODO
        # You are using a model of type deepseek_vl_v2 to instantiate a model of type DeepseekOCR. This is not supported for all configurations of models and can yield errors.
        # Some weights of DeepseekOCRForCausalLM were not initialized from the model checkpoint at deepseek-ai/DeepSeek-OCR and are newly initialized: ['model.vision_model.embeddings.position_ids']
        # You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.



if __name__ == '__main__':
    unittest.main()
