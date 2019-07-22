#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import phash

TEST_IMAGES = {
    "simple": [
        os.path.join(os.path.dirname(__file__), "images", "simple-test-1.png"),
        os.path.join(os.path.dirname(__file__), "images", "simple-test-2.png"),
    ]
}


class TestPhash(unittest.TestCase):
    def test_digest(self):
        self.assertIsNone(None, phash.image_digest(TEST_IMAGES["simple"][0]))

    def test_correlation(self):
        digest_1 = phash.image_digest(TEST_IMAGES["simple"][0])
        digest_2 = phash.image_digest(TEST_IMAGES["simple"][1])

        pcc = phash.cross_correlation(digest_1, digest_2)

        self.assertAlmostEqual(0, pcc)


if __name__ == "__main__":
    unittest.main()
