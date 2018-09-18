buffer = []

def clear():
    global buffer
    buffer = []

def output_buffer():
    for l in buffer:
        line = ""
        for c in l:
            if type(c) == int:
                c = lineChars[c]
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
    expand_buffer(x2 + 1, y2 + 1)

    for x in range(x1 + 1, x2):
        _add_line_part(x, y1, left | right)
        _add_line_part(x, y2, left | right)

    for y in range(y1 + 1, y2):
        _add_line_part(x1, y, up | down)
        _add_line_part(x2, y, up | down)

    _add_line_part(x1, y1, right | down)
    _add_line_part(x2, y1, left  | down)
    _add_line_part(x1, y2, right | up)
    _add_line_part(x2, y2, left  | up)

def draw_h_line(x1, x2, y, includeEdges = True):
    expand_buffer(x2 + 1, y + 1)

    if includeEdges:
        _add_line_part(x1, y, left | right)
        _add_line_part(x2, y, left | right)
    else:
        _add_line_part(x1, y, right)
        _add_line_part(x2, y, left)

    for x in range(x1 + 1, x2):
        _add_line_part(x, y, left | right)

def draw_v_line(x, y1, y2, includeEdges = True):
    expand_buffer(x + 1, y2 + 1)

    if includeEdges:
        _add_line_part(x, y1, up | down)
        _add_line_part(x, y2, up | down)
    else:
        _add_line_part(x, y1, down)
        _add_line_part(x, y2, up)

    for y in range(y1 + 1, y2):
        _add_line_part(x, y, up | down)

def draw_string(x, y, string, w = None, h = None, line_wrap = False):
    if w or h:
        expand_buffer(w or 0, h or 0)

    w = w or len(buffer)
    h = h or (buffer and len(buffer) or 0)

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
                buffer[y][x] = c
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

def expand_buffer(new_w, new_h):
    w = len(buffer[0]) if buffer else 0
    h = len(buffer)

    if w < new_w:
        for row in range(len(buffer)):
            buffer[row] += [None for _ in range(new_w - w)]

    if h < new_h:
        for _ in range(new_h - h):
            buffer.append([None for _ in range(new_w)])

def _add_line_part(x, y, part):
    if (type(buffer[y][x]) != int):
        buffer[y][x] = 0
    buffer[y][x] |= part

left  = 0b0001
right = 0b0010
up    = 0b0100
down  = 0b1000

lineChars = [None for _ in range(16)]

lineChars[left | right] = "─"
lineChars[left | up]    = "┘"
lineChars[left | down]  = "┐"
lineChars[right | up]   = "└"
lineChars[right | down] = "┌"
lineChars[up | down]    = "│"
lineChars[left | right | up]   = "┴"
lineChars[left | right | down] = "┬"
lineChars[left | up | down]    = "┤"
lineChars[right | up | down]   = "├"
lineChars[left | right | up | down] = "┼"

