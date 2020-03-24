import os
import random
import string

import kopf
import kubernetes
import kubernetes.client


@kopf.on.create("jupyter-on-kubernetes.test", "v1alpha1", "jupyternotebooks")
def create(name, uid, namespace, spec, logger, **_):
    custom_objects_api = kubernetes.client.CustomObjectsApi()

    return {
      "url": "http://example.com",
      "password": "password"
    }
