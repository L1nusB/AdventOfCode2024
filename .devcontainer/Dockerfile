FROM continuumio/miniconda3:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and create the custom environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Set up conda to automatically activate
RUN conda init bash

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]
