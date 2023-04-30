class CircularQueue:

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.array = [None] * max_size
        self.front = 0
        self.rear = 0
        self.size = 0


