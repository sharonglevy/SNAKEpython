import random
import sys, pygame
pygame.init()
pygame.font.init()

s_width = 800
s_height = 600
play_width = 800
play_height = 600
block_size = 40

top_left_x = (s_width - play_width)//2
top_left_y = s_height - play_height

class cube(object):
    rows = 20
    w = 800
    def __init__(self, start, dirnx = 1, dirny = 0, color = (250, 155, 155)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dis = self.w // 20
        # current row
        i = self.pos[0]
        # current column
        j = self.pos[1]
        pygame.draw.rect(surface, self.color,(i* dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            # draw the eyes
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + dis - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        # These will represent the direction the snake moves
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # this will return the key that is being pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):  # Loop through every cube in our body
            p = c.pos[:]  # This stores the cubes position on the grid
            if p in self.turns:  # If the cubes current position is one where we turned
                turn = self.turns[p]  # Get the direction we should turn
                c.move(turn[0], turn[1])  # Move our cube in that direction
                if i == len(self.body) - 1:  # If this is the last cube in our body remove the turn from the dict
                    self.turns.pop(p)
            else:  # If we are not turning the cube
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)  # If we haven't reached the edge just move in our current direction

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # We then set the cubes direction to the direction of the snake.
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)

            else:
                c.draw(surface)

        pass

def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

    pass

def create_grid():
    locked_pos = {}
    grid = [[(0,0,0) for _ in range(40)] for _ in range(40)]

    for i in range(len(grid)):
        for j in range(len(grid)):
            if (j, i) in locked_pos:
                locked_pos = {}
    return grid

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def redrawWindow(surface, grid):
    global rows, width, snake, snack
    #fill the screen with black
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    # draw grid lines again
    draw_grid(surface, grid)
    pygame.display.update()


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsansms', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    draw_grid(surface, grid)

def main(win):
    rows = 15
    global snake, snack
    print("in main")
    locked_positions = {}
    grid = create_grid()
    snake = snake((155, 155, 155), (10, 10))
    snack = cube(randomSnack(rows, snake), color=(0, 255, 0))
    run = True

    while run:
        grid = create_grid()
        pygame.time.delay(150)
        pygame.display.update()
        draw_window(win, grid)
        pygame.display.update()
        snake.move()
        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = cube(randomSnack(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                # lose(windows)
                snake.reset((10, 10))
                break
        redrawWindow(win, grid)
        pygame.display.update()

def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('SNAKE')
# main_menu(win)
if __name__ == '__main__':
    main_menu(win)