# Kelpy unit tests
# File created: 7/11/2023
# Author: Chet Russell
# Last edited: 7/11/2023 - Chet Russell

import unittest
import tempfile
import shutil
import os

import core
import gui

cwd = os.getcwd()  # Get the current working directory (cwd)


class UnitTests(unittest.TestCase):
    # This function tests the masker function in core.py
    # It essentially checks if it generates an identical mask with the given example image in the test_imgs folder
    def test_masker(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            shutil.copy(cwd + "\\test_imgs\\glint_test.JPG", tmpdirname)
            core.masker(tmpdirname, 5)
            with open(cwd + "\\test_imgs\\glint_test_mask.JPG", "rb") as img:
                with open(tmpdirname + "\\glint_test_mask.JPG", "rb") as img_msk:
                    self.assertEqual(img.read(), img_msk.read())


if __name__ == "__main__":
    unittest.main()
