#coding = utf-8
import tools

def splitline(*lineN):
    result = []
    for line in lineN:
        words = line.split()  # 将字符串按空格分割为单词列表
        split_lines = [' '.join(words[i:i+100]) for i in range(0, len(words), 100)]  # 每200个单词分成一组
        result.append('\n'.join(split_lines))  # 用换行符拼接回字符串
    return tuple(result)

def get_nodes(total, single):
    if total // single >= 2:
        return total// single
    else:
        return 2

def single_layer(z_position, former_layer,thickness,grid_lines, grid_nodes,grid_factors, cluster_a):
    n = former_layer
    global GRID_THICKNESS_SINGLE
    nodes_a = get_nodes(thickness, GRID_THICKNESS_SINGLE)

    z_position += thickness
    grid_nodes += f"        {nodes_a}"
    cluster_a += f" {n + 1}"
    grid_lines += f" {z_position:.3f}d0"
    grid_factors += f"      1d0"
    n += 1

    return z_position,n,grid_lines,grid_nodes,grid_factors,cluster_a

#一层一层复制着写吧，，，倒不是我要故意搞意面代码，确实不好操作且没必要
def sl_2l(z_position:float, former_layer:int, loop, thickness_a, thickness_b, grid_lines, grid_nodes,
          grid_factors, cluster_a, cluster_b):
    repeat_unit: int = 2

    n = former_layer
    global GRID_THICKNESS_SL
    nodes_a = get_nodes(thickness_a, GRID_THICKNESS_SL)
    nodes_b = get_nodes(thickness_b, GRID_THICKNESS_SL)

    layer_end = loop * repeat_unit + n
    while n < layer_end : #生成起始坐标和结束坐标写入文件。
        # 整除法在3往上就不好使了（还多一步浮点运算，所以这里提前改成计数循环。
        z_position += thickness_a
        grid_nodes += f"        {nodes_a}"
        cluster_a += f" {n + 1}"
        grid_lines += f" {z_position:.3f}d0"

        z_position += thickness_b
        grid_nodes += f"        {nodes_b}"
        cluster_b += f" {n + 2}"
        grid_lines += f" {z_position:.3f}d0"

        for _ in range(repeat_unit):
            grid_factors += f"      1d0"

        n += repeat_unit
 
    return z_position,n,grid_lines,grid_nodes,grid_factors,cluster_a,cluster_b

def sl_3l(z_position:float, former_layer:int, loop, thickness_a, thickness_b,thickness_c, grid_lines, grid_nodes,
          grid_factors, cluster_a, cluster_b, cluster_c):
    repeat_unit: int = 3

    n = former_layer
    global GRID_THICKNESS_SL
    nodes_a = get_nodes(thickness_a,GRID_THICKNESS_SL)
    nodes_b = get_nodes(thickness_b, GRID_THICKNESS_SL)
    nodes_c = get_nodes(thickness_c, GRID_THICKNESS_SL)

    layer_end = loop * repeat_unit + n
    while n < layer_end:  # 生成起始坐标和结束坐标写入文件。
        z_position += thickness_a
        grid_nodes += f"        {nodes_a}"
        cluster_a += f" {n + 1}"
        grid_lines += f" {z_position:.3f}d0"

        z_position += thickness_b
        grid_nodes += f"        {nodes_b}"
        cluster_b += f" {n + 2}"
        grid_lines += f" {z_position:.3f}d0"

        z_position += thickness_c
        grid_nodes += f"        {nodes_c}"
        cluster_c += f" {n + 3}"
        grid_lines += f" {z_position:.3f}d0"

        for _ in range(repeat_unit):
            grid_factors += f"      1d0"

        n += repeat_unit

    return z_position, n, grid_lines, grid_nodes, grid_factors, cluster_a, cluster_b

if __name__ == "__main__":
    #输出文件，采用w模式
    output = "./grid_cluster_output.txt"
    tools.remove_if_exists(output)
    #凑合用用吧=。= 用字典或者类打包也不方便
    grid_lines = ""
    grid_nodes = ""
    grid_factors = ""
    cluster1 = "" #InAs
    cluster2 = "" #GaSb
    cluster3 = "" #AlSb

    GRID_THICKNESS_SL = 2 #超晶格单层的节点间距离，4nm/2 两个节点，9nm/2 四个节点
    GRID_THICKNESS_SINGLE = 20 #单层的节点间距离，比方说600nm/20 就是30个点

    former_z: float = 0 #初始化Z轴位置和层数
    former_n: int = 0
    #第一层，buffer
    #厚度
    thickness_a:float = 600
    former_z, former_n, grid_lines, grid_nodes, grid_factors, cluster2 = single_layer(former_z,former_n,thickness_a,grid_lines, grid_nodes, grid_factors, cluster2)

    #超晶格1 9.39nm InAs/ 4.27nm GaSb
    #周期数和单层厚度
    loop1: int = 30
    sl_a = 3.332
    sl_b = 2.761

    # 添加数据到字符串中,目前是通过传参（cluster12/34 → clusterAB）来让不同的结构调用同一个生成函数
    former_z,former_n,grid_lines,grid_nodes,grid_factors,cluster1,cluster2 = sl_2l(former_z,former_n,loop1,sl_a,sl_b,grid_lines,grid_nodes,grid_factors,cluster1,cluster2)

    #裁剪
    grid_lines,grid_nodes,grid_factors,cluster1,cluster2,cluster3,cluster4 = splitline(grid_lines, grid_nodes, grid_factors, cluster1, cluster2, cluster3)
    
    with open(output,"w") as f:
        # 写入文件
        f.write(f" z-grid-lines     ={grid_lines}\n")
        f.write(f" z-nodes          ={grid_nodes}\n")
        f.write(f" z-grid-factors   ={grid_factors}\n")
        
        f.write(f" cluster-number = 1    region-numbers ={cluster1}\n")
        f.write(f" cluster-number = 2    region-numbers ={cluster2}\n")
        f.write(f" cluster-number = 3    region-numbers ={cluster3}\n")
        f.write(f" cluster-number = 4    region-numbers ={cluster4}\n")
        
    print(former_z)
    wait = input()