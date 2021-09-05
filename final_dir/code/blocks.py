from tkinter import *

class Block: # the block class for the 1010! game
    def __init__(self, block_list_index, blocks, gui, gui_for_blocks):
        self.block_list_index = block_list_index
        self.coord_array = blocks.block_list[block_list_index]
        self.height = 0
        self.width = 0
        self.width_neg = 0
        x_coords = [coord[0] for coord in self.coord_array]
        y_coords = [coord[1] for coord in self.coord_array]
        self.h = max(y_coords) - min(y_coords) + 1
        self.w = max(x_coords) - min(x_coords) + 1
        if gui_for_blocks:
            self.gui = gui
            self.window = gui.window
            self.set_measurement()
            self.canvas = self.__create_block_canvas()

    def set_measurement(self):
        width_pos = 0
        width_neg = 0
        height = 0
        for index in range(0, len(self.coord_array)):
            x1 = self.coord_array[index][0] * 25
            y1 = self.coord_array[index][1] * 25

            if x1 >= 0:
                if x1 + 25 > width_pos:
                    width_pos = x1 + 25
            elif x1 * -1 > width_neg:
                width_neg = (x1 * -1)

            if y1 + 25 > height:
                height = y1 + 25
        self.height = height
        self.width = width_pos + width_neg
        self.width_neg = width_neg

    def get_block_canvas(self):
        return self.canvas

    def __create_block_canvas(self):
        canvas = Canvas(self.window, width=self.width, height=self.height, bg="lightgray", highlightthickness=0)
        canvas.bind("<Button-1>", self.select_block)
        for index in range(0, len(self.coord_array)):
            x1 = self.coord_array[index][0] * 25
            y1 = self.coord_array[index][1] * 25
            canvas.create_rectangle(x1 + self.width_neg, y1, x1 + 25 + self.width_neg, y1 + 25, fill="orange",
                                    outline="")

        return canvas

    def select_block(self, event):
        selected_block = self.gui.game.selected_block
        if selected_block is not None and selected_block is not self:
            selected_block.remove_outline()
        self.gui.game.selected_block = self
        self.canvas["highlightthickness"] = 1

    def remove_outline(self):
        self.canvas["highlightthickness"] = 0

    def destroy(self):
        self.canvas.destroy()


class BLOCKS: # all possible blocks
    def __init__(self):

        self.probabilities = [6/42, 3/42, 3/42, 3/42, 3/42, 1/42, 1/42, 1/42, 1/42, 2/42, 2/42, 2/42, 2/42, 2/42, 2/42, 2/42, 2/42, 2/42, 2/42]

        self.block_list = [
            [[0, 0], [0, 1], [1, 0], [1, 1]],  # 1 1
                                               # 1 1

            # HORIZONTAL 2,3
            [[0, 0], [0, 1]],
            [[0, 0], [0, 1], [0, 2]],
            # VERTICAL 2,3
            [[0, 0], [1, 0]],
            [[0, 0], [1, 0], [2, 0]],

            # CORNER 5
            [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]],  # 1 1 1
            #     1
            #     1
            #
            [[2, 0], [2, 1], [2, 2], [1, 2], [0, 2]],  # 1
            #     1
            # 1 1 1
            #
            [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]],  # 1 1 1
            # 1
            # 1
            #
            [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],  # 1
            # 1
            # 1 1 1


            # HORIZONTAL
            [[0, 0], [0, 1], [0, 2], [0, 3]],
            [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],
            # VERTICAL
            [[0, 0], [1, 0], [2, 0], [3, 0]],
            [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],

            [[0, 0]],

            # CORNER 3
            [[0, 0], [0, 1], [1, 0]], # 1 1
                                      # 1
                                      #
            [[0, 0], [0, 1], [1, 1]], # 1 1
                                      #   1
                                      #
            [[0, 0], [1, 0], [1, 1]], # 1
                                      # 1 1
                                      #
            [[1, 0], [1, 1], [0, 1]], #   1
                                      # 1 1


            [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]],  # 1 1 1
                                                                                        # 1 1 1
                                                                                        # 1 1 1
        ]