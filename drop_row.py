import logging
from breezypythongui import EasyCanvas, EasyFrame

logging.basicConfig(level=logging.INFO)


class DropRow(EasyCanvas):
    """
    This class create the "drop row" for the Connect 4 game.
    It should be at the top of the actual game board. The
    player can click on one of the circles to drop a chip in
    that column. The circle can be highlighted in the colour
    of the current player, e.g., 'yellow' or 'red'.

    If a click handler is provided, it will be called from the
    internal on_click handler with the column as the sole
    argument.
    """
    def __init__(self, parent, width, height):
        EasyCanvas.__init__(self, parent, width=width, height=height, background='blue',
                            borderwidth=0, highlightthickness=0)

        # This list will hold the cells
        self.__cells = [None] * 7

        # Placeholder for the click handler
        self.__click_handler = None

        diam = 80
        offs = 15
        y = offs
        for col in range(7):
            fill = '#707080'  # greyish
            x = offs + col * diam

            # Give the impression of depth
            self.drawOval(x + 2, y, x + diam - 8, y + diam - 8,
                          outline='black', fill='black')

            # This circle may become a coloured chip
            circle = self.drawOval(x, y, x + diam - 10, y + diam - 10,
                                   outline='black', fill=fill, activefill='yellow')
            tag = f'dr-circle-{col}'
            self.tag_bind(tag, '<ButtonRelease-1>', lambda _, c=col: self.__on_click(c))
            self.itemconfig(circle, tags=tag)
            self.__cells[col] = circle

    def set_active_colour(self, colour):
        """
        Change the active colour for the cell.
        :param colour: Colour to highlight the cell with
        :return: None
        """
        for cell in self.__cells:
            self.itemconfigure(cell, activefill=colour)

    def set_click_handler(self, handler):
        """
        Set the click handler. The click handler should accept two
        arguments: column and row.
        :param handler: Function that handles click events
        :return: None
        """
        self.__click_handler = handler

    def __on_click(self, column):
        logging.info(f'Click event at col={column}')

        if self.__click_handler:
            self.__click_handler(column)


def main():
    f = EasyFrame()
    drow = DropRow(f, 590, 110)
    drow.set_active_colour('orange')
    f.addCanvas(drow)
    f.mainloop()


if __name__ == '__main__':
    main()
