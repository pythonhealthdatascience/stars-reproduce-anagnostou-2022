# Source: https://github.com/TomMonks/treatment-centre-sim/blob/main/Dockerfile

# Use publicly available Linux-Miniconda image
# start with miniconda image
FROM continuumio/miniconda3:latest

# Create and set the working directory to the container make copy simpler
RUN mkdir /home/code
WORKDIR /home/code

# Copy all files across to container
COPY ./reproduction /home/code

# Copy jupyter config file
COPY ./reproduction/docker/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# Install anaconda, conda-forge and pip dependencies
RUN conda update conda && conda env create -f environment.yml && conda clean -afy 

# Make RUN commands use the new environment (not really necessary here)...
SHELL ["conda", "run", "-n", "anagnostou2022", "/bin/bash", "-c"]

# Declare port used by jupyter-lab
EXPOSE 80

# Launch JupyterLab
CMD jupyter-lab /home/code/