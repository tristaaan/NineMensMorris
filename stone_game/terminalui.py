_buffer = []

def clear():
    global _buffer
    _buffer = []

def output_buffer():
    for l in _buffer:
        line = ""
        for c in l:
            if type(c) == int:
                c = _lineChars[c]
                if c:
                    line += c
                else:
                    line += " "
            elif type(c) == str:
                line += c
            else:
                line += " "
        print(line)

def draw_box(x1, y1, x2, y2):
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
    if w or h:
        _expand_buffer(w or 0, h or 0)

    w = w or len(_buffer)
    h = h or (_buffer and len(_buffer) or 0)

    if x < w:
        start_x = x
        i = 0
        while i < len(string):
            c = string[i]
            i += 1
            if c == "\n":
                x = start_x
                y += 1
                if y >= h:
                    break
            elif c != "\r":
                _buffer[y][x] = c
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
    draw_box(0, 0, 16, 16)
    draw_box(3, 3, 13, 13)
    draw_box(6, 6, 10, 10)
    draw_h_line(0, 6, 8, includeEdges = False)
    draw_h_line(10, 16, 8, includeEdges = False)
    draw_v_line(8, 0, 6, includeEdges = False)
    draw_v_line(8, 10, 16, includeEdges = False)

    for i in range(1, 24 + 1):
        piece = board.get_piece(i)
        if piece:
            x = max(-1, min(1, 2 - abs(i % 8 - 4)))
            y = max(-1, min(1, abs((i + 2) % 8 - 4) - 2))
            d = [8, 5, 2][(i - 1) // 8]

            draw_string(8 + d * x, 8 + d * y, piece.icon)

def _expand_buffer(new_w, new_h):
    w = len(_buffer[0]) if _buffer else 0
    h = len(_buffer)

    if w < new_w:
        for row in range(len(_buffer)):
            _buffer[row] += [None for _ in range(new_w - w)]

    if h < new_h:
        for _ in range(new_h - h):
            _buffer.append([None for _ in range(new_w)])

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

