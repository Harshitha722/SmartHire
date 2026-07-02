import os

directories = [
    "backend/app/routes",
    "backend/app/controllers",
    "backend/app/models",
    "backend/app/services",
    "backend/app/ml",
    "backend/app/database",
    "backend/app/utils",
    "backend/uploads",
    "dataset",
    "trained_models"
]

for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    
print("Directories created successfully!")
