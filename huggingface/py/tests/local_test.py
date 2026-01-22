import os
import unittest
from unittest import skipIf

import onnx
import onnxruntime

from davidkhala.huggingface.local import clone


@skipIf(os.environ.get("CI"), "length test")
class BGETestCase(unittest.TestCase):
    def test_snapshot(self):
        clone('huggingface/bge_m3_model',
                     owner="BAAI",
                     repository="bge-m3",
                     )

    def test_model_validate(self):
        from davidkhala.huggingface.local.BAAI import download_bge_m3
        onnx_path = download_bge_m3('huggingface/bge_m3_model')
        print(onnx_path)
        onnx.checker.check_model(onnx_path)
        # session
        sess_options = onnxruntime.SessionOptions()
        onnxruntime.InferenceSession(onnx_path, sess_options)


if __name__ == '__main__':
    unittest.main()
