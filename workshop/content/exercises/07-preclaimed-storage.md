When the persistent storage was requested, it was associated with this specific Jupyter notebook deployment. If you delete the custom resource for the Jupyter notebook deployment, both the deployment and the persistent volume claim would be deleted. You would thus loose any work you had done if you had not downloaded your notebooks and data files.

To support being able to retain persistent storage across deployments, you can instead pre claim a persistent volume and tell a deployment to use that persistent storage. To view the persistent volume claim for this, run:

```execute
cat notebook-v4/persistentvolumeclaim.yaml
```

The output should be:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: workspaces
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

The name of the persistent volume claim we have used is ``workspaces``.

To view the custom resource for the Jupyter notebook deployment setup to use this, run:

```execute
cat notebook-v4/jupyternotebook.yaml
```

This should be:

```
apiVersion: jupyter-on-kubernetes.test/v1alpha1
kind: JupyterNotebook
metadata:
  name: notebook
spec:
  storage:
    claimName: workspaces
    subPath: workspace-1
```

Instead of specifying a size for request storage, we instead provide a separate section for storage which lists the name of the existing persistent volume claim. Although not required, we have also listed a ``subPath`` within the persistent volume to be used for this Jupyter notebook deployment.

Before we try this variation, delete the existing Jupyter notebook deployment by running:

```execute
kubectl delete jupyternotebook/notebook --cascade=foreground
```

Make sure all the resources have been deleted by running:

```execute
kubectl get all,configmap,pvc,ingress -l app=notebook -o name
```

To create the persistent volume claim we require, now run:

```execute
kubectl apply -f notebook-v4/persistentvolumeclaim.yaml
```

With the claim created, you can then create the new Jupyter notebook deployment by running:

```execute
kubectl apply -f notebook-v4/jupyternotebook.yaml
```

Wait for the deployment to finish:

```execute
kubectl rollout status deployment/notebook
```

List the details for accessing the Jupyter notebook instance:

```execute
kubectl get jupyternotebook/notebook
```

and access the Jupyter notebook by clicking on:

```dashboard:open-url
url: http://notebook-{{session_namespace}}.{{ingress_domain}}
```

Use the password displayed above with the details for accessing the Jupyter notebook instance.

Key with this variation is that when you delete the Jupyter notebook deployment by deleting the custom resource, the persistent volume claim will not be deleted. This means you can create a new deployment using the same persistent volume claim name and reattach to the same persistent storage, with all your notebooks and data files intact. This would allow you for example to delete a deployment, increase the memory allocated, and create a new deployment with all your work still available.

Delete the Jupyter notebook deployment by running:

```execute
kubectl delete jupyternotebook/notebook --cascade=foreground
```

Now verify that the persistent volume claim still exists.

```execute
kubectl get persistentvolumeclaims
```

If you want, recreate the Jupyter notebook deployment again to check that the same persistent volume is used.

There are a couple of other tricks you can also do.

In this case we specified the ``subPath`` within the persistent volume to use for the deployment. If this wasn't done, then the root of the persistent volume would be used.

By specifying a subpath, the persistent volume can be divided up, with different sub directories for each of the Jupyter notebook deployments, where more than one is created.

In this case since the storage type was ``ReadWriteOnce``, you would only be able to have one active Jupyter notebook deployment at a time using the persistent storage, but if you have storage available of type ``ReadWriteMany``, then you could have multiple deployments with different names running at the same time, sharing the same persistent storage, but with files located in different directories. So long as the sub paths were not overlapping, you would not be able to see files from one deployment from another deployment.

That said, if you were using separate sub paths in the persistent storage for different deployments, you could also create a deployment where no subpath was specified, which would allow you to see files from all deployments using a subpath, at the same time. This could be handy for moving files between the directories for the respective deployments.
