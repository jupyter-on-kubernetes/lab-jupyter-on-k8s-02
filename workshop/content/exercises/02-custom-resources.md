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

Before we can start using this custom resource type we need to register it with the Kubernetes cluster and deploy an operator for handling this type of custom resource. Both these steps would need to be done by a cluster admin of the Kubernetes cluster.

In the case of this workshop you are already a cluster admin of the Kubernetes cluster you are using, so you can do the first step of registering the custom resource type by running:

```terminal:execute
command: kubectl apply -f crds/jupyternotebook.yaml
```

This command registers with the Kubernetes cluster a custom resource definition which describes our custom resource type. The output should be:

```
customresourcedefinition.apiextensions.k8s.io/jupyternotebooks.jupyter-on-kubernetes.test created
```

We still need to deploy an operator, which is just a fancy name for an application or service, which knows how to handle this type of resource. It's job is to respond to instances of the custom resource being created and from that create the core Kubernetes resources to deploy the Jupyter notebook, the same resources we created manually previously.

Normally the operator would be deployed into the same Kubernetes cluster and there is a bit of work involved in doing that in respect of creating a service account and appropriate role based access control (RBAC) configuration specifying what the operator can do in the Kubernetes cluster. For this workshop we will skip that step and run the operator locally within the workshop environment, with it attaching to the Kubernetes cluster using the credentials and corresponding RBAC of the workshop user.

To start the operator in this case run:

```terminal:execute
session: operator
command: INGRESS_SUFFIX={{session_namespace}}.{{ingress_domain}} ~/operator-venv/bin/kopf run --verbose --all-namespaces ~/exercises/operator/handlers.py
```

With the custom resource definition registered and the operator running, to create the deployment of the Jupyter notebook instance, as with any Kubernetes resource you would run:

```execute
kubectl apply -f notebook-v2/jupyternotebook.yaml
```

This should output:

```
jupyternotebook.jupyter-on-kubernetes.test/notebook created
```

As already mentioned the job of the operator is to create the same resources we previously created manually. To see that this has occurred, run:

```execute
kubectl get all,configmap,pvc,ingress -l app=notebook -o name
```

Since a deployment resource was created, the deployment can still be monitored by running:

```execute
kubectl rollout status deployment/notebook
```

Once the deployment has completed, the Jupyter notebook will be available at:

```dashboard:open-url
url: http://notebook-default.{{session_namespace}}.{{ingress_domain}}
```

Access to the Jupyter notebook will still be gated by a password, but this time a unique password will be generated for each deployment.

To find out the password for the deployment, run:

```execute
kubectl get jupyternotebooks/notebook
```

You should see output similar to:

```
NAME       URL                                                   PASSWORD
notebook   http://notebook-default.{{session_namespace}}.{{ingress_domain}}  aAbBcCdDeEfFgGhH
```

You will need to copy the password from the terminal and paste it into the login page of the Jupyter notebook.
