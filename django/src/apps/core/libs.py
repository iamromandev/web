class CircularQueue:

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.array = [None] * max_size
        self.front = 0
        self.rear = 0
        self.size = 0

    def enqueue(self, item):
        if self.size >= self.max_size:
            raise Exception('Queue is full')

        self.array[self.rear] = item
        self.rear = (self.rear + 1) % self.max_size
        self.size += 1
        return self

    def dequeue(self):
        if self.size == 0:
            raise Exception('Underflow')

        item = self.array[self.front]
        self.array[self.front] = None
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        return item

    def peek(self):
        if self.size == 0:
            raise Exception('Underflow')

        return self.array[self.front]

    def iterate(self):
        self.enqueue(self.dequeue())
