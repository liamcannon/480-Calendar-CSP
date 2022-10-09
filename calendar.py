from xml import dom
from typing import Dict, List, NamedTuple, Optional
from csp import CSP, Constraint
from copy import deepcopy

# Calendar CSP problem

# room class

# Course class
class RoomSchedule(NamedTuple):
    room: str
    schedule: List[List[str]]

class Room(NamedTuple):
    name: str

class Professor(NamedTuple):
    name: str
    schedule: List[List[Room]]

class Course(NamedTuple):
    name: str
    room: Room
    professor: Professor
    doubleBlock: bool = False
# Schedule class

class Schedule(NamedTuple):
    schedule: List[List[Course]]
    


def generate_grid(rows: int, columns: int) -> Schedule:
    # initialize grid with random letters
    return [["-" for c in range(columns)] for r in range(rows)]


def display_grid(grid: Schedule) -> None:
    for row in grid:
        print("".join(row))

def generate_domain(course: Course, schedule: Schedule) -> List[Schedule]:
    # initialize grid with random letters
    # deep copy schedule
    # copySchedule = deepcopy(schedule)

    SCHEDULE_WIDTH = len(schedule)
    SCHEDULE_LENGTH = len(schedule[0])


    domain: List[Schedule]

    # if(schedule.doubleBlock):
        # generate domain for double block courses (1x2)
        
    for row in range(len(schedule.schedule)):
        for column in range(len(schedule.schedule[row])):
            if(schedule.doubleBlock):
                if(column < SCHEDULE_WIDTH - 1):
                    if(schedule.schedule[row][column] == "-" and schedule.schedule[row][column + 1] == "-"):
                        tempCopy = deepcopy(schedule)
                        tempCopy.schedule[row][column] = course.name
                        tempCopy.schedule[row][column + 1] = course.name
                        domain.append(tempCopy)
            else:
                # generate domain for single block courses (1x1)
                for row in range(2):
                    for column in range(2):
                        if(schedule.schedule[row][column] == "-"):
                            tempCopy = deepcopy(schedule)
                            tempCopy.schedule[row][column] = course.name
                            domain.append(tempCopy)
    return domain

class ScheduleConstraint(Constraint[Course, List[Schedule]]):
    # can't have same class twice on same day
    # can't have same class twice on same time
    # can't have overlapping classes in the same room
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)

    def satisfied(self, assignment: Dict[Course, List[Schedule]]) -> bool:
        tempList = List[List[Schedule]]
        # check if any courses overlap
        
        
    # def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
    #     # constraint = [pos for values in assignment.values() for pos in values]
    #     all_locations = [locs for values in assignment.values() for locs in values]
    #     #FROM BOOK 
    #     return len(set(all_locations)) == len(all_locations)

# class RoomConstraint(Constraint[Chip, List[GridLocation]]):
#     def __init__(self, chips: List[Chip]) -> None:
#         super().__init__(chips)
        
#     def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
#         # constraint = [pos for values in assignment.values() for pos in values]
#         all_locations = [locs for values in assignment.values() for locs in values]
#         #FROM BOOK 
#         return len(set(all_locations)) == len(all_locations)

# class CourseConstraint(Constraint[Chip, List[GridLocation]]):
#     def __init__(self, chips: List[Chip]) -> None:
#         super().__init__(chips)
        
#     def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
#         # constraint = [pos for values in assignment.values() for pos in values]
#         all_locations = [locs for values in assignment.values() for locs in values]
#         #FROM BOOK 
#         return len(set(all_locations)) == len(all_locations)


