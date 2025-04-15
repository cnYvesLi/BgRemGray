# 图像背景去除与灰度分析工具

本项目用于批量去除图像背景、调整图像大小，并分析处理后图像的灰度值。用于G4实验。

## 功能特点

- **批量背景去除**：自动去除图像背景，保留主体内容
- **统一图像尺寸**：将图像等比例缩放至768×768像素
- **灰度值分析**：计算图像非透明部分的平均灰度值
- **数据可视化**：生成折线图展示不同样本的灰度值变化

## 文件结构

- `batch_rembg.py`: 批量去除图像背景并调整尺寸
- `calculate_avg_gray.py`: 计算处理后图像的平均灰度值
- `plot_results.py`: 将分析结果可视化为折线图

## 使用方法

### 1. 配置环境
```bash
pip install -r requirements.txt
```
### 2. 准备图像

将需要处理的图像放入 `input` 目录下的子文件夹中。例如：
input/
├── Apr8_20.40/
│   ├── overview.jpg
│   ├── vinegar_soak.jpg
│   └── ...
└── Apr15_10.30/
    ├── overview.jpg
    ├── vinegar_soak.jpg
    └── ...
### 3. 去除背景

运行背景去除脚本：

```bash
python /Users/liyu/Desktop/G4/batch_rembg.py
```
处理后的图像将保存在 `output` 目录下。
程序会列出 input 目录下的所有子文件夹，让你选择要处理的文件夹。处理后的图像将保存在 output 目录下，保持原始的文件夹结构。
