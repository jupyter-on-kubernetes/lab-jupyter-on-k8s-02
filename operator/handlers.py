import os
import random
import hashlib
import string

import kopf
import kubernetes
import kubernetes.client


@kopf.on.create("jupyter-on-kubernetes.test", "v1alpha1", "jupyternotebooks")
def create(name, uid, namespace, spec, logger, **_):
    apps_api = kubernetes.client.AppsV1Api()
    core_api = kubernetes.client.CoreV1Api()
    extensions_api = kubernetes.client.ExtensionsV1beta1Api()

    algorithm = 'sha1'
    salt_len = 12

    h = hashlib.new(algorithm)
    salt = ('%0' + str(salt_len) + 'x') % random.getrandbits(4 * salt_len)
    h.update(bytes(passphrase, 'utf-8') + salt.encode('ascii'))

    password_hash = ':'.join((algorithm, salt, h.hexdigest()))

    config_map_body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": name,
            "labels": {
                "app": name
            }
        }
        "data": {
            "jupyter_notebook_config.json" : f"""
                {
                  "NotebookApp": {
                    "password": {password_hash}
                  }
                }
            """
        }
    }

    kopf.adopt(config_map_body)

    core_api.create_namespaced_config_map(namespace=namespace, body=config_map_body)

    image = spec.get("image", "jupyter/minimal-notebook:latest")
    service_account = spec.get("serviceAccountName", "default")

    memory_limit = spec.get("resources", {}).get("limits", {}).get("memory", "512Mi")
    memory_request = spec.get("resources", {}).get("requests", {}).get("memory", memory_limit)

    deployment_body = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name,
            "labels": {
                "app": name
            }
        }
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "deployment": name
                }
            },
            "strategy": {
                "type": "Recreate"
            },
            "template": {
                "metadata": {
                    "labels": {
                        "deployment": name
                    }
                }
                "spec": {
                    "serviceAccountName": service_account,
                    "containers": [
                        {
                            "name": "notebook",
                            "image": image,
                            "imagePullPolicy": "Always",
                            "resources": {
                                "requests": {
                                    "memory": memory_request
                                },
                                "limits": {
                                    "memory": memory_limit
                                }
                            },
                            "ports": [
                                {
                                    "name": "8888-tcp",
                                    "containerPort": 8888,
                                    "protocol": "TCP",
                                }
                            ],
                            "env": [
                                {
                                    "name": "JUPYTER_ENABLE_LAB",
                                    "value": "true",
                                },
                            ],
                        },
                        "volumeMounts": [
                            {
                                "name": "config",
                                "mountPath": "/home/jovyan/.jupyter"
                            }
                        ]
                    ],
                    "volumes": [
                        {
                            "name": "config",
                            "configMap": "notebook"
                        }
                    ]
                },
            },
        },
    }

    kopf.adopt(deployment_body)

    apps_api.create_namespaced_deployment(namespace=namespace, body=deployment_body)

    service_body = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": name,
            "labels": {
                "app": name
            }
        }
        "spec": {
            "type": "ClusterIP",
            "ports": [
                {
                    "name": "8888-tcp",
                    "port": 8888,
                    "protocol": "TCP",
                    "targetPort": 8888,
                }
            ],
            "selector": {
                "deployment": name
            },
        },
    }

    kopf.adopt(service_body)

    core_api.create_namespaced_service(namespace=namespace, body=service_body)

    ingress_domain = os.environ.get("INGRESS_DOMAIN")
    ingress_hostname = f"notebook-{namespace}.{ingress_domain}")

    ingress_body = {
        "apiVersion": "extensions/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "name": name,
            "labels": {
                "app": name
            }
        },
        "spec": {
            "rules": {
                "host": ingress_hostname,
                "http": {
                    "paths": [
                        {
                            "path": "/",
                            "backend": {
                                "serviceName": name,
                                "servicePort": 8888,
                            },
                        }
                    ]
                }
            }
        }
    }

    kopf.adopt(ingress_body)

    extensions_api.create_namespaced_ingress(namespace=namespace, body=ingress_body)

    return {
      "url": f"http://{ingress_hostname}",
      "password": password_hash
    }
