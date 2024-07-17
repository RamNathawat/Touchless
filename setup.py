from setuptools import setup

APP = ['Casual-Touch.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['numpy', 'scipy', 'PIL', 'opencv-python', 'pyobjc-core', 'pyobjc-framework-Cocoa',
                 'pyobjc-framework-Quartz', 'Pillow', 'python-dateutil', 'PyRect', 'PyMsgBox',
                 'PyScreeze', 'pyautogui', 'MouseInfo', 'fonttools', 'rubicon-objc', 'absl-py',
                 'opt-einsum', 'ml-dtypes', 'protobuf', 'matplotlib', 'cffi', 'jax', 'jaxlib',
                 'mediapipe'],
    'includes': ['pyobjc-framework-Cocoa', 'pyobjc-framework-Quartz', 'pyobjc-core', 'Pillow',
                 'python-dateutil', 'PyRect', 'PyMsgBox', 'PyScreeze', 'pyautogui', 'MouseInfo',
                 'fonttools', 'rubicon-objc', 'absl-py', 'opt-einsum', 'ml-dtypes', 'protobuf',
                 'matplotlib', 'cffi', 'jax', 'jaxlib', 'numpy', 'scipy', 'mediapipe'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
