import logging
from breezypythongui import EasyCanvas, EasyFrame

logging.basicConfig(level=logging.INFO)


class DropRow(EasyCanvas):
    """
    This class create the "drop row" for the Connect 4 game.
    It should be at the top of the actual game board. The
    player can click on one of the circles to drop a chip in
    that column. The circle can be highlighted in the colour
    of the current player, e.g., 'yellow' or 'red', with the
    method {set_active_colour}.

    If a click handler is provided, it will be called from the
    internal on_click handler with the column as the sole
    argument.

    The method {disable_column} can be used to completely
    disable an entire column. This is useful when that column
    is full (it has 6 chips). It will set the active colour
    to grey and will prevent any click events from being
    generated for that column.
    """
    COLUMNS = 7
    GREYISH = '#707080'

    def __init__(self, parent, width, height):
        EasyCanvas.__init__(self, parent, width=width, height=height, background='blue',
                            borderwidth=0, highlightthickness=0, cursor='sb_down_arrow')

        # Number of columns
        self.__n_columns = self.COLUMNS

        # This list will hold the cells
        self.__cells = [None] * self.__n_columns

        # The set of cells that are disabled (full columns)
        self.__disabled_cells = set()

        # Placeholder for the click handler
        self.__click_handler = None

        # Create the separate cells
        self.__create_cells()

    def __create_cells(self):
        """Create the cells (visually), register any click
        handler, and store the references to the cells in
        the __cells attribute.
        """
        diam = 80
        offs = 15
        y = offs
        for col in range(self.__n_columns):
            x = offs + col * diam

            # Give the impression of depth
            self.drawOval(x + 2, y, x + diam - 8, y + diam - 8,
                          outline='black', fill='black')

            # This circle may become a coloured chip
            circle = self.drawOval(x, y, x + diam - 10, y + diam - 10,
                                   outline='black', fill=self.GREYISH,
                                   activefill='yellow')
            tag = f'dr-circle-{col}'
            self.tag_bind(tag, '<ButtonRelease-1>', lambda _, c=col: self.__on_click(c))
            self.itemconfig(circle, tags=tag)
            self.__cells[col] = circle

    def disable_column(self, column=None):
        """
        Disable a column. This will set the highlight colour of the
        cell to None. It will also prevent click events from being
        generated any further.
        :param column: Column to change colour for (default=all)
        """
        if column is not None:
            self.__disable_single_column(column)
        else:
            for column in range(self.__n_columns):
                self.__disable_single_column(column)

    def __disable_single_column(self, column):
        """
        Convenience method to disable a single column.
        :param column: Column to disable.
        """
        self.__disabled_cells.add(column)

        # Remove the activefill for this column
        self.itemconfigure(self.__cells[column], activefill=self.GREYISH)

    def __configure_cell(self, colour, column):
        """
        Configure a cell, but only if it is not disabled.
        :param colour: Colour for activefill parameter
        :param column: Column to update
        """
        if column not in self.__disabled_cells:
            cell = self.__cells[column]
            self.itemconfigure(cell, activefill=colour)

    def set_active_colour(self, colour=GREYISH, column=None):
        """
        Change the active {colour} for the cell indicated by the
        parameter {column}. It applies to all columns if that
        parameter is set to None.
        :param colour: Colour with which to highlight the cell
        :param column: Column to change (if None, apply to all)
        """
        if not column:
            # Update all columns
            for col in range(self.__n_columns):
                self.__configure_cell(colour, col)
        else:
            # Update only column addressed with argument {column}
            self.__configure_cell(colour, column)

    def set_click_handler(self, handler):
        """
        Set the click handler. The click handler should accept one
        argument: column.
        :param handler: Function that handles click events
        """
        self.__click_handler = handler

    def reset(self):
        pass

    def __on_click(self, column):
        """
        Private function that is called when a mouse click event
        is registered in a certain {column}. If the cell is not
        disabled and a click handler has been registered, the
        click handler will be called with the column as the only
        argument.
        :param column: Column in which the click event happened
        """
        if column in self.__disabled_cells:
            logging.info(f'Click event at col={column} ignored')
        else:
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
