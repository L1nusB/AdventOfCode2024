#!/bin/bash
conda create -n codespace numpy scipy matplotlib pandas -y
echo "conda activate codespace" >> ~/.bashrc