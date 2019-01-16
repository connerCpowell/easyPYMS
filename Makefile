install:
    virtualenv -p python2.7 venv && . venv/bin/activate && pip install -r requirements.txt && cd Pycluster-1.50 && python setup.py install

