FROM continuumio/miniconda3:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optional: Create a new environment
# Uncomment and modify the following lines to create a specific environment
# COPY environment.yml .
# RUN conda env create -f environment.yml

# Set up conda to automatically activate base environment
RUN conda init bash

# Optional: Install additional conda packages in base environment
RUN conda install -y \
    numpy \
    pandas \
    matplotlib \
    jupyter

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]
