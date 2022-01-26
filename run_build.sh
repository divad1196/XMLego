#!/bin/bash

python3 setup.py sdist bdist_wheel
python3 setup.py install --user
# pip3 install dist/*.whl --force-reinstall