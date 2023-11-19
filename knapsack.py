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
    
class ItemLookupTable:
    def __init__(self, items, maxCapacity):
        self.items = items
        self.maxCapacity = maxCapacity
        # build 2-dim table for every possible knapsack-size (cols) x item (rows)
        self.knapsacks = [[Knapsack(capacity, 0) for capacity in range(maxCapacity + 1)] for _ in range(len(items) + 1)]

    def getKnapsacksFor(self, itemIndex):
        if itemIndex < 0:
            # return a all-zero row for negative index
            return [Knapsack(0, 0) for _ in range(self.maxCapacity + 1)]
        
        return self.knapsacks[itemIndex]

    def fillTable(self):
        for iIdx, item in enumerate(self.items):
            for knapsack in self.knapsacks[iIdx]:
                previousKnapsacks = self.getKnapsacksFor(iIdx - 1);
                # the cell above us
                ksNotAdding = previousKnapsacks[knapsack.capacity];
                ksIfWeAdd = previousKnapsacks[knapsack.capacity - item.weight];
                if knapsack.hasRoomFor(item):
                    allPreviousKnapsacks = self.knapsacks[iIdx - 1];
                    if ksIfWeAdd.value + item.value > ksNotAdding.value:
                        # yes we should add the item
                        knapsack.addItem(item)
                        knapsack.value = ksIfWeAdd.value + item.value
                    else:
                        # no we should not add the item, previous knapsack is better
                        knapsack.value = ksNotAdding.value
                else:
                    # we can't add the item, so just use the previous knapsack
                    knapsack.value = ksNotAdding.value

    def getSolution(self):
        return self.getKnapsacksFor(len(self.items)-1)[self.maxCapacity].value
                

    def __repr__(self):
        tableHeaders = [];
        for i in range(self.maxCapacity + 1):
            tableHeaders.append(f"{i}kg")

        rows = [];
        for i in range(len(self.items)):
            rows.append([self.items[i]] + list(map(lambda x: f"{x.value}$", self.knapsacks[i])))            

        return tabulate(rows, headers=tableHeaders, tablefmt='fancy_grid')


items = [
    Item("A", 3, 2), 
    Item("B", 1, 2), 
    Item("C", 3, 4), 
    Item("D", 4, 5), 
    Item("E", 2, 3)]

solver = ItemLookupTable(items, 7)
solver.fillTable()
print(solver)
print(f"solution: {solver.knapsacks[4][7].value}")
print(solver)