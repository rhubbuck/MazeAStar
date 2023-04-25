import pygame
import math
from tkinter import *
from tkinter import messagebox

screen = pygame.display.set_mode((600, 600))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)

cols = 25
grid = [0 for i in range(cols)]
row = 25
avail_blocks = []
taken_blocks = []
w = 600 / cols
h = 600 / row


class Node:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def add_neighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols - 1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row - 1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])


def heur_function(n, e):
    distance = math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)
    return distance


def handle_mouse_click(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // cols)
    g2 = w // (600 // row)
    access = grid[g1][g2]
    if access != start and access != end:
        if not access.obs:
            access.obs = True
            access.show((255, 255, 255), 0)


def handle_submit():
    global start
    global end
    start = startBox.get().split(',')
    end = endBox.get().split(',')
    start = grid[int(start[0])][int(start[1])]
    end = grid[int(end[0])][int(end[1])]
    window.quit()
    window.destroy()


# create 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Create Spots
for i in range(cols):
    for j in range(row):
        grid[i][j] = Node(i, j)

# Set start and end node
start = grid[22][22]
end = grid[2][2]

# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j].show((255, 255, 255), 1)

for i in range(0, row):
    grid[0][i].show(GREY, 0)
    grid[0][i].obs = True
    grid[cols - 1][i].obs = True
    grid[cols - 1][i].show(GREY, 0)
    grid[i][row - 1].show(GREY, 0)
    grid[i][0].show(GREY, 0)
    grid[i][0].obs = True
    grid[i][row - 1].obs = True

window = Tk()
label = Label(window, text='Start(x,y) min 1,1: ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y) max 23,23: ')
endBox = Entry(window)
description = Label(window, text='Next, draw walls with mouse and Space to run')
submit = Button(window, text='Run', command=handle_submit)

submit.grid(columnspan=2, row=2)
description.grid(row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
avail_blocks.append(start)

end.show(RED, 0)
start.show(RED, 0)

info_loop = True
while info_loop:
    event = pygame.event.get()

    for e in event:
        if e.type == pygame.QUIT:
            info_loop = False
            break

        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                handle_mouse_click(pos)
            except AttributeError:
                pass
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                info_loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].add_neighbors(grid)


def main():
    global current
    start.show(RED, 0)
    end.show(RED, 0)
    if len(avail_blocks) > 0:
        lowest_index = 0
        for i in range(len(avail_blocks)):
            if avail_blocks[i].f < avail_blocks[lowest_index].f:
                lowest_index = i

        current = avail_blocks[lowest_index]
        if current == end:
            print('Done', current.f)
            start.show(RED, 0)
            total_blocks = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show(GREEN, 0)
                current = current.previous
            end.show(RED, 0)

            Tk().wm_withdraw()
            messagebox.showinfo('Program Finished', (
                f"The program finished, the shortest distance \n to the path is {int(total_blocks)} blocks away. "
                f"\n Thank you for playing."))
            pygame.quit()

        avail_blocks.pop(lowest_index)
        taken_blocks.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in taken_blocks:
                node_value = current.g + current.value
                if neighbor in avail_blocks:
                    if neighbor.g > node_value:
                        neighbor.g = node_value
                else:
                    neighbor.g = node_value
                    avail_blocks.append(neighbor)

            neighbor.h = heur_function(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous is None:
                neighbor.previous = current
    current.closed = True


if __name__ == '__main__':
    while True:
        main()
