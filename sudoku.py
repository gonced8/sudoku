import math
import time
import copy
import random
import sys


class Entry:
    def __init__(self, solved=False, checked=False, number=list(range(1, 10)), i=-1, j=-1):
        self.solved = solved
        self.checked = checked
        if number==0 :
            self.number = list(range(1, 10))
        else:
            self.number = number
        self.i = i
        self.j = j


class Hypotesis:
    def __init__(self, assumption, table):
        self.assumption = assumption
        self.table = table


def loadtxt(filename):
    file = open(filename, 'r')
    matrix = [list(map(int, line.split())) for line in file]
    file.close()
    return matrix


def import_sudoku(filename):
    matrix = loadtxt(filename)
    table = []
    for i in range(len(matrix)):
        aux=[]
        for j in range(len(matrix[i])):
            aux.append(Entry(matrix[i][j]!=0, False, matrix[i][j], i, j))
        table.append(aux)
    return matrix, table


def get_row(table, i):
    return table[i][:]


def get_row2(table, i, j):
    return table[i][:j]+table[i][j+1:]


def get_row3(table, i, j):
    dim = int(math.sqrt(len(table)))
    return table[i][:j//dim*dim]+table[i][(j//dim+1)*dim:]


def get_column(table, j):
    return [table[i][j] for i in range(len(table))]


def get_column2(table, i, j):
    array = [table[i][j] for i in range(len(table))]
    del array[i]
    return array


def get_column3(table, i, j):
    dim = int(math.sqrt(len(table)))
    array = [table[i][j] for i in range(i//dim*dim)]
    array += [table[i][j] for i in range((i//dim+1)*dim, len(table))]
    return array


def get_block(table, x):
    array=[]
    dim = int(math.sqrt(len(table)))
    for i in range(x//dim*dim, (x//dim+1)*dim):
        for j in range(x%dim*dim, (x%dim+1)*dim):
            array.append(table[i][j])
    return array


def get_block2(table, i, j):
    array=[]
    dim = int(math.sqrt(len(table)))
    for x in range(i//dim*dim, (i//dim+1)*dim):
        for y in range(j//dim*dim, (j//dim+1)*dim):
            if x==i or y==j:
                continue
            array.append(table[x][y])
    return array


def get_block3(table, i, j):
    array=[]
    dim = int(math.sqrt(len(table)))
    for x in range(i//dim*dim, (i//dim+1)*dim):
        for y in range(j//dim*dim, (j//dim+1)*dim):
            array.append(table[x][y])
    del(array[i%dim*dim+j%dim])
    return array


def which_block(table, i, j):
    dim = int(math.sqrt(len(table)))
    return (i//dim*dim+j//dim)


def update_number(table, array, number, check=True):
    for elem in array:
        if not elem.solved:
            if number in elem.number:
                elem.number.remove(number)
                if len(elem.number)==1:
                    elem.solved=True
                    elem.number=elem.number[0]
                    if check:
                        if check_error(table, elem):
                            return 1
    return 0


def update_possibilities(number, table, i, j):
    row = get_row(table, i)
    column = get_column(table, j)
    block = get_block(table, which_block(table, i, j))
    update_number(row, number)
    update_number(column, number)
    update_number(block, number)


def update_possibilities2(number, table, i, j):
    array = get_row(table, i)
    array += get_column(table, j)
    array += get_block(table, which_block(table, i, j))
    array = list(set(array))
    update_number(array, number)


def update_possibilities3(number, table, i, j):
    array = get_row2(table, i, j)
    array += get_column2(table, i, j)
    array += get_block2(table, i, j)
    update_number(array, number)


def get_neighbours(table, i, j):
    array = get_row3(table, i, j)
    array += get_column3(table, i, j)
    array += get_block3(table, i, j)
    return array


def update_possibilities4(number, table, i, j, check=True):
    array = get_neighbours(table, i, j)
    return update_number(table, array, number, check)


def check_possibilities(table, check=True): # improve row, column and block calls
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j].solved and not table[i][j].checked:
                table[i][j].checked = True
                array=[]
                number = table[i][j].number
                if update_possibilities4(number, table, i, j, check):
                    return 1
    return 0


def get_easiest(table):
    size = len(table)
    possibilities = []
    for row in table:
        for elem in row:
            if not elem.solved:
                if len(elem.number)<size:
                    size = len(elem.number)
    for row in table:
        for elem in row:
            if not elem.solved:
                if len(elem.number)==size:
                    possibilities.append(elem)
    return random.choice(possibilities)


def make_assumption(tables):
    table = copy.deepcopy(tables[-1].table)
    pick = get_easiest(table)
    pick.number = random.choice(pick.number)
    pick.solved = True
    tables.append(Hypotesis(pick, table))
    return tables


def wrong_assumption(tables):
    last = tables.pop()
    if len(tables)>0:
        assumption = last.assumption
        tables[-1].table[assumption.i][assumption.j].number.remove(assumption.number)
        if len(tables[-1].table[assumption.i][assumption.j].number)==0:
            return 1
    return 0


def print_numbers(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(i, j, table[i][j].number)


def print_table(table):
    dim = int(math.sqrt(len(table)))
    print('')
    for i in range(len(table)):
        if i!=0 and i%dim==0:
            print(('--'*dim + '+-')*(dim-1)+('--'*dim))
        for j in range(len(table[i])):
            if j!=0 and j%dim==0:
                print('| ', end='')
            print(table[i][j].number, end=' ')
        print('')
    print('')


def check_solved(table):
    return all(all(elem.solved==True for elem in array)==True for array in table)


def check_progress(table):
    count = 0
    for i in range(len(table)):
        for j in range(len(table[i])):
            if not table[i][j].solved:
                count += len(table[i][j].number)
    return count


def check_error(table, entry):
    array = get_neighbours(table, entry.i, entry.j)
    if entry.number in [elem.number for elem in array]:
        #print("Error in sudoku. Entry: i=%d j=%d number=%d" %(entry.i, entry.j, entry.number))
        return 1
    return 0


def check_solution(table):
    for row in table:
        for elem in row:
            if check_error(table, elem):
                print("Sudoku solution is incorrect.")
                return
    print("Sudoku solution is correct.")


def add_solution(all_solutions, solutions, tables):
    solutions.append(tables[-1].table)
    print(len(solutions))
    check_solution(solutions[-1])
    print_table(solutions[-1])
    if all_solutions:
        while(wrong_assumption(tables)):
            pass
    else:
        tables = []
    return solutions, tables


def main(argv):
    tic = time.process_time()
    if len(argv)==2:
        filename = argv[1]
    else:
        filename = "example1.txt"
    print("File: %s" %filename)
    all_solutions = False
    matrix, table = import_sudoku(filename)
    tables = [Hypotesis(None, table)]
    solutions = []
    check = False       # When true, it checks if the table is possible. Useful when table has no solution and after assumption it is left with impossible number
    while len(tables):
        progress = 1
        while progress:
            previous_progress = 0
            while progress!=previous_progress and progress:
                if check_possibilities(tables[-1].table, check):
                    while(wrong_assumption(tables)):
                        pass
                    break
                previous_progress = progress
                progress = check_progress(tables[-1].table)
                #print_numbers(tables[-1].table)
                #print("Missing: %d" %progress)
                #input()
            if len(tables)==0:
                break
            if progress:
                tables = make_assumption(tables)
                check = True
            else:
                solutions, tables = add_solution(all_solutions, solutions, tables)

    toc = time.process_time()
    print("Elapsed time: %f seconds" %(toc-tic))

main(sys.argv)
