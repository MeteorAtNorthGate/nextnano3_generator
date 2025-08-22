def example_function(arg1, arg2, *args, kwarg1, kwarg2, **kwargs):
    print(f"arg1: {arg1}")
    print(f"arg2: {arg2}")
    print(f"*args: {args}")
    print(f"kwarg1: {kwarg1}")
    print(f"kwarg2: {kwarg2}")
    print(f"**kwargs: {kwargs}")

if __name__ == "__main__":
    # 正确的调用方式
    example_function(1, 2, 3, 4, kwarg1="a", kwarg2="b", key1="value1", key2="value2")

    # 输出:
    # arg1: 1
    # arg2: 2
    # *args: (3, 4)
    # kwarg1: a
    # kwarg2: b
    # **kwargs: {'key1': 'value1', 'key2': 'value2'}