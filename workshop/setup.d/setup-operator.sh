#!/bin/bash

if [ x"$KUBERNETES_SERVICE_HOST" != x"" ]; then
    if [ ! -d operator/bin/activate ]; then
        python3 -m venv operator
        source operator/bin/activate
        pip install operator/requirements.txt
    fi
fi
