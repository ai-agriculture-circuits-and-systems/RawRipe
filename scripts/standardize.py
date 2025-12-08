#!/usr/bin/env python3
"""
标准化 RawRipe 数据集结构
根据标准化数据集结构规范进行重组
这是一个分类数据集，包含10种水果，每种水果有Raw和Ripe两种状态
使用Model 1的结构作为主要数据源（最清晰的组织方式）
"""
import json
import csv
import shutil
from pathlib import Path
from PIL import Image
from collections import defaultdict

# 数据集根目录
ROOT = Path(__file__).parent.parent

# 原始数据目录（Model 1结构）
ORIGINAL_TRAIN_DIR = ROOT / "geufruits5_train" / "Model 1"
ORIGINAL_TEST_DIR = ROOT / "geufruits5_test" / "Model 1"

# 水果名称映射（标准化为复数形式）
FRUIT_MAPPING = {
    "Apple": "apples",
    "Banana": "bananas",
    "Coconut": "coconuts",
    "Guava": "guavas",
    "Leeche": "litchis",  # 标准化拼写
    "Mango": "mangoes",
    "Orange": "oranges",
    "Papaya": "papayas",
    "Pomengranate": "pomegranates",  # 标准化拼写
    "Strawberry": "strawberries",
}

# 状态名称映射（标准化为小写）
STATE_MAPPING = {
    "Raw": "raw",
    "Ripe": "ripe",
}

def create_directory_structure(root: Path):
    """创建标准化目录结构"""
    for fruit_orig, fruit_std in FRUIT_MAPPING.items():
        fruit_dir = root / fruit_std
        for state_orig, state_std in STATE_MAPPING.items():
            subcat_dir = fruit_dir / state_std
            (subcat_dir / "images").mkdir(parents=True, exist_ok=True)
            (subcat_dir / "csv").mkdir(parents=True, exist_ok=True)
            (subcat_dir / "json").mkdir(parents=True, exist_ok=True)
            (subcat_dir / "sets").mkdir(parents=True, exist_ok=True)

def create_labelmap(fruit_dir: Path, fruit_name: str, state_name: str):
    """创建labelmap.json文件"""
    labelmap = {
        "1": {
            "id": 1,
            "name": state_name,
            "supercategory": fruit_name
        }
    }
    labelmap_path = fruit_dir / state_name / "labelmap.json"
    labelmap_path.write_text(
        json.dumps(labelmap, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def create_csv_annotation(image_path: Path, output_csv_path: Path, width: int, height: int):
    """创建CSV标注文件（全图bounding box用于分类）"""
    # CSV格式：image_path, x_min, y_min, x_max, y_max, class_name
    # 全图bounding box: (0, 0, width, height)
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['image_path', 'x_min', 'y_min', 'x_max', 'y_max', 'class_name'])
        writer.writerow([
            str(image_path.name),
            0,
            0,
            width,
            height,
            'fruit'  # 统一使用'fruit'作为类别名
        ])

def create_json_annotation(image_path: Path, output_json_path: Path, width: int, height: int, 
                          fruit_name: str, state_name: str):
    """创建JSON标注文件（全图bounding box用于分类）"""
    annotation_data = {
        "info": {
            "description": f"RawRipe {fruit_name} {state_name} classification dataset",
            "version": "1.0.0",
            "year": 2021,
            "contributor": "Rao Jerripothula, Koteswar and Kumar Shukla, Sarvesh and Jain, Samyak and Singh, Shudhanshu",
            "url": "https://ieeexplore.ieee.org/document/9589215"
        },
        "images": [
            {
                "id": 1,
                "width": width,
                "height": height,
                "file_name": image_path.name,
                "license": 0
            }
        ],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "bbox": [0, 0, width, height],  # 全图bounding box
                "area": width * height,
                "iscrowd": 0
            }
        ],
        "categories": [
            {
                "id": 1,
                "name": state_name,
                "supercategory": fruit_name
            }
        ]
    }
    
    output_json_path.write_text(
        json.dumps(annotation_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def process_images_and_annotations(root: Path):
    """处理图像并生成标注"""
    train_images = defaultdict(lambda: defaultdict(list))
    test_images = defaultdict(lambda: defaultdict(list))
    
    # 处理训练集
    if ORIGINAL_TRAIN_DIR.exists():
        for fruit_orig_dir in sorted(ORIGINAL_TRAIN_DIR.iterdir()):
            if not fruit_orig_dir.is_dir():
                continue
            
            fruit_orig = fruit_orig_dir.name
            if fruit_orig not in FRUIT_MAPPING:
                print(f"Warning: Unknown fruit '{fruit_orig}', skipping")
                continue
            
            fruit_std = FRUIT_MAPPING[fruit_orig]
            fruit_dir = root / fruit_std
            
            for state_orig_dir in sorted(fruit_orig_dir.iterdir()):
                if not state_orig_dir.is_dir():
                    continue
                
                state_orig = state_orig_dir.name
                if state_orig not in STATE_MAPPING:
                    print(f"Warning: Unknown state '{state_orig}' for {fruit_orig}, skipping")
                    continue
                
                state_std = STATE_MAPPING[state_orig]
                subcat_dir = fruit_dir / state_std
                
                # 创建labelmap
                create_labelmap(fruit_dir, fruit_std, state_std)
                
                # 处理图像
                for img_file in sorted(state_orig_dir.iterdir()):
                    if not img_file.is_file() or img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.JPG']:
                        continue
                    
                    # 读取图像尺寸
                    try:
                        with Image.open(img_file) as img:
                            width, height = img.size
                    except Exception as e:
                        print(f"Error reading image {img_file}: {e}")
                        continue
                    
                    # 复制图像
                    img_dest = subcat_dir / "images" / img_file.name
                    shutil.copy2(img_file, img_dest)
                    
                    # 生成标注文件名（不含扩展名）
                    stem = img_file.stem
                    
                    # 创建CSV标注
                    csv_path = subcat_dir / "csv" / f"{stem}.csv"
                    create_csv_annotation(img_dest, csv_path, width, height)
                    
                    # 创建JSON标注
                    json_path = subcat_dir / "json" / f"{stem}.json"
                    create_json_annotation(img_dest, json_path, width, height, fruit_std, state_std)
                    
                    train_images[fruit_std][state_std].append(stem)
    
    # 处理测试集
    if ORIGINAL_TEST_DIR.exists():
        for fruit_orig_dir in sorted(ORIGINAL_TEST_DIR.iterdir()):
            if not fruit_orig_dir.is_dir():
                continue
            
            fruit_orig = fruit_orig_dir.name
            if fruit_orig not in FRUIT_MAPPING:
                continue
            
            fruit_std = FRUIT_MAPPING[fruit_orig]
            fruit_dir = root / fruit_std
            
            for state_orig_dir in sorted(fruit_orig_dir.iterdir()):
                if not state_orig_dir.is_dir():
                    continue
                
                state_orig = state_orig_dir.name
                if state_orig not in STATE_MAPPING:
                    continue
                
                state_std = STATE_MAPPING[state_orig]
                subcat_dir = fruit_dir / state_std
                
                # 处理图像
                for img_file in sorted(state_orig_dir.iterdir()):
                    if not img_file.is_file() or img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.JPG']:
                        continue
                    
                    # 读取图像尺寸
                    try:
                        with Image.open(img_file) as img:
                            width, height = img.size
                    except Exception as e:
                        print(f"Error reading image {img_file}: {e}")
                        continue
                    
                    # 复制图像
                    img_dest = subcat_dir / "images" / img_file.name
                    shutil.copy2(img_file, img_dest)
                    
                    # 生成标注文件名（不含扩展名）
                    stem = img_file.stem
                    
                    # 创建CSV标注
                    csv_path = subcat_dir / "csv" / f"{stem}.csv"
                    create_csv_annotation(img_dest, csv_path, width, height)
                    
                    # 创建JSON标注
                    json_path = subcat_dir / "json" / f"{stem}.json"
                    create_json_annotation(img_dest, json_path, width, height, fruit_std, state_std)
                    
                    test_images[fruit_std][state_std].append(stem)
    
    return train_images, test_images

def create_splits(root: Path, train_images: dict, test_images: dict):
    """创建数据集划分文件"""
    for fruit_name, states in train_images.items():
        for state_name, train_stems in states.items():
            subcat_dir = root / fruit_name / state_name
            sets_dir = subcat_dir / "sets"
            
            test_stems = test_images.get(fruit_name, {}).get(state_name, [])
            
            # 合并所有图像
            all_stems = sorted(set(train_stems + test_stems))
            
            # 写入划分文件
            (sets_dir / "train.txt").write_text("\n".join(sorted(train_stems)) + "\n", encoding="utf-8")
            (sets_dir / "test.txt").write_text("\n".join(sorted(test_stems)) + "\n", encoding="utf-8")
            (sets_dir / "all.txt").write_text("\n".join(all_stems) + "\n", encoding="utf-8")
            (sets_dir / "train_val.txt").write_text("\n".join(sorted(train_stems)) + "\n", encoding="utf-8")
            
            # val.txt 为空（因为原始数据集只有train和test）
            (sets_dir / "val.txt").write_text("", encoding="utf-8")

def main():
    """主函数"""
    print("=== RawRipe 数据集标准化 ===\n")
    
    # 创建目录结构
    print("1. 创建标准化目录结构...")
    create_directory_structure(ROOT)
    print("   ✓ 目录结构创建完成\n")
    
    # 处理图像和标注
    print("2. 处理图像并生成标注...")
    train_images, test_images = process_images_and_annotations(ROOT)
    
    # 统计信息
    total_train = sum(len(stems) for states in train_images.values() for stems in states.values())
    total_test = sum(len(stems) for states in test_images.values() for stems in states.values())
    print(f"   ✓ 处理完成: {total_train} 训练图像, {total_test} 测试图像\n")
    
    # 创建划分文件
    print("3. 创建数据集划分文件...")
    create_splits(ROOT, train_images, test_images)
    print("   ✓ 划分文件创建完成\n")
    
    print("=== 标准化完成 ===")
    print(f"\n数据集统计:")
    for fruit_name, states in sorted(train_images.items()):
        print(f"  {fruit_name}:")
        for state_name in sorted(states.keys()):
            train_count = len(train_images[fruit_name][state_name])
            test_count = len(test_images.get(fruit_name, {}).get(state_name, []))
            print(f"    {state_name}: train={train_count}, test={test_count}, total={train_count + test_count}")

if __name__ == "__main__":
    main()

