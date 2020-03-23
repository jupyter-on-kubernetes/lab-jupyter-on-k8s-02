This is the second workshop exploring the options for deploying Jupyter notebooks to Kubernetes. The first workshop covered how to deploy Jupyter notebooks locally to your own computer, then moved onto the steps required to deploy to Kubernetes. Topics covered in the prior workshop included authentication, exposing the Jupyter notebook outside of the Kubernetes cluster, and persistent storage for saving any work.

The prior workshop highlighted that although it is technically possible to deploy a Jupyter notebook to Kubernetes, the experience and required steps aren't practical for the majority of Jupyter notebook users, as it entails having access to the Kubernetes cluster, and knowing how to use it to do basic deployments.

One of the issues that made deployment difficult was the need to work with Kubernetes resource objects, of which five different resource types were required

Although it doesn't avoid the need to work with Kubernetes directly, this workshop will explore whether the process could be simplified by using custom resources and an operator designed just for the task of deploying Jupyter notebooks to Kubernetes.

Using this approach the process of deploying the Jupyter notebook can be restricted to knowing about a single custom resource type, with the operator working behind the scenes to do the more complicated work of handling the deployment.
