import logging
from random import sample
from breezypythongui import EasyFrame

logging.basicConfig(level=logging.INFO)


class GameBoard(EasyFrame):
    def __init__(self, width, height):
        EasyFrame.__init__(self, title='Connect 4!', width=width, height=height,
                           background='red')

        canvas = self.addCanvas(width=width-5, height=height-5, background='blue')
        self.__canvas = canvas

        self.__on_click = None

        self.__cells = [list([None] * 6) for _ in range(7)]

        def create_click(c, r):
            """Create click handler for cell.
            """
            def click(_):
                self.__on_click(c, r)

            return click

        diam = 100
        for col in range(7):
            for row in range(6):
                fill = '#707080'
                x = 20 + col * diam
                y = 20 + row * diam

                # Give the impression of depth
                canvas.drawOval(x+2, y, x+diam-8, y+diam-8,
                                outline='black', fill='black')

                # This circle may become a coloured chip
                circle = canvas.drawOval(x, y, x+diam-10, y+diam-10,
                                         outline='black', fill=fill)
                canvas.itemconfig(circle, tags=f'circle-{col}-{row}')
                canvas.tag_bind(f'circle-{col}-{row}', '<ButtonRelease-1>',
                                create_click(col, row))

                self.__cells[col][row] = circle

    def set_click_handler(self, handler):
        """
        Set the click handler. The click handler should accept two
        arguments: column and row.
        :param handler: Function that handles click events
        :return: None
        """
        self.__on_click = handler

    def update_cell(self, col, row, colour):
        """
        Update a cell at location (col, row) with a certain colour.
        :param col: column of cell to update
        :param row: row of cell to update
        :param colour: colour to set in selected cell
        :return: None
        """
        cell = self.__cells[col][row]
        self.__canvas.itemconfig(cell, fill=colour)

    def __on_click(self, col, row):
        """
        Click event occurred. Calls the click handler is available.
        :param col: column of cell that received mouse click
        :param row: row of cell that received mouse click
        :return: None
        """
        logging.info(f'Click event at col={col},row={row}')

        if self.__on_click is not None:
            self.__on_click(col, row)


if __name__ == '__main__':
    game = GameBoard(730, 630)
    game.mainloop()
