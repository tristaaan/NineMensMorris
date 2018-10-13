"""
An interface for positional printing and box-drawing in the console.

This interface has an internal buffer that can be drawed to using the ``draw_*`` functions,
the buffer can then be printed to the console using ``output_buffer``. The buffer can also be cleared
using the ``clear`` function.
"""


# The drawing buffer is represented as a two-dimensional array.
# Each cell can contain
# - None meaning the cell is empty and will be drawn as a single space
# - a string (single character) which will be drawn at that position
# - a int where the bits represent which segments to draw
#       the bits are ordered DURL (D = down, U = up, R = right, L = left)
#
#   U
#   U
# LL#RR
#   D
#   D
_buffer = []

def clear():
    """
    Clears the draw buffer.
    """

    global _buffer
    _buffer = []

def output_buffer():
    """
    Prints the draw buffer to the console.
    """

    for l in _buffer:
        line = ""
        for cell in l:
            if type(cell) == int: # cell contains a line or box-edge
                lineChar = _lineChars[cell]
                if lineChar:
                    line += lineChar
                else:
                    # The line part isn't drawable
                    # this should only occur when is contains the edge of a line
                    line += " "
            elif type(cell) == str: # cell contains a single character
                line += cell
            else: # cell is empty
                line += " "
        print(line)

def draw_box(x1, y1, x2, y2):
    """
    Draws a box into the draw buffer

    x1: the x-coordinate of the upper left corner of the box
    y1: the y-coordinate of the upper left corner of the box
    x2: the x-coordinate of the lower right corner of the box
    y2: the y-coordinate of the lower right corner of the box
    """

    _expand_buffer(x2 + 1, y2 + 1)

    for x in range(x1 + 1, x2):
        _add_line_part(x, y1, _left | _right)
        _add_line_part(x, y2, _left | _right)

    for y in range(y1 + 1, y2):
        _add_line_part(x1, y, _up | _down)
        _add_line_part(x2, y, _up | _down)

    _add_line_part(x1, y1, _right | _down)
    _add_line_part(x2, y1, _left  | _down)
    _add_line_part(x1, y2, _right | _up)
    _add_line_part(x2, y2, _left  | _up)

def draw_h_line(x1, x2, y, includeEdges = True):
    """
    Draws a horizontal line from (x1, y) to (x2, y) into the draw buffer.

    x1: the x-coordinate of the left edge of the line
    x2: the x-coordinate of the right edge of the line
    y:  the y-coordinate to draw the line at
    includeEdges: Wether or not to draw to the edge of the cells at the start and end of the line.
                  A false value means the function will only draw to the center of these cells.
    """

    _expand_buffer(x2 + 1, y + 1)

    if includeEdges:
        _add_line_part(x1, y, _left | _right)
        _add_line_part(x2, y, _left | _right)
    else:
        _add_line_part(x1, y, _right)
        _add_line_part(x2, y, _left)

    for x in range(x1 + 1, x2):
        _add_line_part(x, y, _left | _right)

def draw_v_line(x, y1, y2, includeEdges = True):
    """
    Draws a vertical line from (x, y1) to (x, y2) into the draw buffer.

    x:  the x-coordinate to draw the line at
    y1: the y-coordinate of the top edge of the line
    y2: the y-coordinate of the bottom edge of the line
    includeEdges: Wether or not to draw to the edge of the cells at the start and end of the line.
                  A false value means the function will only draw to the center of these cells.
    """

    _expand_buffer(x + 1, y2 + 1)

    if includeEdges:
        _add_line_part(x, y1, _up | _down)
        _add_line_part(x, y2, _up | _down)
    else:
        _add_line_part(x, y1, _down)
        _add_line_part(x, y2, _up)

    for y in range(y1 + 1, y2):
        _add_line_part(x, y, _up | _down)

def draw_string(x, y, string, w = None, h = None, line_wrap = False):
    """
    Draws a string of characters into the draw buffer.

    x:         the x-coordinate at which to draw the string
    y:         the y-coordinate at which to draw the string
    string:    the string to draw
    w:         the width of a bounding-box to keep the drawn string within
               this value may be None to specify that no bounding-box will be used
    h:         the height of a bounding-box to keep the drawn string within
               this value may be None to specify that no bounding-box will be used
    line_wrap: Wether or not to wrap the string back to the provided x-coordinate
               if a line in the string is too long to fit in the bounding box.
    """

    if w is None:
        max_width = max(map(len, string.split("\n")))
        w = max(x + max_width, _buffer and len(_buffer[0]) or 0)
    else:
        w = x + w

    if h is None:
        height = len(string.split("\n"))
        h = max(y + height, len(_buffer))
    else:
        h = y + h

    _expand_buffer(w, h)

    if x < w:
        start_x = x
        i = 0
        while i < len(string):
            char = string[i]
            i += 1
            if char == "\n":
                x = start_x
                y += 1
                if y >= h:
                    break
            elif char != "\r":
                _buffer[y][x] = char
                x += 1
                if x >= w:
                    if line_wrap:
                        x = start_x
                        y += 1
                    else:
                        x = start_x
                        y += 1
                        while i < len(string) and string[i] != "\n":
                            i += 1

                    if y >= h:
                        break

def draw_board(board):
    """
    Draws the provided board into the draw buffer.

    board: the board to draw
    """

    draw_box(1, 1, 33, 17)
    draw_box(7, 4, 27, 14)
    draw_box(13, 7, 21, 11)
    draw_h_line(1, 13, 9, includeEdges = False)
    draw_h_line(21, 33, 9, includeEdges = False)
    draw_v_line(17, 1, 7, includeEdges = False)
    draw_v_line(17, 11, 17, includeEdges = False)

    for i in range(1, 24 + 1):
        x = max(-1, min(1, 2 - abs(i % 8 - 4)))
        y = max(-1, min(1, abs((i + 2) % 8 - 4) - 2))
        d = [8, 5, 2][(i - 1) // 8]

        number_x = 17 + (2 * d + 1) * x
        number_y = 9 + (d + 1) * y
        if x < 0 and i >= 10:
            number_x -= 1
        if i >= 9 and i % 4 == 0:
            number_y -= 1
        draw_string(number_x, number_y, str(i))

        piece = board.get_piece(i)
        if piece:
            # Calculates the x & y coordinates by using
            # a triangle function with period 8 and amplitude 4
            x = max(-1, min(1, 2 - abs(i % 8 - 4)))
            y = max(-1, min(1, abs((i + 2) % 8 - 4) - 2))
            d = [8, 5, 2][(i - 1) // 8]

            icon_x = 17 + 2 * d * x
            icon_y = 9 + d * y
            draw_string(icon_x, icon_y, piece.icon.value)

def draw_tournament(tournament):
    bracket_height = 2
    bracket_x_start = 0
    bracket_y_start = 0

    for round in range(tournament.num_rounds + 1):
        round_names = [
            (
                "*** BYE ***" if round == 0 else " === "
            ) if player is None else player.name
            for player in tournament.rounds_players[round]
        ]

        longest_name_length = max([len(name) for name in round_names])

        line_x1 = bracket_x_start + longest_name_length
        line_x2 = bracket_x_start + longest_name_length + 4

        y = bracket_y_start
        even = True
        for name in round_names:
            draw_string(bracket_x_start, y, name)

            if len(round_names) > 1:
                draw_h_line(line_x1, line_x2, y, False)

                if even:
                    draw_v_line(line_x2, y, y + bracket_height, False)
                    draw_h_line(line_x2, line_x2 + 4, y + bracket_height // 2, False)

            y += bracket_height
            even = not even

        bracket_x_start += longest_name_length + 9
        bracket_y_start += + bracket_height // 2
        bracket_height *= 2

def _expand_buffer(new_w, new_h):
    w = len(_buffer[0]) if _buffer else 0
    h = len(_buffer)

    if w < new_w:
        for row in range(len(_buffer)):
            _buffer[row] += [None for _ in range(new_w - w)]
        w = new_w

    if h < new_h:
        for _ in range(new_h - h):
            _buffer.append([None for _ in range(w)])

def _add_line_part(x, y, part):
    if (type(_buffer[y][x]) != int):
        _buffer[y][x] = 0
    _buffer[y][x] |= part

_left  = 0b0001
_right = 0b0010
_up    = 0b0100
_down  = 0b1000

_lineChars = [None for _ in range(16)]

_lineChars[_left | _right] = "─"
_lineChars[_left | _up]    = "┘"
_lineChars[_left | _down]  = "┐"
_lineChars[_right | _up]   = "└"
_lineChars[_right | _down] = "┌"
_lineChars[_up | _down]    = "│"
_lineChars[_left | _right | _up]   = "┴"
_lineChars[_left | _right | _down] = "┬"
_lineChars[_left | _up | _down]    = "┤"
_lineChars[_right | _up | _down]   = "├"
_lineChars[_left | _right | _up | _down] = "┼"

