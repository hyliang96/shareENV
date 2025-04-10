#!/bin/bash

if [ -d "$conda_path/bin" ]; then
    PATH=$conda_path/bin:$PATH nvim "$@"
else
    nvim "$@"
fi


