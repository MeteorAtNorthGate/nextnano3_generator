#coding = utf-8
# 全局常量
# 超晶格结构中单层的节点间距离，取2或1比较合适。
GRID_THICKNESS_SL = 2
# 单层的节点间距离，单层都比较厚就提高，比较复杂（薄）就降低。 比方说600nm/20 就是30个点
GRID_THICKNESS_SINGLE = 20
# 网格最小尺寸，向0渐变可能会取到很薄的厚度，这没有意义，因此 0~THIN/2 = 0 THIN/2~THIN = THIN 这样来约束
#GRID_THINNEST = 0.64 #III-V族半导体单个晶胞的厚度（monolayer)在0.5~0.6nm左右
GRID_THINNEST = 0.5 #nextnano文档的说明，1nm中节点不超过两个
