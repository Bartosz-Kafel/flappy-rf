import math

class CMath():
    def __init__(self):
        pass

    def calcGini(self, data):
        count = {}
        if len(data) == 0:
            return 0.0
        
        for i in data:
            count[i] = count.get(i, 0) + 1

        squared_total = 0
        for key, value in count.items():
            procentile = value / len(data)
            squared_total += procentile ** 2

        return 1 - squared_total



