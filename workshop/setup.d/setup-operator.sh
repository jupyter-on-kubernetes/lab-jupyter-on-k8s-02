#!/bin/bash

if [ ! -d operator-venv/bin/activate ]; then
    python3 -m venv operator-venv
    source operator-venv/bin/activate
    pip install -r exercises/operator/requirements.txt
fi
