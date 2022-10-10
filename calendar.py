import sched
from xml import dom
from typing import Dict, List, NamedTuple, Optional
from copy import deepcopy
from csp import CSP, Constraint

# Calendar CSP problem

# room class

# Course class
class RoomSchedule(NamedTuple):
    #room: str
    schedule: List[List[str]]

class Room(NamedTuple):
    name: str

class Professor(NamedTuple):
    name: str
    #schedule: List[List[str]]

class Course(NamedTuple):
    name: str
    room: Room
    doubleBlock: bool
    professor: Professor
# Schedule class

class Schedule(NamedTuple):
    schedule: List[List[Course]]
    
def dict_to_schedule(variables, dict, schedule):
    newSched = deepcopy(schedule.schedule)
    list_of_domains = [dict[i].schedule for i in variables]
    for i in list_of_domains:
        for x in range(len(i)):
            for y in range(len(i[0])):
                if i[x][y] != "-":
                    newSched[x][y] = i[x][y]
    return newSched

def generate_grid(rows: int, columns: int) -> Schedule:
    # initialize grid with random letters
    return [["-" for c in range(columns)] for r in range(rows)]


def display_grid(grid: Schedule) -> None:
    # rotate the grid so that it displays correctly
    """rotated_grid = list(zip(*grid))
    for row in rotated_grid:
        for i in row:
            if isinstance(i, type(str)):
                print("-", end="")
            else:
                print(i.course, end="")
        print("\n")"""
    for i in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][i] == "-":
                print("-", end="")
            else:
                print(grid[y][i].course.name, end="")
        print("\n")

def generate_domain(course: Course, schedule: Schedule) -> List[Schedule]:
    # initialize grid with random letters
    # deep copy schedule
    # copySchedule = deepcopy(schedule)

    SCHEDULE_WIDTH = len(schedule)
    SCHEDULE_LENGTH = len(schedule[0])


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
class tempConstraint(Constraint[Course, list[Schedule]]):
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

if __name__ == "__main__":
    newSchedule = Schedule([["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]])
    variables = [Course("300", Room("joyce110"), False, Professor("david")), Course("200", Room("joyce110"), False, Professor("david")), Course("400", Room("joyce110"), False, Professor("david"))]
    variableDict = {}
    #print(generate_domain(variables[0], newSchedule))
    for x in variables:
        variableDict[x] = generate_domain(x, deepcopy(newSchedule))
    print(variableDict)
    #stuff = [locs for values in variableDict.values() for locs in values]
    testCSP = CSP(variables, variableDict)
    testCSP.add_constraint(tempConstraint(variables))
    possibleOutcome = testCSP.backtracking_search()
    if isinstance(possibleOutcome, type(None)):
        print("returned none")
    else:
        print("got something back")
        print(possibleOutcome)
    #print("hello")


