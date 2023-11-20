from tabulate import tabulate
from typing import List
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Item:
    def __init__(self, name, weight, value):
        self.weight = weight
        self.value = value
        self.name = name

    def __repr__(self):
        return f"{self.name}({self.weight}kg, {self.value}$)"

class Knapsack:
    def __init__(self, capacity, initial_value = 0):
        self.capacity = capacity
        self.items = []
        self.value = initial_value

    def hasRoomFor(self, item):
        return self.capacity >= item.weight + sum(map(lambda x: x.weight, self.items))
    
    def addItem(self, item):
        self.items.append(item)
        self.value += item.value

    def getItemList(self):
        return list(map(lambda x: x.name, self.items))

    def __repr__(self):
        return f"Knapsack({self.capacity}kg)"
    
    def copy(self):
        ks = Knapsack(self.capacity, self.value)
        ks.items = self.items.copy()
        return ks75

    def isOverfilled(self):
        totalWeight = 0
        for item in self.items:
            totalWeight = item.weight + totalWeight
        if (totalWeight <= self.capacity):
            return False
        else:
            return True


# brute force approach
def solve(availableItems: List, ks: Knapsack, currentIndex) -> int:
    if (currentIndex > len(availableItems) - 1):
        print(ks.items)
        # if the knapsack is overfilled
        # we consider it broken --> 0$
        if(ks.isOverfilled()):
            return 0
        else:
            return ks.value
    ItemA = availableItems[currentIndex]
    KnapsackWithoutaItem = ks.copy()
    ks.addItem(ItemA)
    ExcludeCurrentItem = solve(availableItems, KnapsackWithoutaItem, currentIndex + 1)
    IncludeCurrentItem = solve(availableItems, ks, currentIndex + 1)
    return max(ExcludeCurrentItem, IncludeCurrentItem)

   
    


items = [
    Item("A", 3, 2), 
    Item("B", 1, 2), 
    Item("C", 3, 4), 
    Item("D", 4, 5), 
    Item("E", 2, 3)]

print(solve(items, Knapsack(7), 0))
