import os
import re
import matplotlib.pyplot as plt
import numpy as np

def read_result_files(result_dir='./result'):
    """读取result目录下的所有txt文件数据"""
    data = {}
    experiment_dates = []
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(result_dir) if f.endswith('.txt')]
    txt_files.sort()  # 按字母顺序排序
    
    for txt_file in txt_files:
        file_path = os.path.join(result_dir, txt_file)
        experiment_name = os.path.splitext(txt_file)[0]
        experiment_dates.append(experiment_name)
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
            # 跳过前几行，直接读取图片数据
            for line in lines:
                match = re.match(r'(.+\.png): ([\d.]+)', line)
                if match:
                    image_name = match.group(1)
                    gray_value = float(match.group(2))
                    
                    if image_name not in data:
                        data[image_name] = {}
                    
                    data[image_name][experiment_name] = gray_value
    
    return data, experiment_dates

def plot_data(data, experiment_dates):
    """为每个图片创建折线图"""
    # 创建输出目录
    plot_dir = './plots'
    os.makedirs(plot_dir, exist_ok=True)
    
    # 设置图表样式
    plt.style.use('ggplot')
    
    # 为每个图片创建折线图
    for image_name, values in data.items():
        plt.figure(figsize=(10, 6))
        
        # 准备数据
        x = []
        y = []
        for date in experiment_dates:
            if date in values:
                x.append(date)
                y.append(values[date])
        
        # 绘制折线图
        plt.plot(x, y, 'o-', linewidth=2, markersize=8)
        
        # 添加数据标签
        for i, (xi, yi) in enumerate(zip(x, y)):
            plt.annotate(f'{yi:.2f}', (xi, yi), textcoords="offset points", 
                         xytext=(0, 10), ha='center')
        
        # 设置图表标题和标签
        plt.title(f'Grey scale - {image_name}', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Grey scale', fontsize=12)
        
        # 调整x轴标签角度，避免重叠
        plt.xticks(rotation=45)
        
        # 自动调整布局
        plt.tight_layout()
        
        # 保存图表
        output_file = os.path.join(plot_dir, f'{os.path.splitext(image_name)[0]}_plot.png')
        plt.savefig(output_file, dpi=300)
        plt.close()
        
        print(f'已生成图表: {output_file}')
    
    # 创建一个汇总图表，显示所有图片的数据
    plt.figure(figsize=(12, 8))
    
    # 为每个图片绘制一条折线
    for image_name, values in data.items():
        x = []
        y = []
        for date in experiment_dates:
            if date in values:
                x.append(date)
                y.append(values[date])
        
        # 使用更简洁的图例名称（去掉.png后缀）
        legend_name = os.path.splitext(image_name)[0]
        plt.plot(x, y, 'o-', linewidth=2, markersize=6, label=legend_name)
    
    # 设置图表标题和标签
    plt.title('Summary', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Grey scale', fontsize=12)
    
    # 添加图例
    plt.legend(loc='best')
    
    # 调整x轴标签角度，避免重叠
    plt.xticks(rotation=45)
    
    # 自动调整布局
    plt.tight_layout()
    
    # 保存汇总图表
    output_file = os.path.join(plot_dir, 'summary_plot.png')
    plt.savefig(output_file, dpi=300)
    plt.close()
    
    print(f'已生成汇总图表: {output_file}')

def main():
    print("开始分析result文件夹中的数据...")
    
    # 读取所有结果文件
    data, experiment_dates = read_result_files()
    
    if not data:
        print("未找到有效数据，请确保result文件夹中包含正确格式的txt文件")
        return
    
    print(f"找到 {len(data)} 个图片数据，跨越 {len(experiment_dates)} 个实验日期")
    
    # 绘制图表
    plot_data(data, experiment_dates)
    
    print("数据可视化完成！所有图表已保存到 ./plots 目录")

if __name__ == "__main__":
    main()