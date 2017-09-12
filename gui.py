from tkinter import *
from board import Board
from square import Square
from rank import Rank
import tkinter.messagebox as tkMessageBox
import time
import threading
from game_solver import *

class Gui:
    def __init__(self, master):
        """
        Initialize GUI, setup menu and board
        :param master: root of the GUI component
        """
        master.minsize(width=600, height=400)

        self.size = [30, 16, 99]
        self.board = Board(self.size)
        self.clocker = None
        self.count = False
        self.rank = Rank()

        self.left_mouse_pressed = False
        self.right_mouse_pressed = False

        self.define_images()
        self.tile_no = dict()
        for x in range(1, 9):
            self.tile_no[x] = PhotoImage(file="images/tile_" + str(x) + ".gif")

        self.frame = Frame(master)
        self.frame.pack()

        new_menu = Menubutton(self.frame, text='new/exit')
        new_menu.menu = Menu(new_menu)
        new_menu.menu.add_command(label='new', command=lambda: self.start())
        new_menu.menu.add_command(label='exit', command=lambda: self.exit())
        new_menu['menu'] = new_menu.menu
        new_menu.grid(row=0, column=0, columnspan=4)

        size_menu = Menubutton(self.frame, text='size')
        size_menu.menu = Menu(size_menu)
        size_menu.menu.add_command(label='small', command=lambda: self.change_to_small_size())
        size_menu.menu.add_command(label='medium', command=lambda: self.change_to_medium_size())
        size_menu.menu.add_command(label='large', command=lambda: self.change_to_large_size())
        size_menu['menu'] = size_menu.menu
        size_menu.grid(row=0, column=4, columnspan=4)

        self.create_labels()
        self.bind_buttons()

    def define_images(self):
        '''
        Define images
        '''
        self.sun_win = PhotoImage(file="images/img_sun_win.gif")
        self.sun_lose = PhotoImage(file="images/img_sun_lose.gif")
        self.sun_normal = PhotoImage(file="images/img_sun_normal.gif")
        self.tile_plain = PhotoImage(file="images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file="images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file="images/tile_mine.gif")
        self.tile_flag = PhotoImage(file="images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file="images/tile_wrong.gif")

    def create_labels(self):
        '''
        Create labels for clocker, remaining mines reminder, and ranking label
        '''
        self.clocker_label = Label(self.frame, text="")
        self.clocker_label.grid(row=0, column=10, columnspan=4)
        self.clocker_label.configure(text='time: ' + str(0))
        self.remaining_label = Label(self.frame, text="")
        self.remaining_label.grid(row=0, column=16, columnspan=5)
        self.remaining_label.configure(text='remaining: ' + str(self.board.remainings))
        self.sun_label = Label(self.frame, text="")
        self.sun_label.grid(row=0, column=8, columnspan=2)
        self.sun_label.config(image=self.sun_normal)
        self.rank_table = Label(self.frame, text="")
        self.rank_table.grid(row=25, column=8, columnspan=10)
        self.rank_table.configure(text=self.convert_rank_to_text())

    def convert_rank_to_text(self):
        '''
        Convert ranking info to text
        :return: text holding ranking info
        '''
        return '1st: ' + str(self.rank.first) + 's' + '\n' + '2st: ' + str(self.rank.second) + 's' + '\n' + \
               '3rd: ' + str(self.rank.third) + 's'

    def bind_buttons(self):
        '''
        Bind buttons with GUI, each button represents a square
        '''
        self.buttons = dict()

        for i in range(self.board.height):
            for j in range(self.board.width):
                self.buttons[str(i) + ',' + str(j)] = Button(self.frame, image=self.tile_plain)
                self.buttons[str(i) + ',' + str(j)].bind('<Button-1>', self.left_clicked_wrapper())
                self.buttons[str(i) + ',' + str(j)].bind('<Button-2>', self.right_clicked_wrapper())
                self.buttons[str(i) + ',' + str(j)].bind('<ButtonRelease-1>', self.release_wrapper([i, j]))
                self.buttons[str(i) + ',' + str(j)].bind('<ButtonRelease-2>', self.release_wrapper([i, j]))
                self.buttons[str(i) + ',' + str(j)].bind('<Double-1>', self.left_double_wrapper([i, j]))

        for key, values in self.buttons.items():
            row = self.board.height - int(key.split(',')[0])
            col = int(key.split(',')[1])
            self.buttons[key].grid(row=row, column=col)

    def press_any_of_two_mouses(self, btn):
        '''
        Define the event triggered by pressing any one of two mouses
        :param btn: button that was clicked
        '''
        if self.left_mouse_pressed and self.left_mouse_pressed <= time.time():
            self.left_mouse_pressed = False

        if self.right_mouse_pressed and self.right_mouse_pressed <= time.time():
            self.right_mouse_pressed = False

        if btn == 1:
            self.left_mouse_pressed = time.time() + 500
        if btn == 2:
            self.right_mouse_pressed = time.time() + 500

    def release_any_of_two_mouses(self, btn):
        '''
        Define the event triggered by releasing any one of two mouses
        :param btn: button that was still clicked
        '''
        if self.left_mouse_pressed and self.right_mouse_pressed:
            self.left_and_right_clicked(btn)
        elif self.left_mouse_pressed:
            self.left_clicked(btn)
        elif self.right_mouse_pressed:
            self.right_clicked(btn)

        self.left_mouse_pressed = False
        self.right_mouse_pressed = False

    def release_wrapper(self, btn):
        '''
        Return button that was still clicked
        :param btn:
        :return: button that was clicked
        '''
        return lambda Button: self.release_any_of_two_mouses(btn)

    def left_clicked_wrapper(self):
        '''
        Return button that was left clicked
        :param i: row of the button
        :param j: column of the button
        :return: button that was clicked
        '''
        return lambda Button: self.press_any_of_two_mouses(1)

    def right_clicked_wrapper(self):
        '''
        Return button that was right clicked
        :param i: row of the button
        :param j: column of the button
        :return: button that was clicked
        '''
        return lambda Button: self.press_any_of_two_mouses(2)

    def left_double_wrapper(self, btn):
        '''
        Return button that was left double clicked
        :param i: row of the button
        :param j: column of the button
        :return: button that was clicked
        '''
        return lambda Button: self.left_and_right_clicked(btn)

    def left_clicked(self, button_data):
        '''
        Define the event trigger by left click on a square
        :param button_data: button that was clicked
        '''
        if not self.count:
            self.update_clock(0)
            self.count = True
        row = button_data[0]
        col = button_data[1]
        self.board.update(Board.CLICK, row, col)
        self.update_gui()
        if self.board.detect_game_state() == Board.WIN:
            self.victory()
        elif self.board.detect_game_state() == Board.LOSE:
            self.game_over()

    def right_clicked(self, button_data):
        '''
        Define the event trigger by right click on a square
        :param button_data: button that was clicked
        '''
        row = button_data[0]
        col = button_data[1]
        self.board.update(Board.FLAG, row, col)
        self.update_gui()
        self.remaining_label.configure(text='remaining: ' + str(self.board.remainings))

    def left_and_right_clicked(self, button_data):
        '''
        Define the event trigger by left double click on a square
        :param button_data: button that was clicked
        '''
        row = button_data[0]
        col = button_data[1]
        self.board.update(Board.DOUBLE, row, col)
        self.update_gui()
        if self.board.detect_game_state() == Board.WIN:
            self.victory()
        elif self.board.detect_game_state() == Board.LOSE:
            self.game_over()

    def update_gui(self):
        '''
        Update GUI according to current board
        '''
        for i in range(self.board.height):
            for j in range(self.board.width):
                square_img = self.board.squares[i][j].display()
                self.update_square_gui(i, j, square_img)

    def update_final_gui(self):
        '''
        Update GUI once the game ended
        '''
        for i in range(self.board.height):
            for j in range(self.board.width):
                square_img = self.board.squares[i][j].final_display()
                if square_img == Square.WRONG:
                    self.buttons[str(i) + ',' + str(j)].config(image=self.tile_wrong)
                else:
                    self.update_square_gui(i, j, square_img)

    def update_square_gui(self, row, col, square_img):
        """
        Update square gui
        :param row: row
        :param col: column
        :param square_img: letters representing square image
        """
        if square_img == Square.BOMB:
            self.buttons[str(row) + ',' + str(col)].config(image=self.tile_mine)
        elif square_img == Square.FLAG:
            self.buttons[str(row) + ',' + str(col)].config(image=self.tile_flag)
        elif square_img == Square.CLEAR:
            self.buttons[str(row) + ',' + str(col)].config(image=self.tile_clicked)
        elif square_img == Square.BLANK:
            self.buttons[str(row) + ',' + str(col)].config(image=self.tile_plain)
        elif int(square_img) in self.tile_no:
            self.buttons[str(row) + ',' + str(col)].config(image=self.tile_no[int(square_img)])

    def game_over(self):
        '''
        Show lose message and restart game
        '''
        self.update_final_gui()
        self.sun_label.config(image=self.sun_lose)
        root.after_cancel(self.clocker)
        tkMessageBox.showinfo("Game Over", "You Lose!")
        self.start()


    def victory(self):
        '''
        Show win message and restart game
        '''
        self.update_final_gui()
        self.sun_label.config(image=self.sun_win)
        root.after_cancel(self.clocker)
        self.rank.update(self.clocker_label.cget('text'))
        tkMessageBox.showinfo("Game Over", "You Win!")
        self.start()

    def start(self):
        '''
        Start the game, destroy current GUI component and restart it
        '''
        self.board = Board(self.size)
        self.destroy_buttons()
        self.bind_buttons()
        self.remaining_label.configure(text='remaining: ' + str(self.board.remainings))
        self.sun_label.config(image=self.sun_normal)
        self.count = False
        self.clocker_label.configure(text='time: ' + str(0))
        self.rank_table.configure(text=self.convert_rank_to_text())

    def destroy_buttons(self):
        '''
        Destory all button components
        '''
        for key, value in self.buttons.items():
            value.destroy()

    def exit(self):
        '''
        Exit the game, destroy root of GUI
        '''
        global root
        root.destroy()

    def change_to_small_size(self):
        '''
        change the board size to small
        '''
        self.size = [8, 8, 10]
        self.start()

    def change_to_medium_size(self):
        '''
        change the board size to medium
        '''
        self.size = [16, 16, 40]
        self.start()

    def change_to_large_size(self):
        '''
        change the board size to large
        '''
        self.size = [30, 16, 99]
        self.start()

    def update_clock(self, count):
        '''
        update clock each second
        :param count: current time elapsed
        '''
        self.clocker_label.configure(text='time: ' + str(count))
        self.clocker = root.after(1000, self.update_clock, count + 1)


def auto_solve_game(board):
    '''
    Auto solve the game
    :param board: game board
    '''
    time.sleep(3)
    solve_game(board,auto=True)
    print('finished')

if __name__ == "__main__":
    global root
    root = Tk()
    root.title("Minesweeper")
    gui = Gui(root)
    gui.change_to_small_size()
    # create another thread auto solving the game
    t = threading.Thread(target=auto_solve_game, args=[gui.board])
    t.start()

    root.mainloop()
