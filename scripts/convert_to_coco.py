#!/usr/bin/env python3
"""
Convert RawRipe dataset annotations to COCO JSON format.
Based on the standardized dataset structure specification.
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image

def read_split_list(split_file: Path) -> List[str]:
    """Read image base names (without extension) from a split file."""
    if not split_file.exists():
        return []
    lines = [line.strip() for line in split_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]

def image_size(image_path: Path) -> Tuple[int, int]:
    """Return (width, height) for an image path using PIL."""
    with Image.open(image_path) as img:
        return img.width, img.height

def parse_csv_boxes(csv_path: Path) -> List[Dict]:
    """Parse a single CSV file and return bounding boxes."""
    if not csv_path.exists():
        return []
    
    boxes = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                x_min = float(row.get('x_min', 0))
                y_min = float(row.get('y_min', 0))
                x_max = float(row.get('x_max', 0))
                y_max = float(row.get('y_max', 0))
                
                width = x_max - x_min
                height = y_max - y_min
                
                if width > 0 and height > 0:
                    boxes.append({
                        'bbox': [x_min, y_min, width, height],
                        'area': width * height,
                        'category_id': 1  # 分类任务只有一个类别
                    })
            except (ValueError, KeyError):
                continue
    
    return boxes

def collect_annotations_for_split(
    subcategory_root: Path,
    split: str,
    category_name: str,
    subcategory_name: str,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Collect COCO dictionaries for images, annotations, and categories."""
    images_dir = subcategory_root / "images"
    annotations_dir = subcategory_root / "csv"
    sets_dir = subcategory_root / "sets"
    
    split_file = sets_dir / f"{split}.txt"
    image_stems = set(read_split_list(split_file))
    
    if not image_stems:
        # Fall back to all images if no split file
        image_stems = {p.stem for p in images_dir.glob("*.jpg")}
        image_stems.update({p.stem for p in images_dir.glob("*.JPG")})
        image_stems.update({p.stem for p in images_dir.glob("*.png")})
    
    images: List[Dict] = []
    anns: List[Dict] = []
    
    categories: List[Dict] = [
        {"id": 1, "name": subcategory_name, "supercategory": category_name}
    ]
    
    image_id_counter = 1
    ann_id_counter = 1
    
    for stem in sorted(image_stems):
        img_path = None
        for ext in ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG']:
            potential_path = images_dir / f"{stem}{ext}"
            if potential_path.exists():
                img_path = potential_path
                break
        
        if not img_path or not img_path.exists():
            continue
        
        width, height = image_size(img_path)
        images.append({
            "id": image_id_counter,
            "file_name": f"{category_name}/{subcategory_name}/images/{img_path.name}",
            "width": width,
            "height": height,
        })
        
        csv_path = annotations_dir / f"{stem}.csv"
        boxes = parse_csv_boxes(csv_path)
        
        for box in boxes:
            anns.append({
                "id": ann_id_counter,
                "image_id": image_id_counter,
                "category_id": box["category_id"],
                "bbox": box["bbox"],
                "area": box["area"],
                "iscrowd": 0,
            })
            ann_id_counter += 1
        
        image_id_counter += 1
    
    return images, anns, categories

def build_coco_dict(
    images: List[Dict],
    anns: List[Dict],
    categories: List[Dict],
    description: str,
    url: str,
    year: int,
) -> Dict:
    """Build a COCO-format dictionary."""
    return {
        "info": {
            "description": description,
            "url": url,
            "version": "1.0.0",
            "year": year,
        },
        "images": images,
        "annotations": anns,
        "categories": categories,
        "licenses": [],
    }

def convert(
    root: Path,
    out_dir: Path,
    subcategories: List[Tuple[str, str]],  # [(category_name, subcategory_name), ...]
    splits: List[str],
) -> None:
    """Convert selected subcategories and splits to COCO JSON files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for category_name, subcategory_name in subcategories:
        subcategory_root = root / category_name / subcategory_name
        
        if not subcategory_root.exists():
            print(f"Warning: Subcategory directory {category_name}/{subcategory_name} not found, skipping")
            continue
        
        for split in splits:
            images, anns, cat_list = collect_annotations_for_split(
                subcategory_root, split, category_name, subcategory_name
            )
            
            if not images:
                print(f"Warning: No images found for {category_name}/{subcategory_name}/{split}, skipping")
                continue
            
            desc = f"RawRipe {category_name} {subcategory_name} {split} split"
            url = "https://ieeexplore.ieee.org/document/9589215"
            coco = build_coco_dict(images, anns, cat_list, desc, url, 2021)
            # 使用植物类别前缀避免文件名冲突
            out_path = out_dir / f"{category_name}_{subcategory_name}_instances_{split}.json"
            out_path.write_text(json.dumps(coco, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Generated: {out_path} ({len(images)} images, {len(anns)} annotations)")

def main():
    parser = argparse.ArgumentParser(description="Convert RawRipe dataset to COCO JSON format")
    parser.add_argument("--root", type=Path, default=Path("."), help="Dataset root directory")
    parser.add_argument("--out", type=Path, default=Path("annotations"), help="Output directory for COCO JSON files")
    parser.add_argument("--splits", nargs="+", default=["train", "test"], help="Dataset splits to convert")
    
    args = parser.parse_args()
    
    root = args.root.resolve()
    out_dir = args.out.resolve()
    
    # 查找所有子类别
    subcategories = []
    for category_dir in sorted(root.iterdir()):
        if not category_dir.is_dir() or category_dir.name in ['scripts', 'annotations', 'data', 'docs', '.git']:
            continue
        
        category_name = category_dir.name
        for subcat_dir in sorted(category_dir.iterdir()):
            if not subcat_dir.is_dir() or subcat_dir.name in ['images', 'csv', 'json', 'sets']:
                continue
            
            # 检查是否有images目录
            if (subcat_dir / 'images').exists():
                subcategory_name = subcat_dir.name
                subcategories.append((category_name, subcategory_name))
    
    if not subcategories:
        print("Error: No subcategories found. Make sure you've run standardize.py first.")
        sys.exit(1)
    
    print(f"Found {len(subcategories)} subcategories to convert")
    convert(root, out_dir, subcategories, args.splits)
    print(f"\nConversion complete. Output directory: {out_dir}")

if __name__ == "__main__":
    main()

