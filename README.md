## Setup
- Install miniconda (https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)
- `conda create --name myenv python=3.11`
- `python -m pip install "kivy[base]" kivy_examples` (or any from here https://kivy.org/doc/stable/gettingstarted/installation.html#install-pip)


## Building with PyInstaller
- `pip install pyinstaller`
- In root folder, `python -m PyInstaller --name json_parser main.py`
- Copy out the `dist` folder and execute by pressing the `.exe` file inside
- Before rebuilding with `PyInstaller`, delete the `dist` and `build` folders.

## Building with Android (Untested)
https://kivy.org/doc/stable/guide/packaging-android.html