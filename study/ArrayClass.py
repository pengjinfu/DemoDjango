import random
import re
import statistics


class ArrayClass:
    def __init__(self, name, init_arr):
        self.name = name
        self.init_arr = init_arr

    def to_string(self):
        return self.name

    def demo_arr(self):
        arr = ['a', 'b', 'c']
        return arr.append(self.name)

    def demo_if(self):

        if isinstance(self.name, int):
            exit("Name is not an integer !")

        if self.name == 'A':
            return self.name

        elif self.name == 'B':
            return self.name + 'BBB'

        else:
            return self.name + 'CCC'

    def set_name(self, value):
        self.name = value

    def __str__(self):
        return 'it is file to string ' + self.name

    def add_arr(self, new_arr):
        # 支持数据的直接累加
        #

        return self.init_arr + new_arr

    def demo_fib(self, num):
        a, b = 0, 1
        data = []
        while a < num:
            data.append(a)
            a = b
            b = a + b

        return data

    def demo_for(self, result):
        for w in result:
            print(w)

    def demo_even(self, num):

        # 返回数组中构思的个数
        for n in range(2, num):
            if n % 2 == 0:
                print("Found an even number", n)
                continue
        print("Found a number", num)

    def demo_in_array(self, value):
        if value in self.init_arr:
            return True

    def demo_stack(self):
        stack = [1, 3, 5, 8, 4]
        stack.append(6)
        return stack

    def demo_matrix(self):
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ]

    def demo_format(self):
        print('{0} and {1}'.format('aaa', 'bbb'))

    def regular(self, str):
        re.findall(r'\bf[a-z]*', str)

    def demo_random(self, arr):
        value = random.choice(arr)
        return value

    def demo_stat(self, arr):
        # python 的均值和方差， 该statistics模块计算数值数据的基本统计属性（均值，中位数，方差等）
        # data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
        statistics.mean(arr)
        statistics.median(arr)
        statistics.variance(arr)

    def demo_empty(self, key):
        arr = [{"a": 1, "b": 2}]
        if key is not None and hasattr(arr, key):
            print("{0} key is exist ", key)


pass
