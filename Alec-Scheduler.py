from xml import dom
from typing import Dict, List, NamedTuple, Optional
from csp import CSP, Constraint
from copy import deepcopy
from random import shuffle

# Calendar CSP problem

class Room(NamedTuple):
    name: str

#represents a professor, and their level of class they can teach
class Professor(NamedTuple):
    name: str
    level: int

#represents a course, whether its a double block, its name and what minimum level is required to teach it
class Course(NamedTuple):
    name: str
    doubleBlock: bool
    minLevel: int

#representation of a single course, which room its in and the teacher
class RoomCourse(NamedTuple):
    room: Room
    course: Course
    professor: Professor

#representation of teh schedule being used by the csp
class Schedule(NamedTuple):
    schedule: List[List[RoomCourse]]

#converts a dictionary to a schedule, with making lists of roomcourses in positions that allow for multiple classes in the same timeslot
def dict_to_schedule(variables, dict, schedule):
    newSched = deepcopy(schedule.schedule)
    list_of_domains = [dict[i].schedule for i in variables]
    for i in list_of_domains:
        for x in range(len(i)):
            for y in range(len(i[0])):
                if i[x][y] != "-":
                    if newSched[x][y] == "-":
                        newSched[x][y] = [i[x][y]]
                    else:
                        newSched[x][y].append(i[x][y])
    return newSched

def generate_grid(rows: int, columns: int) -> Schedule:
    # initialize grid with random letters
    return Schedule([["-" for c in range(columns)] for r in range(rows)])


def display_grid(grid: Schedule) -> None:
    # rotate the grid so that it displays correctly
    for i in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][i] == "-":
                print("no class", end=" | ")
            else:
                for x in range(len(grid[y][i])):
                    print(grid[y][i][x].course.name + " " + grid[y][i][x].professor.name + " " + grid[y][i][x].room.name, end="")
                    if not (x+1 >= len(grid[y][i])):
                        print(", ", end="")
                    if x+1 >= len(grid[y][i]):
                        print(" | ", end="")
        print("\n")

    

def generate_domain(course: Course, schedule: Schedule, prof: list[Professor], rooms: list[Room])-> List[Schedule]:

    SCHEDULE_WIDTH = len(schedule.schedule)
    SCHEDULE_LENGTH = len(schedule.schedule[0])
    professors = deepcopy(prof)

    domain: List[Schedule] = []

    for room in rooms:
        shuffle(professors)
        for professor in professors:
            roomCourse = RoomCourse(room, course, professor)
            if roomCourse.professor.level >= roomCourse.course.minLevel:
                # generate domain for double block course (1x2)
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
                                tempCopy.schedule[row+3][column] = roomCourse
                                domain.append(tempCopy)
    return domain


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
                                # check if room or professor overlaps 
                                if i[x][y].room == j[x][y].room or i[x][y].professor == j[x][y].professor:
                                    return False
                            #check if courses are no no classes allowed days
                            if i[x][y] != "-" or j[x][y] != "-":
                                if x == 2 and (y == 4 or y == 5):
                                    return False
                                elif x == 4 and (y == 6 or y == 7):
                                    return False
        return True

#solution function, passed courses, rooms and professors
def solution(variables: list[Course], rooms: list[Room], professors: list[Professor]) -> None:
    newSched = generate_grid(5, 8)
    variableDict = {}
    #generate domains for all courses
    for x in variables:
        variableDict[x] = generate_domain(x, deepcopy(newSched), professors, rooms)
    csp = CSP(variables, variableDict)
    csp.add_constraint(ScheduleConstraint(variables))
    genOutcome = csp.backtracking_search()
    if isinstance(genOutcome, type(None)):
        print("returned none")
    else:
        display_grid(dict_to_schedule(variables, genOutcome, newSched))


if __name__ == "__main__":
    professors: list[Professor] = [Professor("Murat", 4), Professor("David", 4), Professor("Brian", 4), Professor("Wei", 4), Professor("Sarah", 4), Professor("Frank", 4), Professor("Brent", 4), Professor("Scott", 4), Professor("Alex", 4), Professor("Eric", 4), Professor("Josh", 4)]
    rooms: list[Room] = [Room("JOYC 201"), Room("JOYC 210"), Room("JOYC 211"), Room("MIC 308")]
    # variables = [Course("300", Room("joyce110"), True , Professor("david")), Course("200", Room("joyce110"), True, Professor("david")), Course("400", Room("joyce110"), True, Professor("david"))]
    variables = [Course("120", False, 1), Course("140", False, 1), Course("180", False, 1), Course("240", False, 2), Course("230", False, 2), Course("281", False, 2), Course("280", False, 2), 
                Course("300", False, 3), Course("320", False, 3), Course("351", False, 3), Course("352", False, 3), Course("355", False, 3), Course("357", False, 3), Course("370", False, 3), 
                Course("380", False, 3), Course("480", False, 4), Course("330", False, 3), Course("340", False, 3), Course("420", False, 4), Course("440", False, 4)]
    #print(generate_domain(variables[0], newSchedule))
    solution(variables, rooms, professors)
