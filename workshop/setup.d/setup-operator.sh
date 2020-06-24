#!/bin/bash

if [ x"$KUBERNETES_SERVICE_HOST" != x"" ]; then
    if [ ! -d operator-venv/bin/activate ]; then
        python3 -m venv operator-venv
        source operator-venv/bin/activate
        pip install -r exercises/operator/requirements.txt
    fi
fi
