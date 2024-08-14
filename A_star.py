from data_structures.Priority_queue import priority_queue
from data_structures.Problem import problem 
import numpy

def heristic(possible_step:numpy.ndarray, recent_step:numpy.ndarray, target:numpy.ndarray, bonus_locations:numpy.ndarray) -> float:   
    return h1(possible_step, recent_step, bonus_locations) + h2(possible_step, recent_step, bonus_locations)

#check if it move 1 to bonus location or move 2 out of bonus location 
def h1(possible_step:numpy.ndarray, recent_step:numpy.ndarray, bonus_locations:numpy.ndarray) -> float:
    bonus_location_coordinates = numpy.array(list(zip(*numpy.nonzero(bonus_locations))))
    for bonus_location_coordinate in bonus_location_coordinates: 
        difference = possible_step[*bonus_location_coordinate] - recent_step[*bonus_location_coordinate]
        if difference == 1 or difference == -2:
            return 0
    return 1

#the sum of distance from 1s to bonus location 
def h2(possible_step:numpy.ndarray, recent_step:numpy.ndarray, bonus_locations:numpy.ndarray) -> float:
    bonus_location_coordinates = numpy.array(list(zip(*numpy.nonzero(bonus_locations))))
    not_one_mask = recent_step != 1   
    one_only = numpy.array(recent_step)[not_one_mask] = 0
    one_coordinates = numpy.array(list(zip(*numpy.nonzero(recent_step)))) 
    distance_sum = 0
    for bonus_location_coordinate in bonus_location_coordinates:
        for one_coordinate in one_coordinates:
            distance_sum += abs(numpy.linalg.norm(bonus_location_coordinate - one_coordinate))
    return distance_sum


def find_possible_next_steps(recent_step:numpy.ndarray, bonus_locations:numpy.ndarray) -> list[numpy.ndarray]:
    possible_next_steps = []
    possible_movements = numpy.array([[1,0], [-1,0], [0,1], [0,-1]])
    bonus_location_free = True
    for location in numpy.ndindex(recent_step.shape):  
        location = numpy.array(location)
        if recent_step[*location] != 0:
            if bonus_location_free and bonus_locations[*location] == 0 or recent_step[*location] == 2:
                for movement in possible_movements: 
                    possible_next_step = numpy.array(recent_step)
                    moved_location = location + movement 
                    if numpy.all(moved_location >= 0) and moved_location[0] < recent_step.shape[0] and moved_location[1] < recent_step.shape[1] and recent_step[*moved_location] == 0:
                        value = recent_step[*location]
                        possible_next_step[*location] = 0
                        possible_next_step[*moved_location] = value
                        possible_next_steps.append(possible_next_step)
            elif bonus_locations[*location] == 1:
                if bonus_location_free:
                    bonus_location_free = False
                    possible_next_steps = []
                possible_next_step = numpy.array(recent_step)
                possible_next_step[*location] = 2
                possible_next_steps.append(possible_next_step)

    return possible_next_steps                     
            
              
def A_star(puzzle:numpy.ndarray, bonus_locations:numpy.ndarray, target:numpy.ndarray, heristic_function:callable) -> list:
    possible_steps_queue = priority_queue(reverse=True)  
    possible_steps_queue.put(puzzle,0)
    previous_steps = {puzzle.tobytes() : None} 
    costs = {puzzle.tobytes() : 0}

    while not possible_steps_queue.is_empty():
        recent_step = possible_steps_queue.pop_next()
        if numpy.all(recent_step == target):
            break
        next_steps = find_possible_next_steps(recent_step, bonus_locations)
        for next_step in next_steps:
            next_step_cost = costs[recent_step.tobytes()] + 1 
            if next_step.tobytes() not in costs or next_step_cost < costs[next_step.tobytes()]:
                costs[next_step.tobytes()] = next_step_cost 
                previous_steps[next_step.tobytes()] = recent_step
                possible_steps_queue.put(next_step, next_step_cost + heristic_function(next_step, recent_step, target, bonus_locations))
    result_path = [] 
    step = target
    while numpy.any(step != puzzle):
        result_path.insert(0, step)
        step = previous_steps[step.tobytes()]
    
    return result_path


s = numpy.array([[1, 0, 1], 
                 [1, 0, 1]])    

b = numpy.array([[0, 0, 0], 
                 [1, 0, 0]])

t = numpy.array([[2, 0, 2], 
                 [2, 0, 2]])

# results =  find_possible_next_steps(s,b)
# for result in results:
#     print(result)
solution = A_star(s, b, t, heristic)

print(len(solution))
for step in solution: 
    print(step,"\n")
    
     
    

