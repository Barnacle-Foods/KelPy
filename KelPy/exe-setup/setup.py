import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
packages = ["onnxruntime","cv2","numpy","torch","PIL", "torchvision", "rasterio"]
includefiles = ['rasterio.libs', 'graphics']

# base="Win32GUI" should be used only for Windows GUI app
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(
    name="KelPy",
    version="0.1",
    description="KelPy",
    author='Chet Russell',
    author_email='chet.barnaclefoods@gmail.com',
    options={"build_exe": {'packages':packages, 'include_files':includefiles}},
    executables=[Executable("main.py", base=base, icon='graphics/bull.ico')],
)