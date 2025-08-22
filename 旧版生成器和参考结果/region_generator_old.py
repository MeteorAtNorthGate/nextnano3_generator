#coding = utf-8
import tools

def sl_2l(z, layer_start, layer_total, layer1, layer2, out_path):
    with open(out_path, "a") as f:
        n: int = 0
        while n < layer_total : #循环生成起始坐标和结束坐标
            i = f"{z:.3f}d0"
            if n % 2 == 0:
                z += layer1
            else:
                z += layer2
            j = f"{z:.3f}d0"
            
            # 写入文件
            f.write(f" region-number = {n + layer_start + 1}     ")
            f.write("base-geometry = line     ")
            f.write("region-priority = 1\n")
            f.write(f" z-coordinates = {i}   {j}\n\n")
            n += 1
        f.write("!----------------------------------------!\n")
    return z

if __name__ == "__main__":
    #输出文件，采用追加写入模式，因此需要先清除上次运行的输出
    output = "./region_output.txt"
    tools.remove_if_exists(output)
    
    #初始位置和region计数
    startZ: float = 300
    
    lastN: int = 1
    #超晶格周期数和单层厚度
    loop1: int = 477
    layerA = 4.4
    layerB = 4.4
    
    layer_this_block = loop1 * 2 #两层一个周期
    # 数据输出到文件, 并返回顶层位置
    startZ = sl_2l(startZ, lastN, layer_this_block, layerA, layerB, output)
    
    #超晶格2------------------------------------------------
    lastN += layer_this_block
    #超晶格周期数和单层厚度
    loop2: int = 44
    layerA = 1.45
    layerB = 1.98
    
    layer_this_block = loop2 * 2 #两层一个周期
    # 数据输出到文件, 并返回顶层位置
    startZ = sl_2l(startZ, lastN, layer_this_block, layerA, layerB, output)
    
    #超晶格3------------------------------------------------
    lastN += layer_this_block
    #超晶格周期数和单层厚度
    loop3: int = 57
    layerA = 4.4
    layerB = 4.4
    
    layer_this_block = loop3 * 2 #两层一个周期
    # 数据输出到文件, 并返回顶层位置
    startZ = sl_2l(startZ, lastN, layer_this_block, layerA, layerB, output)
    
    #
    print(startZ)
    wait = input()
