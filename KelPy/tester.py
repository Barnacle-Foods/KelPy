# Kelpy unit tests
# File created: 7/11/2023
# Author: Chet Russell
# Last edited: 7/11/2023 - Chet Russell

import unittest
import tempfile
import shutil
import os
import filecmp

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

    # def test_ortho(self):
    #    self.assertFalse(core.orthorec("", "", "high", 0, False, "sift", False, True))

    # This function tests the write_yaml_to_file function in core.py
    # All this does is create two identical yaml files, then runs the function, then checks if they are the same
    def test_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(tmpdirname + "\\test1.yaml", "w") as f:
                pass
            with open(tmpdirname + "\\test2.yaml", "w") as f:
                pass
            data = {
                "This is test": 1,
            }
            core.write_yaml_to_file(data, tmpdirname + "\\test2")
            self.assertFalse(
                filecmp.cmp(tmpdirname + "\\test1.yaml", tmpdirname + "\\test2.yaml")
            )


if __name__ == "__main__":
    unittest.main()
