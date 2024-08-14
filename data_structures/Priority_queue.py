import numpy
from typing import List


class priority_queue:
    class queue_cell:
        def __init__(self, value, weight:float) -> None:
            self.value = value
            self.weight = weight 


    def __init__(self,  reverse:bool = False) -> None:
        self.queue: List[self.queue_cell] = []
        self.reverse = reverse
    

    def __get_weight(self, cell:queue_cell) -> queue_cell: 
        return cell.weight


    def put(self, value, weight:float) -> None:
        '''
        add one more cell to the queue and make them in the ascent/decent order of weight 

        args:
            value: the value of this cell, can be anything
            weight(float): the weight of this cell in float point number repreasent the priority of this cell in this queue

        return:
            no return value 
        '''
        self.queue.append(self.queue_cell(value, weight))
        self.queue.sort(key = self.__get_weight, reverse = self.reverse)


    def peek_next(self):
        '''
        get the value of the next value in the queue but do not remove it

        args:
            no argument
        
        return: 
           Object: the value of the next queue cell  
        '''
        cell = self.queue[-1]
        return cell.value
    

    def pop_next(self):
        '''
        pop the value of the next value in the queue 

        args:
            no argument
        
        return: 
           Object: the value of the next queue cell  
        '''
        cell = self.queue.pop() 
        return cell.value


    def is_empty(self) -> bool:
        return len(self.queue) == 0



