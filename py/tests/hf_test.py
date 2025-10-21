import unittest

from davidkhala.ai.huggingface import clone


class DownloadTestCase(unittest.TestCase):
    def test_snapshot(self):
        r = clone('bge_m3_model',
              owner="BAAI",
              repository="bge-m3",
              )
        print()
        print('r', r, type(r))




if __name__ == '__main__':
    unittest.main()
