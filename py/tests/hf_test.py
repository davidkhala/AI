import os
import unittest

import onnx
import onnxruntime

from davidkhala.ai.huggingface import clone
from davidkhala.ai.huggingface.inference import API


class BGETestCase(unittest.TestCase):
    def test_snapshot(self):
        r = clone('huggingface/bge_m3_model',
              owner="BAAI",
              repository="bge-m3",
              )
        print()
        print('r', r, type(r))
        return r

    def test_model_validate(self):

        from davidkhala.ai.huggingface.BAAI import bge_m3_path
        onnx_path= bge_m3_path('huggingface/bge_m3_model')
        print(onnx_path)

        with self.assertRaises(ValueError) as e:
            onnx_model = onnx.load("huggingface/bge_m3_model/onnx/model.onnx")
            onnx.checker.check_model(onnx_model)
        self.assertEqual('This protobuf of onnx model is too large (>2GiB). Call check_model with model path instead.', str(e.exception))
        onnx.checker.check_model("huggingface/bge_m3_model/onnx/model.onnx")

    def test_session(self):
        from davidkhala.ai.huggingface.BAAI import bge_m3_path
        onnx_path = bge_m3_path('huggingface/bge_m3_model')
        sess_options = onnxruntime.SessionOptions()
        onnxruntime.InferenceSession(onnx_path, sess_options)


class InferenceTestCase(unittest.TestCase):
    def test_sample(self):
        token = os.environ.get('PAT')
        i = API(token)
        i.as_model("google-bert/bert-base-uncased")
        r = i.call(inputs = "The goal of life is [MASK].", raw_response=True)
        print(r) # FIXME always 404


if __name__ == '__main__':
    unittest.main()
