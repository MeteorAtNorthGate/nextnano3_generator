import sys

my_list = []
print(f"Empty list size: {sys.getsizeof(my_list)} bytes")

for i in range(1000):
    my_list.append(i)
    # 每次 append 后打印大小，你会看到大小并不是线性增长，而是在达到某个阈值后跳跃性增长
    # 这就是过度分配的体现
    print(f"List with {len(my_list)} elements size: {sys.getsizeof(my_list)} bytes")