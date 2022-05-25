import os
import sys
import tty

file_location = sys.argv[1]
buffer = []
with open(file_location) as file:
    for line in file:
        line = buffer.append(list(line))

size = os.get_terminal_size()

#position of top left of screen relative to file
screen_line = 0
screen_column = 0

#position of the cursor RELATIVE to the screen
cursor_line = 0
cursor_column = 0

def print_screen():

    global screen_line, screen_column, cursor_line, cursor_column

    #print area of buffer visible on screen
    for line in buffer[screen_line: screen_line + size.lines]:
        
        print(
            ''.join(line[screen_column: screen_column + cursor_column]) + 
            '\x1b[7m' + ''.join(line[screen_column + cursor_column]) + '\x1b[27m' + 
            ''.join(line[screen_column + cursor_column + 1: screen_column + size.columns])
        )

#listen for arrow presses


tty.setcbreak(sys.stdin.fileno())
while True:
    #print(ord(sys.stdin.read(1)))
    input_char = sys.stdin.read(1)

    if ord(input_char) == 27 and ord(sys.stdin.read(1)) == 91:
        
        input_char = sys.stdin.read(1)

        #up arrow
        if ord(input_char) == 65:
            cursor_line = (cursor_line - 1) % size.lines
        #down arrow
        elif ord(input_char) == 66:
            cursor_line = (cursor_line + 1) % size.lines
        #right arrow
        elif ord(input_char) == 67:
            cursor_column = (cursor_column + 1) % size.columns
        #left arrow
        elif ord(input_char) == 68:
            cursor_column = (cursor_column - 1) % size.columns
    else:
        buffer[screen_line + cursor_line][screen_column + cursor_column] = input_char
        cursor_column += 1
    print_screen()