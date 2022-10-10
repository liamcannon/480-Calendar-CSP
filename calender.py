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
    doubleBlock: bool
# Schedule class

class RoomCourse(NamedTuple):
    room: Room
    course: Course
    # Need to add when we update domain to contain professors
    # professor: Professor

class Schedule(NamedTuple):
    schedule: List[List[RoomCourse]]

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
    rotated_grid = list(zip(*grid))
    for row in rotated_grid:
        print(row)

def generate_domain(course: Course, schedule: Schedule) -> List[Schedule]:

    SCHEDULE_WIDTH = len(schedule.schedule)
    SCHEDULE_LENGTH = len(schedule.schedule[0])
    rooms: List[str] = [Room("JOYC 201"), Room("JOYC 210"), Room("JOYC 211"), Room("MIC 308")]


    domain: List[Schedule] = []

    # if(schedule.doubleBlock):
        # generate domain for double block courses (1x2)
    for room in rooms:
        roomCourse = RoomCourse(room, course)
        if course.doubleBlock:    
            for row in range(SCHEDULE_WIDTH):
                for column in range(SCHEDULE_LENGTH):
                    if(column + 1 <= SCHEDULE_LENGTH-1):
                        if(schedule.schedule[row][column] == "-" and schedule.schedule[row][column + 1] == "-"):
                            tempCopy = deepcopy(schedule)
                            tempCopy.schedule[row][column] = roomCourse
                            tempCopy.schedule[row][column + 1] = roomCourse
                            domain.append(tempCopy)
        else:
            # generate domain for single block courses (1x1)
            for row in range(2):
                for column in range(len(schedule.schedule[0])):
                    if(schedule.schedule[row][column] == "-"):
                        tempCopy = deepcopy(schedule)
                        tempCopy.schedule[row][column] = roomCourse
                        tempCopy.schedule[row+2][column] = roomCourse
                        domain.append(tempCopy)
    return domain

""" def OLD_generate_domain(course: Course, schedule: Schedule) -> List[Schedule]:

    SCHEDULE_WIDTH = len(schedule.schedule)
    SCHEDULE_LENGTH = len(schedule.schedule[0])



    domain: List[Schedule] = []

    # if(schedule.doubleBlock):
        # generate domain for double block courses (1x2)
    
    if course.doubleBlock:    
        for row in range(SCHEDULE_WIDTH):
            for column in range(SCHEDULE_LENGTH):
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
    return domain """

# class TempConstraint(Constraint[Course, list[Schedule]]):
#     def __init__(self, variables: list[Schedule]):
#         self.variables: list[Schedule] = variables

#     def satisfied(self, variableDict: Dict):
#         #print(variableDict)
#         stuff = [locs for values in variableDict.values() for locs in values]
#         schedule = Schedule([["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]])
#         for z in stuff:
#             for i in range(len(schedule)):
#                 for y in range(len(schedule[0])):
#                     if z[i][y] != "-" and schedule[i][y] == "-":
#                         schedule[i][y] = z[i][y]
#                     else:
#                         if schedule[i][y] != "-":
#                             return False
#         return True


class ScheduleConstraint(Constraint[Course, List[Schedule]]):
    # can't have same class twice on same day
    # can't have same class twice on same time slot
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
                                if i[x][y].room == j[x][y].room:
                                    return False
                                return False
        return True

def solution() -> None:
    # generate grid
    schedule = generate_grid(2, 5)
    # generate domain
    # generate constraints
    # generate CSP
    # solve CSP
    # display solution


if __name__ == "__main__":
    newSchedule = Schedule([["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]])
    # variables = [Course("300", Room("joyce110"), True , Professor("david")), Course("200", Room("joyce110"), True, Professor("david")), Course("400", Room("joyce110"), True, Professor("david"))]
    variables = [Course("300", True), Course("200", False), Course("400", True)]
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
        #display_grid(dict_to_schedule(variables, possibleOutcome, newSchedule))
        
