#problem class for create problem 
import numpy
from typing import List, SupportsInt


class illegalMovement(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        (from_x, from_y, to_x, to_y) = args
        print(f"\n!!! WRONG SOLUTION --> illegal movement from <{from_x}, {from_y}> to <{to_x}, {to_y}> because target location have a non-zero value <-- WRONG SOLUTION !!!\n")


class bonusLocationOccupied(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print("\n!!! WRONG SOLUTION --> bonus location occupied, empty bonus location immidately after adding bonus to the puzzle <-- WRONG SOLUTION !!!\n")


class problem:
    def __init__(self, puzzle_board:numpy.array, answer_board:numpy.array, bonus_location_xy:numpy.array) -> None:
        '''
        init method for the problem

        args:
            puzzle_board(numpy.array): the layout of the puzzle, should be a numpy array contain only 0 and 1
            bonus_location_xy(numpy.array): the coordinate of the location with bonus
        
        return: 
            no return value 
        '''
        self.movement_count = 0
        self.y_movement_count = 0
        self.x_movement_count = 0
        self.puzzle_x_size = puzzle_board.shape[0]
        self.puzzle_y_size = puzzle_board.shape[1] 
        self.puzzle_board = puzzle_board
        self.answer_board = answer_board 
        self.bonus_board = numpy.zeros(self.puzzle_board.shape)
        self.bonus_board[bonus_location_xy[0]][bonus_location_xy[1]] = 1
        self.bonus_location = bonus_location_xy


    def add_bonus(self) -> None:
        '''
        add bonus to the bonus location 

        args: 
            no argument 

        return: 
            no return value 
        '''
        if self.puzzle_board[self.bonus_location[0]][self.bonus_location[1]] > 0: 
            self.puzzle_board = self.puzzle_board + self.bonus_board

        if self.puzzle_board[self.bonus_location[0]][self.bonus_location[1]] > 2:
            raise bonusLocationOccupied()


    def can_move(self, destination_xy:numpy.array) -> bool:
        '''
        determine if this target position is a moveable position
        args: 
            destination_xy(numpy.array): the coordinate of destination of this movement
        return:
            bool: if this location is occupied recently, which is if this location's value is not zero
        '''
        return self.puzzle_board[destination_xy[0]][destination_xy[1]] == 0

     
    def move_x_or_y(self, from_xy:numpy.array, direction:float, axis:float) -> None:
        '''
        move puzzle on given position along given axis on given direction

        args: 
            from_xy(numpy.array): the coordinate of target puzzle  
            direction(float): direction flag, positive value for move 1 unit, negative value for move -1 unit 
            axis(float): axis flag, positive value for move one x axis, negative value for move one y axis  

        return: 
            no return value  
        '''
        if direction < 0:
            direction = -1
        elif direction > 0:
            direction = 1

        destination_xy = numpy.array(from_xy)
        if axis > 0:
            self.x_movement_count = self.x_movement_count + 1
            destination_xy[0] = destination_xy[0] + direction
        elif axis < 0: 
            self.y_movement_count = self.y_movement_count + 1
            destination_xy[1] = destination_xy[1] + direction

        if not self.can_move(destination_xy):
            raise illegalMovement(from_xy[0], from_xy[1], destination_xy[0], destination_xy[1])
        else:
            self.puzzle_board[destination_xy[0]][destination_xy[1]] = self.puzzle_board[from_xy[0]][from_xy[1]]
            self.puzzle_board[from_xy[0]][from_xy[1]] = 0
        
        self.movement_count = self.movement_count + 1


    def move_x(self, from_xy:numpy.array, direction:float) -> None:
        '''
        move puzzle on given position along x axis

        args: 
            from_xy(numpy.array): the coordinate of target puzzle  
            direction(float): direction flag, positive value for move 1 unit, negative value for move -1 unit  

        return: 
            no return value
        '''
        self.move_x_or_y(from_xy = from_xy, direction = direction, axis = 1)


    def move_y(self, from_xy:numpy.array, direction:float) -> None:
        '''
        move puzzle on given position along y axis

        args: 
            from_xy(numpy.array): the coordinate of target puzzle  
            direction(float): direction flag, positive value for move 1 unit, negative value for move -1 unit  

        return: 
            no return value
        '''
        self.move_x_or_y(from_xy = from_xy, direction = direction, axis = -1)
     

    def value(self, target_xy:numpy.array) -> int:
        '''
        get value on certain position

        args: 
            target_xy(numpy.array): coordinate to check 

        return: 
            int: the value at given coordinate 
        '''
        return self.puzzle_board[target_xy[0], target_xy[1]]
    

    def is_soving_completed(self) -> bool:
        '''
        check if this problem is completely solved 

        args: 
            no arguments

        return: 
            bool: if this puzzle is fully solved
        '''
        return self.puzzle_board - self.answer_board == 0
          
        
    


        

         