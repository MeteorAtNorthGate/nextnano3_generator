import re
import pandas as pd


def to_layer_input():


def xlsx(file_path,sheet = "Sheet1"):
    try:
        # 读取 Excel 文件
        # 你可以指定 sheet_name 参数来读取特定的工作表，例如 sheet_name='Sheet1'
        # 如果不指定，默认读取第一个工作表
        df = pd.read_excel(file_path, sheet_name = sheet)

        # 创建一个空字典来存储列数据
        columns_data = {}

        # 遍历 DataFrame 的每一列
        for column_name in df.columns:
            # 将列数据转换为列表并存储到字典中
            columns_data[column_name] = df[column_name].tolist()

        return columns_data

    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

if __name__ == "__main__":
    datas = xlsx(r"demo.xlsx")
    '''
    for column, data in datas.items(): #使用.items进行字典解包
        print("-------------------------------------")
        print(column)
        print(data)
    '''
