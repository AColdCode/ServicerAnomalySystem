"""
single_metric_detection.sliding_window

滑动窗口数据结构
"""

from collections import deque


class SlidingWindow:
    """
    固定大小滑动窗口
    """

    def __init__(self, max_size):
        """
        初始化窗口

        Parameters
        ----------
        max_size : int
            窗口最大长度
        """

        self.max_size = max_size
        self.data = deque()

    def append(self, value):
        """
        添加新数据

        如果窗口满，则自动删除最旧数据
        """

        if len(self.data) >= self.max_size:
            self.data.popleft()

        self.data.append(value)

    def is_full(self):
        """
        判断窗口是否满
        """

        return len(self.data) == self.max_size

    def values(self):
        """
        获取窗口数据
        """

        return list(self.data)

    def mean(self):
        """
        计算窗口平均值
        """

        if len(self.data) == 0:
            return 0

        return sum(self.data) / len(self.data)

    def std(self):
        """
        计算标准差
        """

        if len(self.data) < 2:
            return 0

        mean = self.mean()

        var = sum((x - mean) ** 2 for x in self.data) / len(self.data)

        return var ** 0.5
    