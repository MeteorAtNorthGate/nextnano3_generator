import tools

def region(outpath,grid_lines):
    region_num = len(grid_lines)-1
    with open(outpath, "w") as f:
        f.write("$regions \n")
        for i in range(region_num):
            f.write(f" region-number = {i+1}     base-geometry = line     region-priority = 1\n z-coordinates = {grid_lines[i]}   {grid_lines[i+1]}\n\n")
        f.write("$end_regions                                                                !\n")

def grid_and_cluster(outpath,grid_lines, grid_nodes, grid_factors, *cluster_i):
    tools.add_cap(*cluster_i) #添加
    # 拼接列表为字符串，过长时换行符分割。
    grid_lines_str, grid_nodes_str, grid_factors_str, *cluster_i_str = tools.merge_and_split(grid_lines, grid_nodes, grid_factors, *cluster_i)

    with open(outpath, "w") as f:
        # 写入文件
        f.write(f" z-grid-lines     ={grid_lines_str}\n")
        f.write(f" z-nodes          ={grid_nodes_str}\n")
        f.write(f" z-grid-factors   ={grid_factors_str}\n")
        for i in range(len(cluster_i_str)):
            f.write(f" cluster-number = {i+1}    region-numbers ={cluster_i_str[i]}\n")