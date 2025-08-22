#coding = utf-8
import config
import tools
import output

def single_layer(z_position, former_layer, thickness, grid_lines, grid_nodes, grid_factors, cluster_a):
    n = former_layer
    nodes_a = tools.get_nodes(thickness, config.GRID_THICKNESS_SINGLE)

    z_position += thickness
    grid_nodes.append(nodes_a)
    cluster_a.append(n + 1)
    grid_lines.append(f" {z_position:.3f}d0")
    grid_factors.append("1d0")
    n += 1
    print(f"当前单层顶端位置为{z_position:.3f}，是第{n}个region")
    return z_position,n,grid_lines,grid_nodes,grid_factors,cluster_a

#基础的两层超晶格
def sl_2_layer(z_position:float, layer_num:int, loop, grid_lines, grid_nodes,
               grid_factors, thickness_a, cluster_a, thickness_b, cluster_b):
    """
    :param z_position:上一层的结束坐标
    :param layer_num:上一层的结束层数
    :param loop:超晶格循环数
    :param grid_lines
    :param grid_nodes
    :param grid_factors
    :param thickness_a:A层厚度
    :param cluster_a:A层应归属的类型
    :param thickness_b:B层厚度
    :param cluster_b:B层应归属的类型
    :return:返回结束坐标、结束层数、lines、nodes、factors、两个cluster列表
    """
    layer_total = loop * 2

    nodes_a = tools.get_nodes(thickness_a, config.GRID_THICKNESS_SL)
    nodes_b = tools.get_nodes(thickness_b, config.GRID_THICKNESS_SL)

    layer_end = layer_num + layer_total
    while layer_num < layer_end :
        # 整除法在3往上就不好使了（还多一步浮点运算，所以这里提前改成计数循环。
        z_position += thickness_a
        grid_nodes.append(nodes_a)
        cluster_a.append(layer_num + 1)
        grid_lines.append(f" {z_position:.3f}d0")

        z_position += thickness_b
        grid_nodes.append(nodes_b)
        cluster_b.append(layer_num + 2)
        grid_lines.append(f" {z_position:.3f}d0")

        for _ in range(2):
            grid_factors.append("1d0")

        layer_num += 2
    print(f"当前超晶格顶端位置为{z_position:.3f}，是第{layer_num}个region")
    return z_position,layer_num,grid_lines,grid_nodes,grid_factors,cluster_a,cluster_b

def sl_multi_layer(z_position:float, layer_num:int, loop, grid_lines, grid_nodes,
                   grid_factors, *thickness_and_cluster):
    """
    完整的超晶格生成函数。如果超晶格只有两层，且不需要梯度渐变，可以用简化版的sl_2_layer
    :param z_position:上一层的结束坐标
    :param layer_num:上一层的结束层数
    :param loop:超晶格循环数
    :param thickness_and_cluster: 依次写入每层的厚度和归属cluster,渐变厚度用(float,float)或者[float,float]的形式输入初始厚度和结束厚度
    因为每层有两个参数(厚度和cluster），这部分输入数量必须为偶数！
    :return:返回新的当前Z坐标，层数，lines,nodes,factors，最后依次返回每个cluster
    """
    if not len(thickness_and_cluster) % 2 == 0:
        print("请检查输入参数数量！")
        return
    units_num = len(thickness_and_cluster) // 2

    thickness_i = []
    cluster_i = []
    i:int = 0
    while i < (units_num * 2):  # 遍历输入的循环体结构,拆解成厚度和cluster两个列表
        thickness_i.append(thickness_and_cluster[i])
        i += 1
        cluster_i.append(thickness_and_cluster[i])
        i += 1

    #对于厚度列表，统一将固定厚度和渐变厚度都转为一个长度为loop的元组
    gradient_thickness_i = [] #二维列表（每个单层，每个单层的渐变梯度表）
    for thickness in thickness_i:
        if isinstance(thickness, float):
            gradient_thickness_i.append((thickness,)*loop)
        if isinstance(thickness, tuple):
            gradient_thickness = tools.create_gradient_tuple_np(thickness[0],thickness[1],loop)
            gradient_thickness_i.append(gradient_thickness)
        if isinstance(thickness, list):
            gradient_thickness = tools.create_gradient_tuple_np(thickness[0],thickness[1],loop)
            gradient_thickness_i.append(gradient_thickness)

    for N in range(loop) :
        for i in range(units_num): #两层循环，总层数 = units_num * loop
            current_layer = tools.if_too_thin(gradient_thickness_i[i][N]) #太薄的层不计入，实际上也不可能存在，说到底mbe（叽里咕噜...
            if current_layer is not None:
                z_position += current_layer
                grid_nodes.append(tools.get_nodes(current_layer,config.GRID_THICKNESS_SL))
                cluster_i[i].append(layer_num + 1)
                grid_lines.append(f" {z_position:.3f}d0") #输出时缩短为3位小数，但z_position本身还是原始精度继续运算
                grid_factors.append("1d0")
                layer_num += 1
    print(f"当前超晶格顶端位置为{z_position:.3f}，是第{layer_num}个region")
    return z_position,layer_num,grid_lines,grid_nodes,grid_factors,*cluster_i

if __name__ == "__main__":
    #输出文件，采用w模式
    output_1 = "./region_output.txt"
    output_2 = "./grid_cluster_output.txt"
    tools.remove_if_exists(output_1)
    tools.remove_if_exists(output_2)

    #输出单元，更多的cluster需要手动添加。
    grid_lines = ["0d0",]
    grid_nodes = []
    grid_factors = []
    cluster1 = [] #InAs
    cluster2 = [] #GaSb
    cluster3 = [] #AlSb

    former_z: float = 0 #初始化Z轴位置和层数
    former_n: int = 0

    #1 600nm GaSb
    thickness_1:float = 600
    former_z, former_n, grid_lines, grid_nodes, grid_factors, cluster2 = single_layer(former_z, former_n,
                                                    thickness_1, grid_lines, grid_nodes, grid_factors, cluster2)
    #2  9.39nm InAs/4.27nm GaSb
    #周期数和单层厚度
    loop1: int = 205
    sl_a = 9.39
    sl_b = 4.27
    # 添加数据到字符串中,通过传参（cluster12/13/23 → clusterAB）来让不同的结构调用同一个生成函数,务必注意cluster对应关系
    former_z,former_n,grid_lines,grid_nodes,grid_factors,cluster1,cluster2 = sl_2_layer(former_z, former_n,
                            loop1, grid_lines, grid_nodes, grid_factors, sl_a, cluster1, sl_b, cluster2)

    #3  9.39nm InAs/(0,2.45)nm AlSb/(4.27,0)nm GaSb
    loop2: int = 38
    sl_a = 9.39
    sl_b = (0,2.45)
    sl_c = (4.27,0)
    #复制前面模块时注意，形参的loop1要改为loop2!!!
    former_z, former_n, grid_lines, grid_nodes, grid_factors, cluster1, cluster3, cluster2 = sl_multi_layer(former_z, former_n,loop2,
                                                                                                            grid_lines,grid_nodes, grid_factors,
                                                                                                            sl_a,cluster1,
                                                                                                            sl_b, cluster3,
                                                                                                            sl_c, cluster2
                                                                                                            )
    #4 9.39nm InAs/2.45nm AlSb
    loop3: int = 20
    sl_a = 9.39
    sl_b = 2.45
    former_z, former_n, grid_lines, grid_nodes, grid_factors, cluster1, cluster3 = sl_2_layer(former_z, former_n,
                                                                                                  loop3, grid_lines, grid_nodes, grid_factors,
                                                                                                  sl_a, cluster1, sl_b, cluster3)
    #5 10nm InAs
    thickness_2:float = 10
    #复制前面模块时注意，形参的thickness_1要改为thickness_2!
    former_z, former_n, grid_lines, grid_nodes, grid_factors, cluster1 = single_layer(former_z, former_n,
                                                                                      thickness_2, grid_lines, grid_nodes, grid_factors, cluster1)

    output.region(output_1,grid_lines)
    output.grid_and_cluster(output_2,grid_lines,grid_nodes,grid_factors,cluster1,cluster2,cluster3)

    wait = input()
