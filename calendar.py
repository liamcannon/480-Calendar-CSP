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
    # schedule: List[List[Room]]

class Course(NamedTuple):
    name: str
    room: Room
    doubleBlock: bool
    professor: Professor
# Schedule class

class Schedule(NamedTuple):
    schedule: List[List[Course]]
    


def generate_grid(rows: int, columns: int) -> Schedule:
    # initialize grid with random letters
    return [["-" for c in range(columns)] for r in range(rows)]


def display_grid(grid: Schedule) -> None:
    # rotate the grid so that it displays correctly
    rotated_grid = list(zip(*grid))
    for row in rotated_grid:
        print(row)

def generate_domain(course: Course, schedule: Schedule) -> List[Schedule]:

    SCHEDULE_WIDTH = len(schedule.schedule)
    SCHEDULE_LENGTH = len(schedule.schedule[0])


    domain: List[Schedule] = []

    # if(schedule.doubleBlock):
        # generate domain for double block courses (1x2)
        
    if course.doubleBlock:    
        for row in range(len(schedule.schedule)):
            for column in range(len(schedule.schedule[row])):
                if(column + 1 <= SCHEDULE_LENGTH-1):
                    if(schedule.schedule[row][column] == "-" and schedule.schedule[row][column + 1] == "-"):
                        tempCopy = deepcopy(schedule)
                        tempCopy.schedule[row][column] = course.name
                        tempCopy.schedule[row][column + 1] = course.name
                        domain.append(tempCopy)
    else:
        # generate domain for single block courses (1x1)
        for row in range(2):
            for column in range(len(schedule.schedule[0])):
                if(schedule.schedule[row][column] == "-"):
                    tempCopy = deepcopy(schedule)
                    tempCopy.schedule[row][column] = course.name
                    domain.append(tempCopy)
    return domain

class TempConstraint(Constraint[Course, list[Schedule]]):
    def __init__(self, variables: list[Schedule]):
        self.variables: list[Schedule] = variables

    def satisfied(self, variableDict: Dict):
        #print(variableDict)
        stuff = [locs for values in variableDict.values() for locs in values]
        schedule = Schedule([["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]])
        for z in stuff:
            for i in range(len(schedule)):
                for y in range(len(schedule[0])):
                    if z[i][y] != "-" and schedule[i][y] == "-":
                        schedule[i][y] = z[i][y]
                    else:
                        if schedule[i][y] != "-":
                            return False
        return True


class ScheduleConstraint(Constraint[Course, List[Schedule]]):
    # can't have same class twice on same day
    # can't have same class twice on same time
    # can't have overlapping classes in the same room
    def __init__(self, variables: List[Course]) -> None:
        self.variables: List[Course] = variables

    def satisfied(self, assignment: Dict) -> bool:
        # check if any courses overlap
        values = [locs for values in assignment.values() for locs in values]
        for i in values:
            for j in values:
                if i != j:
                    for x in range(len(i)):
                        for y in range(len(i[0])):
                            if i[x][y] != "-" and j[x][y] != "-":
                                return False
        return True
        
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

def solution() -> None:
    # generate grid
    schedule = generate_grid(2, 5)
    display_grid(schedule)
    # generate domain
    # generate constraints
    # generate CSP
    # solve CSP
    # display solution


if __name__ == "__main__":
    newSchedule = Schedule([["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]])
    variables = [Course("300", Room("joyce110"), True , Professor("david")), Course("200", Room("joyce110"), True, Professor("david")), Course("400", Room("joyce110"), True, Professor("david"))]
    variableDict = {}
    #print(generate_domain(variables[0], newSchedule))
    for x in variables:
        variableDict[x] = generate_domain(x, deepcopy(newSchedule))
    # print(variableDict)
    for i in [locs for values in variableDict.values() for locs in values]:
        display_grid(i.schedule)
        print("\n")
    # stuff = [locs for values in variableDict.values() for locs in values]
    testCSP = CSP(variables, variableDict)
    # testCSP.add_constraint(TempConstraint(variables))
    testCSP.add_constraint(ScheduleConstraint(variables))
    possibleOutcome = testCSP.backtracking_search()
    if isinstance(possibleOutcome, type(None)):
        print("returned none")
    else:
        print("got something back")
        print(possibleOutcome)
