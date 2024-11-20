#!/bin/bash

# note that if this says 'permission denied' in bash run:
# chmod +x run_local_build.sh

# step 0: Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# step 1: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# step 2: unit tests
echo "Running unit tests..."
pip install pytest
pytest .

# step 3: Run the notebooks using nbconvert
echo "Running notebooks..."
for notebook in notebooks/*.ipynb; do
    echo "Running $notebook..."
    jupyter nbconvert --to html --execute "$notebook" --output-dir outputs/notebooks
done

# step 4: Run simulation
echo "Running simulation..."
# #TODO: add simulation command here

# step 5:
# Move the generated png files to the images folder
echo "Moving png files to images folder..."
mv outputs/plots/*.png PelicanWebsite/content/img/



