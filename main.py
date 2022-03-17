import pygame
import math
from graph import Graph

BACKGROUND = (60, 80, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
GREEN = (30, 200, 30)
BLUE = (30, 30, 200)
YELLOW = (230, 230, 100)
WIDTH = 900
HEIGHT = 900
SHOW_LABELS = False


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.init()
pygame.font.init()

font = pygame.font.SysFont("Arial", 14)

running = True
selected_node = None
choice1 = None
choice2 = None

g = Graph.pattern(5, 846900323733667)

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def draw_bezier(window, start, control, target, color):
    lastpoint = None
    for s in range(101):
        t = s/100
        px = start[0] * (1 - t) ** 2 + 2 * (1 - t) * t * control[0] + target[0] * t ** 2
        py = start[1] * (1 - t) ** 2 + 2 * (1 - t) * t * control[1] + target[1] * t ** 2
        point = (px, py)
        if lastpoint is not None:
            pygame.draw.line(window, color, lastpoint, point, 3)
        lastpoint = point

def draw_arrow(window, start, control, target, color, radius):
    lastpoint = None
    point = None
    for s in range(101):
        t = s / 100
        px = start[0] * (1 - t) ** 2 + 2 * (1 - t) * t * control[0] + target[0] * t ** 2
        py = start[1] * (1 - t) ** 2 + 2 * (1 - t) * t * control[1] + target[1] * t ** 2
        point = (px, py)
        if lastpoint is not None:
            pygame.draw.line(window, color, lastpoint, point, 3)
        if (px-target[0])**2 + (py-target[1])**2 <= radius**2:
            break
        lastpoint = point
    # arrow tip
    if point == None or lastpoint == None:
        return
    ARROW_TIP_LENGTH = 15
    ARROW_TIP_WIDTH = 10
    v = (point[0]-lastpoint[0], point[1]-lastpoint[1]) # vector from second last to last
    l = math.sqrt(v[0]**2 + v[1]**2) # len of last line segment
    u = (v[0]/l, v[1]/l) # v scaled to unit length
    normal = (-u[1], u[0])
    v1 = (lastpoint[0]-ARROW_TIP_LENGTH*u[0]+ARROW_TIP_WIDTH*normal[0], lastpoint[1]-ARROW_TIP_LENGTH*u[1]+ARROW_TIP_WIDTH*normal[1])
    v2 = (lastpoint[0]-ARROW_TIP_LENGTH*u[0]-ARROW_TIP_WIDTH*normal[0], lastpoint[1]-ARROW_TIP_LENGTH*u[1]-ARROW_TIP_WIDTH*normal[1])
    pygame.draw.polygon(window, color, (lastpoint, v1, v2))

# mover = pygame.BUTTON_RIGHT
# selecter = pygame.BUTTON_LEFT
mover = pygame.BUTTON_LEFT
selecter = pygame.BUTTON_RIGHT
deleter = pygame.K_DELETE

while running:
    pygame.time.wait(10)
    window.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # drag nodes
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == mover:
                if selected_node is None:
                    for node in g.nodes:
                        if dist(event.pos, node.pos) < node.radius:
                            selected_node = node
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == mover:
                if selected_node is not None:
                    selected_node.pos = event.pos
                    selected_node = None
        if event.type == pygame.MOUSEMOTION:
            if selected_node is not None:
                selected_node.pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == selecter:
                for node in g.nodes:
                    if dist(event.pos, node.pos) < node.radius:
                        if choice1 == None:
                            choice1 = node
                        elif node == choice1:
                            choice1 = None
                        elif choice1 != choice2:
                            choice2 = node
                            g.add_product_node(choice1, choice2)
                            choice1 = None
                            choice2 = None
        if event.type == pygame.KEYDOWN:
            if event.key == deleter:
                if choice1 is not None:
                    g.remove_node(choice1)
                    choice1 = None

    for edge in g.red:
        node1 = edge[0]
        node2 = edge[1]
        if not node1 == node2:
            middle = ((node1.pos[0]+node2.pos[0]) / 2 + 30, (node1.pos[1]+node2.pos[1]) / 2 + 30)
            draw_arrow(window, node1.pos, middle, node2.pos, RED, node1.radius)

    for edge in g.green:
        node1 = edge[0]
        node2 = edge[1]
        if not node1 == node2: #selfloop
            middle = ((node1.pos[0] + node2.pos[0]) / 2 - 30, (node1.pos[1] + node2.pos[1]) / 2 - 30)
            draw_arrow(window, node1.pos, middle, node2.pos, GREEN, node1.radius)

    for node in g.nodes:
        pygame.draw.circle(window, BLACK, node.pos, node.radius)
        if node == choice1:
            pygame.draw.circle(window, WHITE, node.pos, node.radius-2)
        else:
            pygame.draw.circle(window, BLUE, node.pos, node.radius-2)
        if SHOW_LABELS:
            name = font.render(str(node.name), True, BLACK)
            pos = (node.pos[0] - name.get_rect().width / 2, node.pos[1] - name.get_rect().height / 2)
            window.blit(name, pos)#

    for edge in g.red:
        node1 = edge[0]
        node2 = edge[1]
        if node1 == node2: #selfloop
            x = node1.pos[0]
            y = node1.pos[1]
            pygame.draw.rect(window, RED, (x-10, y-10, 15, 15))
    for edge in g.green:
        node1 = edge[0]
        node2 = edge[1]
        if node1 == node2: #selfloop
            x = node1.pos[0]
            y = node1.pos[1]
            pygame.draw.rect(window, GREEN, (x-5, y-5, 15, 15))

    pygame.display.update()

