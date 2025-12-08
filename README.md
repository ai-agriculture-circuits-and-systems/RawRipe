# RawRipe Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#changelog)

A comprehensive dataset of fruit images in both raw and ripe states, designed for fruit maturity recognition tasks. The dataset includes images of 10 different fruit types, enabling various classification approaches from agricultural, market, and automation perspectives.

- Project page: `https://ieeexplore.ieee.org/document/9589215`
- Paper: `docs/Fruit_Maturity_Recognition_from_Agricultural_Market_and_Automation_Perspectives.pdf`

## TL;DR
- Task: classification (with detection annotations)
- Modality: RGB 
- Platform: ground
- Real/Synthetic: real
- Images: 1,630 across 10 fruit types and 2 maturity states (raw/ripe)
- Resolution: variable (original images)
- Annotations: per-image CSV and JSON (COCO-style, full-image bounding boxes); COCO format available
- License: CC BY 4.0 (see License)
- Citation: see below

## Table of contents
- [Download](#download)
- [Dataset structure](#dataset-structure)
- [Sample images](#sample-images)
- [Annotation schema](#annotation-schema)
- [Stats and splits](#stats-and-splits)
- [Quick start](#quick-start)
- [Applications](#applications)
- [Evaluation and baselines](#evaluation-and-baselines)
- [Datasheet (data card)](#datasheet-data-card)
- [Known issues and caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download
- Original dataset: Available through IEEE Xplore (see paper link)
- This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.
- Local license file: see `LICENSE` (Creative Commons Attribution 4.0 International).

## Dataset structure
```
RawRipe/
├── apples/                      # Apple fruit category
│   ├── raw/                     # Raw apple subcategory
│   │   ├── csv/                 # CSV per image
│   │   ├── json/                # JSON per image
│   │   ├── images/              # JPG images
│   │   ├── labelmap.json
│   │   └── sets/                # train.txt / test.txt (plus all.txt, train_val.txt)
│   ├── ripe/                    # Ripe apple subcategory
│   │   ├── csv/
│   │   ├── json/
│   │   ├── images/
│   │   ├── labelmap.json
│   │   └── sets/
│   └── labelmap.json            # Main category labelmap (optional)
├── bananas/                      # Banana fruit category
│   ├── raw/
│   ├── ripe/
│   └── labelmap.json
├── coconuts/                     # Coconut fruit category
├── guavas/                       # Guava fruit category
├── litchis/                      # Litchi fruit category
├── mangoes/                      # Mango fruit category
├── oranges/                      # Orange fruit category
├── papayas/                      # Papaya fruit category
├── pomegranates/                 # Pomegranate fruit category
├── strawberries/                 # Strawberry fruit category
├── annotations/                  # COCO JSON output (generated)
│   ├── apples_raw_instances_train.json
│   ├── apples_raw_instances_test.json
│   ├── apples_ripe_instances_train.json
│   └── ... (more COCO files)
├── scripts/
│   ├── convert_to_coco.py       # conversion utility
│   └── standardize.py           # standardization script
├── data/
│   └── original/                 # Original data directories (preserved for backup)
│       ├── geufruits5_train/
│       └── geufruits5_test/
├── docs/                         # Documentation
│   └── Fruit_Maturity_Recognition_from_Agricultural_Market_and_Automation_Perspectives.pdf
├── LICENSE
├── requirements.txt
└── README.md
```
- Splits: `{fruit_category}/{state}/sets/train.txt`, `{fruit_category}/{state}/sets/test.txt` (and also `all.txt`, `train_val.txt`) list image basenames (no extension). Note: Original dataset only provides train/test splits; validation set is empty.
- Note: This is a classification dataset. Each image has a full-image bounding box annotation for compatibility with detection frameworks.
- Fruit categories: apples, bananas, coconuts, guavas, litchis, mangoes, oranges, papayas, pomegranates, strawberries (10 total)
- Maturity states: raw, ripe (2 states per fruit)

## Sample images

Below are example images from this dataset. Paths are relative to this README location.

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Apple Raw</strong></td>
    <td>
      <img src="apples/raw/images/Apple_Raw_test_27.jpg" alt="Apple raw example" width="200"/>
      <div align="center"><code>apples/raw/images/Apple_Raw_test_27.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Apple Ripe</strong></td>
    <td>
      <img src="apples/ripe/images/Apple_Ripe_train_100.jpg" alt="Apple ripe example" width="200"/>
      <div align="center"><code>apples/ripe/images/Apple_Ripe_train_100.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Banana Raw</strong></td>
    <td>
      <img src="bananas/raw/images/Banana_Raw_train_60.jpg" alt="Banana raw example" width="200"/>
      <div align="center"><code>bananas/raw/images/Banana_Raw_train_60.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Banana Ripe</strong></td>
    <td>
      <img src="bananas/ripe/images/Banana_Ripe_train_100.jpg" alt="Banana ripe example" width="200"/>
      <div align="center"><code>bananas/ripe/images/Banana_Ripe_train_100.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Mango Raw</strong></td>
    <td>
      <img src="mangoes/raw/images/Mango_Raw_train_85.jpg" alt="Mango raw example" width="200"/>
      <div align="center"><code>mangoes/raw/images/Mango_Raw_train_85.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Mango Ripe</strong></td>
    <td>
      <img src="mangoes/ripe/images/Mango_Ripe_train_100.jpg" alt="Mango ripe example" width="200"/>
      <div align="center"><code>mangoes/ripe/images/Mango_Ripe_train_100.jpg</code></div>
    </td>
  </tr>
</table>

## Annotation schema
- CSV per-image schemas (stored under each fruit/state's `csv/` folder):
  - Format: `image_path, x_min, y_min, x_max, y_max, class_name`
  - Full-image bounding boxes: `(0, 0, width, height)` for classification compatibility
- JSON per-image schemas (stored under each fruit/state's `json/` folder):
```json
{
  "info": {
    "description": "RawRipe {fruit} {state} classification dataset",
    "version": "1.0.0",
    "year": 2021,
    "contributor": "...",
    "url": "https://ieeexplore.ieee.org/document/9589215"
  },
  "images": [{
    "id": 1,
    "width": 256,
    "height": 256,
    "file_name": "image.jpg",
    "license": 0
  }],
  "annotations": [{
    "id": 1,
    "image_id": 1,
    "category_id": 1,
    "bbox": [0, 0, 256, 256],
    "area": 65536,
    "iscrowd": 0
  }],
  "categories": [{
    "id": 1,
    "name": "raw",
    "supercategory": "apples"
  }]
}
```
- COCO-style (generated):
```json
{
  "info": {"year": 2021, "version": "1.0.0", "description": "RawRipe {fruit} {state} {split}", "url": "https://ieeexplore.ieee.org/document/9589215"},
  "images": [{"id": 1, "file_name": "apples/raw/images/IMG_0001.jpg", "width": 256, "height": 256}],
  "categories": [{"id": 1, "name": "raw", "supercategory": "apples"}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 1, "bbox": [0, 0, 256, 256], "area": 65536, "iscrowd": 0}]
}
```

- Label maps: each fruit/state folder includes a `labelmap.json` mapping category IDs to names.

## Stats and splits

### Overall Statistics
- **Total Images**: 1,630
- **Training Images**: 1,216
- **Test Images**: 414
- **Fruit Types**: 10
- **Maturity States**: 2 (raw, ripe)
- **Total Subcategories**: 20 (10 fruits × 2 states)

### Per-Fruit Statistics

| Fruit | Raw (Train/Test) | Ripe (Train/Test) | Total |
|-------|------------------|-------------------|-------|
| Apples | 78/27 | 81/27 | 213 |
| Bananas | 63/21 | 86/29 | 199 |
| Coconuts | 54/18 | 58/20 | 150 |
| Guavas | 45/16 | 56/20 | 137 |
| Litchis | 37/13 | 55/19 | 124 |
| Mangoes | 72/25 | 46/16 | 159 |
| Oranges | 48/17 | 54/18 | 137 |
| Papayas | 51/18 | 77/25 | 171 |
| Pomegranates | 58/20 | 57/19 | 154 |
| Strawberries | 65/21 | 75/25 | 186 |

### Splits
- **Train/Test Ratio**: Approximately 75/25
- Splits are provided via `{fruit}/{state}/sets/train.txt` and `{fruit}/{state}/sets/test.txt`
- Note: Original dataset only provides train/test splits; no validation set is provided. The `val.txt` files are empty.

## Quick start

### Python (COCO):
```python
from pycocotools.coco import COCO
coco = COCO("annotations/apples_raw_instances_train.json")
img_ids = coco.getImgIds()
img = coco.loadImgs(img_ids[0])[0]
ann_ids = coco.getAnnIds(imgIds=img['id'])
anns = coco.loadAnns(ann_ids)
```

### Convert CSV to COCO JSON:
```bash
python scripts/convert_to_coco.py --root . --out annotations --splits train test
```

### Standardize Dataset:
```bash
python scripts/standardize.py
```

### Dependencies:
```bash
pip install -r requirements.txt
```

## Applications

This dataset can be used to solve three types of classification problems:

1. **Raw vs Ripe for a specific fruit** (agricultural perspective)
   - Binary classification: Determine if a specific fruit (e.g., apple) is raw or ripe
   - Example: Train on `apples/raw` vs `apples/ripe`

2. **Raw vs Ripe for any fruit** (market perspective)
   - Binary classification: Determine if any fruit is raw or ripe, regardless of fruit type
   - Example: Combine all `raw` subcategories vs all `ripe` subcategories

3. **Multi-class/label classification** (automation perspective)
   - Multi-class classification: Classify both fruit type and maturity state
   - Example: 20 classes (10 fruits × 2 states)

## Evaluation and baselines

- **Task**: Classification (fruit maturity recognition)
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Reference Performance** (from original paper): See paper for baseline results
- **Note**: The original paper presents results for all three classification perspectives mentioned above

## Datasheet (data card)

### Motivation
- **For**: Fruit maturity recognition from agricultural, market, and automation perspectives
- **Existing Solutions**: Manual inspection, traditional computer vision methods
- **Impact**: Automated fruit sorting, quality control in agricultural markets, robotic harvesting

### Composition
- **Instances**: 1,630 images across 10 fruit types and 2 maturity states
- **Collection Process**: Images collected from search engines and agricultural sources
- **Preprocessing**: Images standardized to consistent format; full-image bounding boxes added for detection framework compatibility

### Collection Process
- **Timeframe**: 2021
- **Sources**: Search engines, agricultural databases
- **Collection Method**: Web scraping and manual curation

### Preprocessing/cleaning/labeling
- **Labeling**: Manual annotation of fruit type and maturity state
- **Quality Control**: Images verified for correct fruit type and maturity state
- **Standardization**: Reorganized into standardized structure with consistent naming conventions

### Uses
- **Primary**: Fruit maturity classification
- **Secondary**: Transfer learning, agricultural automation research
- **Out-of-scope**: Object detection (no instance-level annotations), segmentation

### Distribution
- **License**: CC BY 4.0
- **Hosting**: IEEE Xplore (original), this repository (standardized version)
- **Maintenance**: Community-maintained

### Maintenance
- **Who**: Dataset creators and community contributors
- **Update Frequency**: As needed
- **Versioning**: See Changelog section

## Known issues and caveats

1. **No Validation Set**: The original dataset only provides train/test splits. Users may need to split the training set further to create a validation set.
2. **Image Size Variation**: Images have variable resolutions (not standardized to a fixed size).
3. **Limited Samples**: Some fruit/state combinations have relatively few samples (e.g., Litchis raw: 50 images).
4. **Classification Task**: This is a classification dataset. Full-image bounding boxes are provided for compatibility with detection frameworks, but there are no instance-level annotations.
5. **Original Structure**: The original dataset had three different organizational structures (Model 1, Model 2, Model 3). This standardized version uses Model 1 structure as the primary source.

## License

This dataset is licensed under the **Creative Commons Attribution 4.0 International Public License (CC BY 4.0)**.

See `LICENSE` file for the full license text.

**Attribution Requirements:**
- When using this dataset, please cite the original paper (see Citation section)
- Include attribution to the dataset creators: Rao Jerripothula, Koteswar; Kumar Shukla, Sarvesh; Jain, Samyak; Singh, Shudhanshu

## Citation

If you use this dataset in your research, please cite:

```bibtex
@INPROCEEDINGS{9589215,
  author={Rao Jerripothula, Koteswar and Kumar Shukla, Sarvesh and Jain, Samyak and Singh, Shudhanshu},
  booktitle={IECON 2021 – 47th Annual Conference of the IEEE Industrial Electronics Society},
  title={Fruit Maturity Recognition from Agricultural, Market and Automation Perspectives},
  year={2021},
  pages={1-6},
  doi={10.1109/IECON48115.2021.9589215}
}
```

**Paper Link:** https://ieeexplore.ieee.org/document/9589215

## Changelog

### Version 1.0.0 (2024-12-08)
- Initial standardization of RawRipe dataset
- Reorganized data into standardized structure (`{fruit}/{state}/` format)
- Generated per-image CSV and JSON annotations with full-image bounding boxes
- Created dataset splits (train/test) for each fruit/state combination
- Generated COCO format annotations for all subcategories and splits
- Updated README.md with comprehensive documentation
- Added LICENSE file (CC BY 4.0)
- Created requirements.txt
- Moved original data to `data/original/` for backup

## Contact

For questions or issues related to this standardized dataset:
- **Original Dataset Authors**: See paper for contact information
- **Standardization**: This standardized version is maintained by the community

For questions about the original dataset, please refer to the original paper or IEEE Xplore.
