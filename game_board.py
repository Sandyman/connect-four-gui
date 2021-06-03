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
    DEFAULT_COLOUR = '#707080'

    def __init__(self, parent, width, height):
        EasyCanvas.__init__(self, parent, width=width, height=height, background='blue',
                            borderwidth=0, highlightthickness=0)

        # Placeholder for click handler
        self.__click_handler = None

        # This 2D list will hold all cells
        self.__cells = [list([None] * 6) for _ in range(7)]

        diam = 80
        offs = 15
        for col in range(7):
            for row in range(6):
                row = 5 - row
                fill = self.DEFAULT_COLOUR  # greyish
                x = offs + col * diam
                y = offs + row * diam

                # Give the impression of depth
                self.drawOval(x+2, y, x+diam-8, y+diam-8,
                              outline='black', fill='black')

                # This circle may become a coloured chip
                circle = self.drawOval(x, y, x+diam-10, y+diam-10,
                                       outline='black', fill=fill)
                self.__cells[col][row] = circle

                # Create tag for circle
                tag = f'gb-circle-{col}-{5 - row}'

                # Bind ButtonRelease event handler to tag
                self.tag_bind(tag, '<ButtonRelease-1>',
                              lambda _, c=col, r=row: self.__click_handler(c, r))

                # Assign tag to circle
                self.itemconfig(circle, tags=tag)

    def __on_click(self, col, row):
        """
        Click event occurred. Calls the click handler is available.
        :param col: column of cell that received mouse click
        :param row: row of cell that received mouse click
        """
        logging.info(f'Click event at col={col},row={row}')

        if self.__click_handler is not None:
            self.__click_handler(col, row)

    def set_click_handler(self, handler):
        """
        Set the click handler. The click handler should accept two
        arguments: column and row.
        :param handler: Function that handles click events
        """
        self.__click_handler = handler

    def update_cell(self, col, row, colour=DEFAULT_COLOUR):
        """
        Update a cell at location (col, row) with a certain colour.
        :param col: column of cell to update
        :param row: row of cell to update
        :param colour: colour to set in selected cell
        """
        cell = self.__cells[col][5 - row]
        self.itemconfig(cell, fill=colour)


def main():
    colours = ['red', 'yellow']
    current = 0

    f = EasyFrame()
    game = GameBoard(f, 590, 510)
    f.addCanvas(game)

    def handler(col, row):
        nonlocal current
        game.update_cell(col, row, colours[current])
        current = 1 - current

    game.set_click_handler(handler)
    f.mainloop()


if __name__ == '__main__':
    main()
