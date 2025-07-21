# RawRipe Dataset

A comprehensive dataset of fruit images in both raw and ripe states, designed for fruit maturity recognition tasks. The dataset includes images of 10 different fruit types, enabling various classification approaches from agricultural, market, and automation perspectives.

## Dataset Description

The RawRipe Dataset contains images of fruits in both raw and ripe states, collected for research in fruit maturity recognition. This dataset is specifically designed for computer vision and deep learning applications in agricultural detection and classification tasks.

### Data Summary

The dataset includes 10 types of fruits:
- Apple
- Banana
- Coconut
- Guava
- Litchi
- Mango
- Orange
- Papaya
- Pomegranate
- Strawberry

Each fruit is represented in both raw and ripe states.

## Database Structure

The dataset is organized into training and test sets, each with three classification perspectives (Model 1, Model 2, Model 3):

```
geufruits5_train/
  ├── Model 1/
  │   ├── Apple/
  │   │   ├── Raw/
  │   │   └── Ripe/
  │   ├── Banana/
  │   │   ├── Raw/
  │   │   └── Ripe/
  │   └── ... (other fruits)
  ├── Model 2/
  │   ├── Raw/
  │   └── Ripe/
  └── Model 3/
      ├── Apple_Raw/
      ├── Apple_Ripe/
      ├── Banana_Raw/
      ├── Banana_Ripe/
      └── ... (other fruit-state combinations)
```
The same structure applies to `geufruits5_test/`.

- **Model 1:** Each fruit has its own folder, with subfolders for "Raw" and "Ripe" images.
- **Model 2:** All "Raw" images and all "Ripe" images are grouped together, regardless of fruit type.
- **Model 3:** Each combination of fruit and maturity state (e.g., Apple_Raw, Banana_Ripe) has its own folder.

## JSON Annotation Format

For each image, a JSON annotation file with the same name as the image is provided in the same directory. The annotation format is as follows:

```json
{
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
      "id": "10-digit unique id",
      "width": null,
      "height": null,
      "file_name": "image_name.jpg",
      "size": null,
      "format": "JPG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [],
  "categories": [
    {
      "id": "10-digit unique id (same for the same category across all files)",
      "name": "Fruit_Ripeness (e.g., Apple_Ripe)",
      "supercategory": "Fruit (e.g., Apple)"
    }
  ]
}
```
- The `id` fields are 10-digit strings. For categories, the last 3 digits are derived from the timestamp at generation time, and the first 7 digits are a unique index for each category (with leading zeros).
- The `categories` field describes the fruit and its maturity state.
- The `annotations` field is empty, as there are no bounding boxes or segmentation labels in this dataset.

## Applications

This dataset can be used to solve three types of classification problems:

1. Raw vs Ripe for a specific fruit (agricultural perspective)
2. Raw vs Ripe for any fruit (market perspective)
3. Multi-class/label classification (automation perspective)

## Citation

When using this dataset in your research, please cite:

```
@INPROCEEDINGS{9589215,
  author={Rao Jerripothula, Koteswar and Kumar Shukla, Sarvesh and Jain, Samyak and Singh, Shudhanshu},
  booktitle={IECON 2021 – 47th Annual Conference of the IEEE Industrial Electronics Society},
  title={Fruit Maturity Recognition from Agricultural, Market and Automation Perspectives},
  year={2021},
  pages={1-6},
  doi={10.1109/IECON48115.2021.9589215}
}
```

## Paper Reference

For more details, refer to the paper:
"Fruit Maturity Recognition from Agricultural, Market and Automation Perspectives" (IECON'21)

Paper link: https://ieeexplore.ieee.org/document/9589215

## Categories

- Computer Science
- Artificial Intelligence
- Computer Vision
- Object Classification
- Machine Learning
- Agriculture
- Deep Learning
- Fruit Recognition
- Maturity Detection 