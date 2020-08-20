The resources we used for the deployment of the Jupyter notebook were core resources provided with every Kubernetes cluster. These are primitives, and although they can be used in combination to build up complex deployments, require the user to know how to create the resources, or use a higher level template system to ease the management of and working with the resources.

An alternative to working with the core resource types, would be to make use of custom resource definitions, and a purpose built Kubernetes operator which knows how to deploy Jupyter notebooks, to manage the actual deployment.

Using a custom resource, your desire to have a Jupyter notebook deployment could be expressed with a single resource. To see what this resource might look like, run:

```execute
cat notebook-v2/jupyternotebook.yaml
```

The output should be:

```
apiVersion: jupyter-on-kubernetes.test/v1alpha1
kind: JupyterNotebook
metadata:
  name: notebook
```

This custom resource says that we want to create a deployment of a Jupyter notebook called ``notebook`` and that is all. Nothing else needed to be supplied, we did not have to define the five different resources we did previously.

With this custom resource definition, to create the deployment, as with any Kubernetes resource you would run:

```execute
kubectl apply -f notebook-v2/jupyternotebook.yaml
```

Because this is not one of the core Kubernetes resources, one needs to have a custom Kubernetes operator running which responds and performs any appropriate actions when an instance of the resource is created.

In this case, the actions of the operator result in the other resources we previously created manually, being created for us.

```execute
kubectl get all,configmap,pvc,ingress -l app=notebook -o name
```

Since a deployment resource was created, the deployment can still be monitored by running:

```execute
kubectl rollout status deployment/notebook
```

Once the deployment has completed, the Jupyter notebook will be available at:

```dashboard:open-url
url: http://notebook-{{session_namespace}}.{{ingress_domain}}
```

Access to the Jupyter notebook will still be gated by a password, but this time a unique password will be generated for each deployment.

To find out the password for the deployment, run:

```execute
kubectl get jupyternotebooks/notebook
```

You should see output similar to:

```
NAME       URL                                                   PASSWORD
notebook   http://notebook-{{session_namespace}}.{{ingress_domain}}  aAbBcCdDeEfFgGhH
```

You will need to copy the password from the terminal and paste it into the login page of the Jupyter notebook.
