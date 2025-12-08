import os
import json
import random
import time
from glob import glob

# Supported image extensions
IMG_EXTS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']

# Root directories
ROOTS = [
    'geufruits5_train/Model 1', 'geufruits5_train/Model 2', 'geufruits5_train/Model 3',
    'geufruits5_test/Model 1', 'geufruits5_test/Model 2', 'geufruits5_test/Model 3'
]

# Generate a 10-digit id: first 7 digits random, last 3 digits are the last 3 of the current timestamp
def gen_id():
    rand_part = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    ts_part = str(int(time.time()))[-3:]
    return int(rand_part + ts_part)

# Check if file is an image
def is_image_file(filename):
    return any(filename.endswith(ext) for ext in IMG_EXTS)

# Get category name (fruit + ripeness)
def get_category_name(path, model):
    # Model 1: .../fruit/ripeness/image
    # Model 2: .../ripeness/image (fruit name in filename)
    # Model 3: .../fruit_ripeness/image
    parts = os.path.normpath(path).split(os.sep)
    if model == 'Model 1':
        fruit = parts[-3]
        ripeness = parts[-2]
        return f'{fruit}_{ripeness}'
    elif model == 'Model 2':
        ripeness = parts[-2]
        fname = os.path.basename(path)
        fruit = fname.split('_')[0]
        return f'{fruit}_{ripeness}'
    elif model == 'Model 3':
        fruit_ripeness = parts[-2]
        return fruit_ripeness
    else:
        return 'Unknown'

# Get all image paths
def get_all_images(root, model):
    img_paths = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if is_image_file(fname):
                img_paths.append(os.path.join(dirpath, fname))
    return img_paths

# Scan all images and collect unique categories
def collect_all_categories():
    categories = set()
    img_info = []  # (img_path, model, category_name)
    for root in ROOTS:
        model = os.path.basename(root)
        img_paths = get_all_images(root, model)
        for img_path in img_paths:
            category_name = get_category_name(img_path, model)
            categories.add(category_name)
            img_info.append((img_path, model, category_name))
    return sorted(categories), img_info

# Assign a unique id to each category (10-digit string, leading zeros, last 3 are timestamp)
def assign_category_ids(categories):
    base_ts = str(int(time.time()))[-3:]
    cat2id = {}
    for idx, cat in enumerate(categories):
        cat2id[cat] = f'{idx:07d}{base_ts}'  # always 10 digits as string
    return cat2id

# Main process
def main():
    categories, img_info = collect_all_categories()
    cat2id = assign_category_ids(categories)
    for img_path, model, category_name in img_info:
        img_name = os.path.basename(img_path)
        json_name = os.path.splitext(img_name)[0] + '.json'
        # Only image filename is available, width/height can be filled later if needed
        json_data = {
            "info": {
                "description": "data",
                "version": "1.0",
                "year": 2025,
                "contributor": "search engine",
                "source": "no_augmentation",
                "license": {
                    "name": "Creative Commons Attribution 4.0 International",
                    "url": "https://creativecommons.org/licenses/by/4.0/"
                }
            },
            "images": [
                {
                    "id": gen_id(),
                    "width": None,
                    "height": None,
                    "file_name": img_name,
                    "size": None,
                    "format": os.path.splitext(img_name)[1][1:].upper(),
                    "url": "",
                    "hash": "",
                    "status": "success"
                }
            ],
            "annotations": [],
            "categories": [
                {
                    "id": cat2id[category_name],
                    "name": category_name,
                    "supercategory": category_name.split('_')[0]
                }
            ]
        }
        # Save json
        json_path = os.path.join(os.path.dirname(img_path), json_name)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f'Generated: {json_path}')

if __name__ == '__main__':
    main() 