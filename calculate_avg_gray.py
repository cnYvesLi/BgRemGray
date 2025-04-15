import os
import argparse
from PIL import Image
import numpy as np

def list_directories(path='.'):
    """列举指定路径下的所有目录"""
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories

def select_directory(directories):
    """让用户从列表中选择一个目录"""
    if not directories:
        print("当前路径下没有目录")
        return None
    
    print("请选择要处理的目录:")
    for i, directory in enumerate(directories, 1):
        print(f"{i}. {directory}")
    
    while True:
        try:
            choice = int(input("请输入目录编号 (0 退出): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(directories):
                return directories[choice-1]
            print(f"请输入1到{len(directories)}之间的数字")
        except ValueError:
            print("请输入有效的数字")

def calculate_avg_gray(image_path):
    """计算图片非透明部分的平均灰度值"""
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 确保图片是RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 转换为numpy数组
        img_array = np.array(img)
        
        # 获取alpha通道
        alpha = img_array[:, :, 3]
        
        # 找出非透明像素（alpha > 0）
        non_transparent = alpha > 0
        
        # 如果没有非透明像素，返回None
        if not np.any(non_transparent):
            return None
        
        # 计算RGB通道的平均值（只考虑非透明像素）
        r_avg = np.mean(img_array[:, :, 0][non_transparent])
        g_avg = np.mean(img_array[:, :, 1][non_transparent])
        b_avg = np.mean(img_array[:, :, 2][non_transparent])
        
        # 计算RGB平均灰度值
        avg_gray = (r_avg + g_avg + b_avg) / 3
        
        return avg_gray
    
    except Exception as e:
        print(f"处理 {image_path} 时出错: {str(e)}")
        return None

def process_directory(input_dir):
    """处理指定目录中的所有PNG图片，计算平均灰度值"""
    results = {}
    total_gray = 0
    valid_count = 0
    
    # 获取所有PNG文件
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
             if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith('.png')]
    
    for file_path in files:
        print(f"处理: {file_path}")
        avg_gray = calculate_avg_gray(file_path)
        
        if avg_gray is not None:
            filename = os.path.basename(file_path)
            results[filename] = avg_gray
            total_gray += avg_gray
            valid_count += 1
    
    # 计算所有图片的平均灰度值
    overall_avg = total_gray / valid_count if valid_count > 0 else 0
    
    return results, overall_avg

def main():
    parser = argparse.ArgumentParser(description='计算图片非透明部分的平均灰度值')
    parser.add_argument('-i', '--input', help='输入目录，默认为用户选择output中的子目录')
    parser.add_argument('-o', '--output', help='输出文本文件路径，默认为result/目录名.txt')
    args = parser.parse_args()
    
    # 如果没有指定输入目录，让用户选择output中的子目录
    input_dir = args.input
    if not input_dir:
        output_dir = './output'
        if not os.path.exists(output_dir):
            print(f"错误: 输出目录 {output_dir} 不存在")
            return
        
        directories = list_directories(output_dir)
        if not directories:
            print(f"错误: 在 {output_dir} 中没有找到子目录")
            return
        
        selected_dir = select_directory(directories)
        if selected_dir:
            input_dir = os.path.join(output_dir, selected_dir)
        else:
            print("未选择目录，退出程序")
            return
    
    # 获取输入目录的名称
    input_dir_name = os.path.basename(os.path.normpath(input_dir))
    
    # 创建result文件夹
    result_dir = './result'
    os.makedirs(result_dir, exist_ok=True)
    
    # 设置输出文件路径
    output_file = args.output
    if not output_file:
        output_file = os.path.join(result_dir, f"{input_dir_name}.txt")
    
    print(f"开始处理图片...")
    print(f"输入目录: {input_dir}")
    print(f"输出文件: {output_file}")
    
    # 处理目录中的图片
    results, overall_avg = process_directory(input_dir)
    
    # 将结果写入文本文件
    with open(output_file, 'w') as f:
        f.write(f"目录: {input_dir}\n")
        f.write(f"总平均灰度值: {overall_avg:.2f}\n\n")
        f.write("各图片灰度值:\n")
        for filename, avg_gray in results.items():
            f.write(f"{filename}: {avg_gray:.2f}\n")
    
    print(f"处理完成! 结果已保存到 {output_file}")
    print(f"总平均灰度值: {overall_avg:.2f}")

if __name__ == "__main__":
    main()