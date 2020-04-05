The custom resource we used only said that we wanted a Jupyter notebook deployed. It did not saying anything about the container image to be used, or what resources to allocate. In the most basic deployment, we wouldn't actually care, and as such, these details were filled in by the operator.

To see what additional properties were used for the deployment, run:

```execute
kubectl describe jupyternotebook/notebook
```

Scroll through the output, and you will find a status section which looks similar to the following:

```
Status:
  Jupyter:
    Deployment:
      Image:  jupyter/minimal-notebook:latest
      Resources:
        Limits:
          Memory:   512Mi
          Storage:
        Requests:
          Memory:            512Mi
          Storage:
      Service Account Name:  default
    Notebook:
      Interface:  lab
      Password:   aAbBcCdDeEfFgGhH
      URL:        http://notebook-%session_namespace%.%ingress_domain%
    Storage:
      Claim Name:
      Sub Path:
```

As you can see, the operator used the ``jupyter/minimal-notebook`` image from the set of official Jupyter notebook images from the Jupyter project. It also specified that 512Mi of memory be allocated to run the Jupyter notebook and that the deployment be run using the ``default`` service account in the namespace.

Although filled in by the operator if not supplied, you could still override them if need be. You just need to fill in the appropriate property values in the custom resource.

To see an example of the custom resource with the properties explicitly set, run:

```execute
cat notebook-v3/jupyternotebook.yaml
```

This should yield the output:

```
apiVersion: jupyter-on-kubernetes.test/v1alpha1
kind: JupyterNotebook
metadata:
  name: notebook
spec:
  notebook:
    interface: lab
  deployment:
    image: jupyter/minimal-notebook
    serviceAccountName: default
    resources:
      requests:
        storage: 5Gi
      limits:
        memory: 512Mi
```

Before attempting to deploy this notebook, first delete the existing deployment by running:

```execute
kubectl delete jupyternotebook/notebook
```

You will note here that we did not have to explicitly list the other resources which were created. This is because the custom resource object we created acted as the owner of the other resources. As such, when the custom resource object was deleted, the other resources were automatically deleted, and we did not have to worry about what they were.

Make sure all the resources have been deleted by running:

```execute
kubectl get all,configmap,pvc,ingress -l app=notebook -o name
```

When they have been deleted, create a Jupyter notebook using the new custom resource.

```execute
kubectl apply -f notebook-v3/jupyternotebook.yaml
```

List the resources created in this case by running:

```execute
kubectl get all,configmap,pvc,ingress -l app=notebook -o name
```

You will see this time that an additional resource was created for a ``persistentvolumeclaim``. This is because the default case is that persistent storage would not be provided. As a storage request was made this time, storage was allocated and mounted into the Jupyter notebook deployment. This request for persistent storage is also reflected in the status captured in the custom resource.

```execute
kubectl describe jupyternotebook/notebook
```

This shows the utility of using a custom resource, in that in can apply defaults, but also allow you to optionally enable additional capabilities. The operator will then worry about the actual details as to what resources are required and how to configure them.
