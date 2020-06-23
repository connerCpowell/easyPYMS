#!/usr/bin/env bash

virtualenv -p python2.7 venv2p7 && . venv2p7/bin/activate && pip install -r requirements.txt && cd Pycluster-1.50 && python setup.py install
