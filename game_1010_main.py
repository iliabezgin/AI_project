import time
from tkinter import *
from agents import Agent
from action import Action
from game_state import Game


class Main:
    def __init__(self, agent: Agent, sleep_between_actions=True):

        self.sleep_between_actions = sleep_between_actions
        self.agent = agent

        self.window = Tk()
        self.window.title("1010")
        self.window.geometry("600x750")
        self.window.configure(background='#474747')
        self.window.resizable(False, False)

        self.last_x = None
        self.last_y = None
        self.last_preview = []

        self.points_label = Label(self.window, font=("Segoe UI Light", 24), bg="#474747", fg="lightgray")
        self.points_label["text"] = "0"
        self.points_label.place(x=(300 - self.points_label.winfo_width() / 2), y=10)

        self.canvas = Canvas(self.window, width=500, height=500, bg="lightgray", highlightthickness=0)

        self.canvas.place(x=50, y=75)

        self.lose_img = PhotoImage(file='resources/LoseScreen.png')
        self.img = PhotoImage(file='resources/DragAndDropOverlay.gif')
        self.bc_overlay = PhotoImage(file='resources/BlockCanvasOverlay.gif')

        self.block_canvas = Canvas(self.window, width=500, height=125, bg="lightgray", highlightthickness=0)
        self.block_canvas.place(x=50, y=525 + 50 + 25)

        self.block_canvas.create_image(0, 0, image=self.bc_overlay, anchor="nw")
        self.img_id = self.canvas.create_image(0, 0, image=self.img, anchor="nw")

        self.game = Game(self)
        self.game.generate_blocks()
        # GUILoseScreen(self.window, self.game, self.lose_img)
        if agent.get_type() == "HumanAgent":
            self.canvas.bind("<Button-1>", self.canvas_click)
            self.canvas.bind("<Motion>", self.render_preview)
            self.canvas.bind("<Leave>", self.remove_last_values)
        else:
            self.window.update()
            self._game_loop()

        self.render_current_blocks()
        self.window.mainloop()

    def _game_loop(self):
        '''
        Main loop
        :return: final score
        '''
        while self.game.is_action_possible():
            if self.sleep_between_actions:
                time.sleep(1)
            #
            # a = Action(0, 0, self.game.current_blocks[0])
            # first = self.game.generate_successor(a)
            # second = self.game.generate_successor(a)
            # s = set()
            # s.add(str(first.board))
            # print(str(second.board) in s)
            action = self.agent.get_action(self.game)

            self.apply_action(action)
            #GUI
            self.render_current_blocks()
            self.window.update()

        GUILoseScreen(self.window, self.game, self.lose_img)
        print(self.game.points)
        return self.game.points

    def apply_action(self, action: Action):
        x = action.x
        y = action.y
        coordinates = action.block.coord_array
        if self.game.fits(x, y, coordinates):
            for index in range(0, len(coordinates)):
                self.draw_rect_on_coordinates(x + coordinates[index][0],
                                              y + coordinates[index][1])
                self.game.set_filed(x + coordinates[index][0],
                                    y + coordinates[index][1], 1)
            self.selected_block = None
            for block in self.game.current_blocks:
                if block.block_list_index == action.block.block_list_index:
                    self.game.current_blocks.remove(block)
                    break
            action.block.destroy()
            if len(self.game.current_blocks) == 0:
                self.game.generate_blocks()

        lines = self.game.check_lines()
        columns = self.game.check_columns()

        if len(lines) > 0:
            for line in lines:
                self.game.clear_line(line)
                for i in range(0, 10):
                    self.clear_rect_on_coordinates(i, line)

        if len(columns) > 0:
            for column in columns:
                self.game.clear_column(column)
                for i in range(0, 10):
                    self.clear_rect_on_coordinates(column, i)

    def canvas_click(self, event):
        x = int(event.x / 50)
        y = int(event.y / 50)
        if (x < 10) and (y < 10):
            if self.game.selected_block is not None:

                coordinates = self.game.selected_block.coord_array
                if self.game.fits(x, y, coordinates):
                    self.place(x, y, coordinates)
                    block = self.game.selected_block
                    block.destroy()
                    self.game.selected_block = None
                    self.game.current_blocks.remove(block)
                    if len(self.game.current_blocks) == 0:
                        self.game.generate_blocks()
                        self.render_current_blocks()

                if len(self.game.check_lines()) > 0:
                    for lines in self.game.check_lines():
                        self.game.clear_line(lines)
                        for i in range(0, 10):
                            self.clear_rect_on_coordinates(i, lines)

                if len(self.game.check_columns()) > 0:
                    for columns in self.game.check_columns():
                        self.game.clear_column(columns)
                        for i in range(0, 10):
                            self.clear_rect_on_coordinates(columns, i)

                if not self.game.is_action_possible():
                    GUILoseScreen(self.window, self.game, self.lose_img)

    def render_preview(self, event):
        x = int(event.x / 50)
        y = int(event.y / 50)
        if self.last_x != x or self.last_y != y:
            self.last_x = x
            self.last_y = y
            if self.game.selected_block is not None:
                if 0 <= x and 0 <= y and x < 10 and y < 10:
                    if self.game.fits(x, y,
                                      self.game.selected_block.coord_array):
                        for index in range(0, len(self.last_preview)):
                            lx = self.last_preview[index][0]
                            ly = self.last_preview[index][1]
                            if self.game.board[ly][lx] == 0:
                                self.draw_rect(self.last_preview[index][0],
                                               self.last_preview[index][1],
                                               "lightgray")
                        if self.game.selected_block is not None:
                            ca = self.game.selected_block.coord_array
                            self.last_preview = []
                            for index in range(0, len(ca)):
                                tx = x + ca[index][0]
                                ty = y + ca[index][1]
                                if tx < 10 and ty < 10:
                                    self.draw_rect(tx, ty, "yellow")
                                    self.last_preview.append(
                                        [x + ca[index][0], y + ca[index][1]])

    def place(self, x, y, coordinates):
        for index in range(0, len(coordinates)):
            self.draw_rect_on_coordinates(x + coordinates[index][0],
                                          y + coordinates[index][1])
            self.game.set_filed(x + coordinates[index][0],
                                y + coordinates[index][1], 1)

    def remove_last_values(self, event):
        self.last_x = None
        self.last_y = None
        for index in range(0, len(self.last_preview)):
            lx = self.last_preview[index][0]
            ly = self.last_preview[index][1]
            if self.game.board[ly][lx] == 0:
                self.draw_rect(self.last_preview[index][0],
                               self.last_preview[index][1], "lightgray")

    def draw_rect_on_coordinates(self, x, y):
        self.draw_rect(x, y, "orange")

    def clear_rect_on_coordinates(self, x, y):
        self.draw_rect(x, y, "lightgray")

    def draw_rect(self, x, y, color):
        x = x * 50
        y = y * 50
        self.canvas.create_rectangle(x, y, x + 50, y + 50, fill=color,
                                     outline="")
        self.restore_grid(self.img_id)

    def render_current_blocks(self):
        for index in range(0, len(self.game.current_blocks)):
            c = self.game.current_blocks[index].get_block_canvas()
            c.place(x=50 + 166 * (index + 1) - 83 - int(c["width"]) / 2,
                    y=75 + 500 + 25 + (62 - int(c["height"]) / 2))

    def restore_grid(self, img_id):
        self.img_id = self.canvas.create_image(0, 0, image=self.img,
                                               anchor="nw")
        self.canvas.delete(img_id)


class GUILoseScreen:
    def __init__(self, window, game, lose_img):
        canvas = Canvas(window, width=600, height=725, bg="#FFFFFF",
                        highlightthickness=0)
        canvas.create_image(120, 10, image=lose_img, anchor="nw")
        canvas.place(x=0, y=0)
        self.points_label = Label(canvas, font=("Segoe UI Light", 24),
                                  bg="#474747", fg="lightgray")
        self.points_label["text"] = f"Score: {str(game.points)}"
        self.points_label.place(
            x=(300 - self.points_label.winfo_width() / 2) - 50, y=10)

# main = Main()
