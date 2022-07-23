By adding a request for storage in the custom resource for the Jupyter notebook, we were able to have a persistent volume claim made on our behalf and mounted into the container for the Jupyter notebook.

As in the last workshop, this persistent volume was mounted on the home directory ``/home/jovyan``, where a users notebooks and data files would be created or uploaded. A user can install additional Python packages using either ``conda`` or ``pip``, however these packages are installed outside of the home directory of the user into the ``/opt/conda`` directory. Specifically, they were installed into the Anaconda Python base environment. This meant that if the container the Jupyter notebook was running in were restarted, those changes would be lost and the packages would need to be reinstalled.

In order to provide the option of having any installed packages be persistent, the startup script mounted into the container contains steps to allow the Jupyter notebook environment to be switched to an alternate Python virtual environment located in the area of persistent storage under ``/home/jovyan``.

The steps in the startup script which enable this were:

```
conda init

source $HOME/.bashrc

if [ ! -f $HOME/.condarc ]; then
    cat > $HOME/.condarc << EOF
envs_dirs:
  - $HOME/.conda/envs
EOF
fi

if [ -d $HOME/.conda/envs/workspace ]; then
    echo "Activate virtual environment 'workspace'."
    conda activate workspace
fi
```

In order to have the Python virtual environment created under the home directory, the ``$HOME/.condarc`` file was updated to set the ``envs_dir`` configuration so that the directory ``$HOME/.conda/envs`` would be used for any virtual environment created.

Subsequently, if the Python virtual environment directory ``$HOME/.conda/envs/workspace`` existed, this would be activated before starting up the Jupyter notebook.

Initially the Python virtual environment named ``workspace`` would not exist and thus any installed packages would be lost as the base environment would be used. If the user did want to have any additional Python packages installed and had a sufficiently large persistent volume, they could opt in by creating the ``workspace`` environment. This would be done by creating a terminal from the Jupyter notebook web interface and running:

```copy
conda create --name workspace --clone base
```

To have the Jupyter notebook use this environment, the Jupyter notebook would be shutdown from the web interface. This will cause the container to be stopped and restarted. When it restarts, as the directory ``$HOME/.conda/envs/workspace`` now exists, that environment would be activated and used. Any packages that are now subsequently installed, will be stored in the persistent volume mounted into the container and will be retained if the Jupyter notebook container were ever restarted.

That link again for the Jupyter notebook if the browser window or tab is also deleted is:

```dashboard:open-url
url: http://notebook-default.{{session_namespace}}.{{ingress_domain}}
```

Although not enabled by default, this does allow a user to opt in to having everything persistent. It is not done by default in case the persistent volume is not of sufficient size or persistence isn't required. Also, the act of creating the clone of the base environment does take time, as it will need to download all the packages off the internet once again, as they are not cached in the container image. This action would delay startup of the Jupyter notebook the first time giving the impression that it hasn't deployed correctly. As such, it is seen as being better that users actively opt into this arrangement and create the new Python virtual environment themselves.

Do note that the new Python virtual environment must be created as a clone of the base environment using the command shown above, otherwise it will be missing all the packages required for running the Jupyter notebook itself. If this is not done correctly, the whole Jupyter notebook deployment would need to be deleted and a new one created.
