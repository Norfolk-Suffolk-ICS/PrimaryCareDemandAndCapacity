#!/bin/bash
cd ./notebooks
# Execute all .ipynb notebooks in the current directory in-place
export PYDEVD_DISABLE_FILE_VALIDATION=1

for nb in *.ipynb; do
  echo "Executing notebook: $nb"
    jupyter nbconvert --execute --inplace "$nb"
done


echo "All notebooks executed successfully."
