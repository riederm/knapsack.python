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
        return ks

def solve(availableItems: List, ks: Knapsack) -> int:
    if len(availableItems) == 0:
        print(f"Knapsack: {ks.value} {ks.items}")
        return ks.value    #we did not add anything

    #take first item from the available list
    item = availableItems[0]

    newKnapsack = ks.copy()
    #can we add?
    notAdded = solve(availableItems[1:], newKnapsack)

    if ks.hasRoomFor(item):
        newKnapsack.addItem(item)
        added = solve(availableItems[1:], newKnapsack)
        return max(notAdded, added)
    
    else:
        return notAdded


items = [
    Item("A", 3, 2), 
    Item("B", 1, 2), 
    Item("C", 3, 4), 
    Item("D", 4, 5), 
    Item("E", 2, 3)]

print(solve(items, Knapsack(7)))
