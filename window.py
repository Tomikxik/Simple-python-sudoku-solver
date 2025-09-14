import tkinter as tk
import time
from solver_functions import solve,get_count,reset_count
                        # solve - main function on calculation sudoku - engine, get_count and reset_count are for calculating number of steps made

class Window(tk.Tk):                                #nastaveno okno pomoci tk.Tk
    def __init__(self,sudoku):                      
        super().__init__()                          #rika pythonu ze to tk.Tk je cast teto tridy
        self.inicializaceOkna()                     #menim parametry okna

        self.obsahOkna()

        self.sudoku = sudoku
        self.turbo = True
        self.edit_mode = False
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.mainloop()

    def inicializaceOkna(self):
        self.title("Sudoku solver :]")
        self.geometry("600x500+500+300")
        self.resizable(False, False)

    def obsahOkna(self):

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)


        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0,column=0,sticky="ns",padx=10,pady=10)

        self.button_import = tk.Button(self.left_frame,text="import",width=10, font=("Arial", 12),command=self.import_button)
        self.button_import.pack(pady=5)

        self.button_solve = tk.Button(self.left_frame,text="solve",width=10, font=("Arial", 12),command=self.solve_button)
        self.button_solve.pack(pady=5)

        self.label_step_count = tk.Label(self.left_frame,text="steps: 0",width=10,font=("Arial", 12))
        self.label_step_count.pack(pady=5)

        self.button_turbo = tk.Button(self.left_frame,bg="red",text="turbo",width=10, font=("Arial", 12),command=self.turbo_button)
        self.button_turbo.pack(pady=5)
        """self.label_restart = tk.Label(self.left_frame,text="OFF",width=10,font=("Arial", 12))
        self.label_restart.pack()"""

        self.button_reset = tk.Button(self.left_frame,text="reset",width=10, font=("Arial", 12),command=self.reset_button)
        self.button_reset.pack(pady=5)

        self.button_edit_mode = tk.Button(self.left_frame,text="edit",width=10, font=("Arial", 12),command=self.toggle_edit_mode)
        self.button_edit_mode.pack(pady=5)

        """self.entry_edit_value = tk.StringVar()
        self.entry_edit = tk.Entry(self.left_frame,textvariable=self.entry_edit_value)
        self.entry_edit.pack(padx=5,pady=5)"""

        self.button_exit = tk.Button(self.left_frame,text="exit",width=10, font=("Arial", 12),command=exit)
        self.button_exit.pack(pady=5)

        self.canvas = tk.Canvas(self,bg="white",width=470,height=470,highlightthickness=0)            # velikost hraciho pole je 470x470 - 20 je offset pro coz znamena ze jedno pole je 50x50
        self.canvas.grid(row=0,column=1,sticky="nw")

        self.cells()




        """self.canvas.pack(expand=True)"""                     #black magic

        


    def cells(self):
        self.canvas.delete("mrizka")                    #deletes all cells before(cleaning for safety :})
        
        size = 50

        self.canvas.create_line(0, 0, 450, 0, width=4, tags="mrizka")           #top            borders which doesnt wanted to work |
        self.canvas.create_line(0, 0, 0, 450, width=4, tags="mrizka")           #left                                               |
        self.canvas.create_line(450, 0, 450, 450, width=4, tags="mrizka")       #right                                              |
        self.canvas.create_line(0, 450, 450, 450, width=4, tags="mrizka")       #bottom                                             V
        
        for i in range(10):
            lines_width = 3 if i % 3 == 0 else 1            #zkracena verze - podminka ze pokud je i delitelne(celociselne) 3 lines_width = 3 jinak lines_width = 1

            """if i % 3 == 0:                               #delsi verze...
                lines_width = 3
            else:
                lines_width = 1"""

            self.canvas.create_line(i*size,0,i*size,450,width=lines_width,tags="mrizka")            #horizontal               <--- here
            self.canvas.create_line(0,i*size,450,i*size,width=lines_width,tags="mrizka")            #vertical



    def numbers_draw(self,highlight=None):
        self.canvas.delete("numbers")

        size = 50
        offset_x = size//2
        offset_y = size//2

        for row in range(9):
            for col in range(9):
                value = self.sudoku[row][col]

                if value != 0:                           # 0 = empty --- filtr
                    x = col*size + offset_x
                    y = row*size + offset_y                 #offset calc the coords of to make the number in middle(recalc position)
                    x0 = col * size + 1
                    y0 = row * size + 1
                    x1 = x0 + size - 2
                    y1 = y0 + size - 2

                    fill_color = "white"
                    if highlight == (row, col):
                        fill_color = "lightyellow"

                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="", tags="numbers")
                    self.canvas.create_text(x,y,text=str(value),fill="black",font=("Helvetica", 18),tags="numbers")

    def redraw(self,highlight=None):
        self.numbers_draw(highlight)
        self.cells()
        self.update_idletasks()


    def import_button(self):
        try:
            with open("sudoku.txt", "r", encoding="UTF-8") as f:
                lines = f.readlines()
                for i in range(9):
                    self.sudoku[i] = list(map(int, lines[i].strip().split()))
            self.redraw()
        except Exception as e:
            print(f"Import failed: {e}")

    def solve_button(self):                       #cant be easily transefered through files and edited and used at the same time if not wrapped in list
        print("Solve pressed")
        if self.edit_mode:
            print("Cannot solve in Edit Mode.")
            return
        def step_draw(row,column):
            if self.turbo:
                self.redraw((row,column))               #makes the animation
                time.sleep(0.02)
            self.label_step_count.config(text="steps: " + str(get_count()))
            self.update()

        result = solve(self.sudoku,step_draw)                 #returns [True/False,number]

        if result:                               #only first part of list - True or False
            print("Solved successfully")
        else:
            print("Solve doesnt exists")
        self.label_step_count.config(text="steps: " + str(get_count()))
        self.redraw()

    def turbo_button(self):
        if self.turbo:
            self.turbo = False
            """self.label_restart.config(text="ON")"""
            self.button_turbo.config(bg="green")
        else:
            self.turbo = True
            """self.label_restart.config(text="OFF")"""
            self.button_turbo.config(bg="red")

    def reset_button(self):
        self.canvas.delete("numbers")               #fixed - clears cells
        self.cells()
        reset_count()
        self.label_step_count.config(text="steps: " + str(get_count()))


    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            self.button_edit_mode.config(bg="orange")
            self.show_edit_entries()
        else:
            self.button_edit_mode.config(bg="SystemButtonFace")
            self.save_entries_to_sudoku()
            self.clear_entries()
            self.redraw()

    def show_edit_entries(self):
        size = 50
        for row in range(9):
            for col in range(9):
                x = col * size
                y = row * size
                entry = tk.Entry(self.canvas, width=2, font=("Helvetica", 18), justify="center")
                entry.place(x=x+15, y=y+10, width=30, height=30)            #matika pomoooooooc uz nechci :[

                value = self.sudoku[row][col]
                if value != 0:
                    entry.insert(0, str(value))
                self.entries[row][col] = entry

    def save_entries_to_sudoku(self):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                if entry:
                    value = entry.get()
                    try:
                        self.sudoku[row][col] = int(value) if value else 0
                    except ValueError:
                        self.sudoku[row][col] = 0

    def clear_entries(self):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                if entry:
                    entry.destroy()
                    self.entries[row][col] = None


"""     def sudoku_console_show(self):  #doesnt work now(bcs different type of saving(lines of 9 instead of 3))
        print("showing sudoku --->")

        for i in range(3):
            print(self.sudoku[0][i],"|",self.sudoku[1][i],"|",self.sudoku[2][i])

        print("---------------------------------------------")
        for i in range(3):
            print(self.sudoku[3][i],"|",self.sudoku[4][i],"|",self.sudoku[5][i])

        print("---------------------------------------------")
        for i in range(3):
            print(self.sudoku[6][i],"|",self.sudoku[7][i],"|",self.sudoku[8][i])"""



if __name__ == "__main__":
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]                                                       #na testing :]
    Window(sudoku)