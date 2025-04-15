import os
from rembg import remove
from PIL import Image
import argparse

def list_directories(path='./input/'):
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

def process_directory(input_dir, output_dir, recursive=False):
    """处理指定目录中的所有图片文件，去除背景并保存到输出目录"""
    # 获取输入目录的名称
    input_dir_name = os.path.basename(os.path.normpath(input_dir))
    
    # 在输出目录中创建与输入目录同名的子目录
    final_output_dir = os.path.join(output_dir, input_dir_name)
    os.makedirs(final_output_dir, exist_ok=True)
    
    # 获取所有文件
    if recursive:
        files = []
        for root, _, filenames in os.walk(input_dir):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    # 支持的图片格式
    supported_formats = ['.png', '.jpg', '.jpeg', '.webp', '.bmp']
    
    # 处理每个文件
    processed_count = 0
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in supported_formats:
            try:
                # 计算相对路径以保持目录结构（如果是递归模式）
                if recursive:
                    rel_path = os.path.relpath(file_path, input_dir)
                    output_path = os.path.join(final_output_dir, rel_path)
                    # 确保输出子目录存在
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                else:
                    filename = os.path.basename(file_path)
                    output_path = os.path.join(final_output_dir, filename)
                
                # 处理图片
                print(f"处理: {file_path}")
                input_image = Image.open(file_path)
                output_image = remove(input_image)
                
                # 调整图片大小为768*768，等比例缩放
                output_image = resize_image_to_768(output_image)
                
                # 统一输出为PNG格式
                output_path = os.path.splitext(output_path)[0] + '.png'
                
                output_image.save(output_path)
                processed_count += 1
            except Exception as e:
                print(f"处理 {file_path} 时出错: {str(e)}")
    
    return processed_count

def resize_image_to_768(image):
    """将图片等比例缩放到最长边为768，并放置在768*768的透明背景上"""
    # 获取原始尺寸
    width, height = image.size
    
    # 计算缩放比例
    if width > height:
        new_width = 768
        new_height = int(height * (768 / width))
    else:
        new_height = 768
        new_width = int(width * (768 / height))
    
    # 等比例缩放图片
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # 创建768*768的透明背景
    new_image = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    
    # 计算粘贴位置（居中）
    paste_x = (768 - new_width) // 2
    paste_y = (768 - new_height) // 2
    
    # 将缩放后的图片粘贴到透明背景上
    new_image.paste(resized_image, (paste_x, paste_y), resized_image if resized_image.mode == 'RGBA' else None)
    
    return new_image

def main():
    parser = argparse.ArgumentParser(description='批量去除图片背景')
    parser.add_argument('-i', '--input', help='输入目录，默认为用户选择input目录中的子目录')
    parser.add_argument('-o', '--output', default='./output', help='输出目录，默认为当前目录下的output文件夹')
    parser.add_argument('-r', '--recursive', action='store_true', help='是否递归处理子目录')
    parser.add_argument('-l', '--list', action='store_true', help='列出input目录下的所有目录')
    args = parser.parse_args()
    
    input_base_dir = './input/'
    
    # 如果用户指定了--list参数，只列出目录后退出
    if args.list:
        directories = list_directories(input_base_dir)
        if directories:
            print("input目录下的文件夹:")
            for directory in directories:
                print(f"- {directory}")
        else:
            print("input目录下没有文件夹")
        return
    
    # 如果没有指定输入目录，让用户选择
    input_dir = args.input
    if not input_dir:
        directories = list_directories(input_base_dir)
        selected_dir = select_directory(directories)
        if selected_dir:
            input_dir = os.path.join(input_base_dir, selected_dir)
        else:
            print("未选择目录，退出程序")
            return
    
    output_dir = args.output
    
    print(f"开始处理图片...")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"递归模式: {'是' if args.recursive else '否'}")
    
    count = process_directory(input_dir, output_dir, args.recursive)
    print(f"处理完成! 共处理 {count} 张图片")

if __name__ == "__main__":
    main()