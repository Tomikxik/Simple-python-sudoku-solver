import time

 
step_count = 0


def get_count():
    return step_count

def reset_count():
    global step_count
    step_count = 0

def find_empty_cell(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i,j                                         #coords of empty cell/s
    return None                                                   #nothing found


def is_valid(sudoku,number,row,column):
    if number in sudoku[row]:                       #row check example:(number in [0,0,0,0,0])
        return False

    for i in range(9):                              #column check example:(takes [0,3,1,4,6,9] and tryes to detect it by name[i][j])
        if number == sudoku[i][column]:
            return False

    box_x = (column // 3) * 3                       #splits to boxes(3x3 in rows and columns) rows
    box_y = (row // 3) * 3                          #                                         columns
        
    for i in range(box_y, box_y + 3):                   
        for j in range(box_x, box_x + 3):
            if sudoku[i][j] == number:
                return False

    return True


def solve(sudoku,stepcallback=None):
    global step_count                                  #cant be easily transefered through files and edited and used at the same time if not wrapped in list
    find = find_empty_cell(sudoku)
    if not find:
        return True                                  #solved sudoku
    else:
        row,column = find           #find_empty_cells gives --- x,y meaning row column
            

    for number in range(1,10):
        if is_valid(sudoku,number,row,column):
            sudoku[row][column] = number
            step_count += 1
            print(f"Trying {number} at ({row}, {column}), step: {step_count}")

            if stepcallback:
                stepcallback(row,column)

            if solve(sudoku,stepcallback):
                return True

            sudoku[row][column] = 0
            step_count += 1
            print(f"Backtracking at ({row}, {column}), step: {step_count}")
            if stepcallback:
                stepcallback(row,column)
    return False