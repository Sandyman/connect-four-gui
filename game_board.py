import logging
from breezypythongui import EasyCanvas, EasyFrame

logging.basicConfig(level=logging.INFO)


class GameBoard(EasyCanvas):
    """
    This class creates a GameBoard for the Connect4 game. It creates
    7 columns of each 6 cells. Each cell can be set to any colour
    using the method {update_cell}. If a cell is clicked, the click
    handler is called (if it is set).
    """
    def __init__(self, parent, width, height):
        EasyCanvas.__init__(self, parent, width=width, height=height, background='blue')

        # Placeholder for click handler
        self.__on_click = None

        # This 2D list will hold all cells
        self.__cells = [list([None] * 6) for _ in range(7)]

        diam = 100
        for col in range(7):
            for row in range(6):
                fill = '#707080'
                x = 20 + col * diam
                y = 20 + row * diam

                # Give the impression of depth
                self.drawOval(x+2, y, x+diam-8, y+diam-8,
                              outline='black', fill='black')

                # This circle may become a coloured chip
                circle = self.drawOval(x, y, x+diam-10, y+diam-10,
                                       outline='black', fill=fill)
                self.tag_bind(f'circle-{col}-{row}', '<ButtonRelease-1>',
                              lambda _, c=col, r=row: self.__on_click(c, r))
                self.itemconfig(circle, tags=f'circle-{col}-{row}')

                self.__cells[col][row] = circle

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
        self.itemconfig(cell, fill=colour)


def main():
    colours = ['red', 'yellow']
    current = 0

    f = EasyFrame()
    game = GameBoard(f, 730, 630)
    f.addCanvas(game)

    def handler(col, row):
        nonlocal current
        game.update_cell(col, row, colours[current])
        current = 1 - current

    game.set_click_handler(handler)
    f.mainloop()


if __name__ == '__main__':
    main()
