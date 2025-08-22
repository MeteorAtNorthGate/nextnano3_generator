import os
import numpy as np
import config
from config import GRID_THINNEST

def add_cap(*lists):
    if not lists:
        return

    max_last_element = -float('inf')
    target_list = None

    for current_list in lists:
        if not isinstance(current_list, list) or not current_list:
            # 可以选择跳过非列表或空列表，或者抛出错误
            continue

        last_element = current_list[-1]

        if last_element > max_last_element:
            max_last_element = last_element
            target_list = current_list

    if target_list is not None:
        target_list.append(max_last_element + 1)

def merge_and_split(*lists):
    result = []
    for outputlist in lists:
        # 每200个单词分成一组,列表推导式[ XXX for i in range(start,end,step) ]
        # end-start < step时也会以 i=start 执行一次，只有end一开始就小于等于start时才不执行（步长可以为负，此时start > end才会执行）
        split_lines = [' '.join(str(x) for x in outputlist[i:i+200]) for i in range(0, len(outputlist), 200)]
        """ 可以拆解为↓↓↓的方法，但列表推导式比append有优势（底层优化）
        split_lines = []
        for i in range(0, len(outputlist), 200):
            split_lines.append(' '.join(str(x) for x in outputlist[i:i+200])) # ( XXX for i in list[]是一个生成器，这里还可以再拆开成一层循环=。= )
        """
        result.append('\n'.join(split_lines))  # 用换行符拼接回字符串,再将字符串append到result里。
    #return *result 不合法，可以return arg1,*args ,但*直接放在return后面不会被正确解释
    return tuple(result)

def get_nodes(total:float, single:int):
    if int(total / single) >= 2:
        return int(total / single)
    else:
        return 1

def if_too_thin(thickness:float):
    if thickness < config.GRID_THINNEST/2 :
        return None
    else:
        if thickness < config.GRID_THINNEST :
            return GRID_THINNEST
        else:
            return thickness

def create_gradient_tuple_np(start, end, length):
    """
    生成一个从 start 到 end，长度为 length 的等间距元组。

    Args:
        start (float/int): 区间的起始值。
        end (float/int): 区间的结束值。
        length (int): 生成的等间距元素的数量。

    Returns:
        tuple: 包含等间距元素的元组。
    """
    if length <= 0:
        return ()
    if length == 1:
        return (float(start),) # 如果只有一个元素，确保是浮点数元组

    # 使用 numpy.linspace 生成等间距的数组
    # endpoint=True 确保包含 end 值
    evenly_spaced_array = np.linspace(start, end, num=length, endpoint=True)

    # 将 NumPy 数组转换为元组
    return tuple(evenly_spaced_array)

def create_gradient_tuple_py(start, end, length):
    """
    不使用 NumPy，生成一个从 start 到 end，长度为 length 的等间距元组。

    Args:
        start (float/int): 区间的起始值。
        end (float/int): 区间的结束值。
        length (int): 生成的等间距元素的数量。

    Returns:
        tuple: 包含等间距元素的元组。
    """
    if length <= 0:
        return ()
    if length == 1:
        return (float(start),)

    # 计算步长
    # 如果 length > 1，则有 (length - 1) 个间隔
    step = (end - start) / (length - 1)

    # 使用列表推导式生成元素，然后转换为元组
    result_list = [start + i * step for i in range(length)]
    return tuple(result_list)

def remove_if_exists(path_to_remove):
    """
    检查一个路径（文件或目录）是否存在，如果存在则删除它。

    参数:
        path_to_remove (str): 要检查和删除的路径。

    返回:
        bool: 如果路径被成功删除则返回 True，如果路径不存在或删除失败则返回 False。
    """
    if os.path.exists(path_to_remove):
        try:
            if os.path.isfile(path_to_remove):
                os.remove(path_to_remove)
                print(f"文件 '{path_to_remove}' 已成功删除。")
            elif os.path.isdir(path_to_remove):
                # os.rmdir() 只能删除空目录
                # 如果要删除非空目录，需要使用 shutil.rmtree()
                # 为了保持模块简单，这里只处理空目录或直接删除文件
                os.rmdir(path_to_remove)
                print(f"空目录 '{path_to_remove}' 已成功删除。")
            return True
        except OSError as e:
            print(f"删除 '{path_to_remove}' 时发生错误: {e}")
            return False
    else:
        print(f"路径 '{path_to_remove}' 不存在。")
        return False