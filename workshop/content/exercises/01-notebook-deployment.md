In the previous workshop we derived a solution for deploying a Jupyter notebook, including the ability to have persistent storage.

To see the resource files from that workshop run:

```execute
ls notebook-v1/*.yaml
```

The directory should include the files:

```
notebook-v1/configmap.yaml
notebook-v1/persistentvolumeclaim.yaml
notebook-v1/deployment.yaml
notebook-v1/service.yaml
notebook-v1/ingress.yaml
```

The config map included the ``jupyter_notebook_config.json`` file and was used to set the password for accessing the Jupyter notebook application.

```execute
cat notebook-v1/configmap.yaml
```

The remaining resource files were a persistent volume claim, deployment, service and ingress.

To deploy a Jupyter notebook application using these resource files, run:

```execute
kubectl apply -f notebook-v1
```

Monitor the deployment by running:

```execute
kubectl rollout status deployment/notebook
```

If this is the first time the container image is being used in the Kubernetes cluster, because the Jupyter notebook images can be quite large, it may take some time to pull down the image and deploy it.

Once the deployment has completed, the Jupyter notebook will be available at:

%ingress_protocol%://notebook-%session_namespace%.%ingress_domain%/

The password for the Jupyter notebook will be:

```copy
jupyter
```

When done verifying the deployment worked, delete all the resources created by running:

```execute
kubectl delete all,configmap,pvc,ingress -l all
```
