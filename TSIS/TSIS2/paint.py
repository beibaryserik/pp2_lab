import pygame
import sys
from tools import *

pygame.init()

WIDTH, HEIGHT = 1100, 700
TOOLBAR_WIDTH = 1000
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (220,220,220)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((TOOLBAR_WIDTH, HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()

tool = "pencil"
color = BLACK
brush_size = 2

drawing = False
start_pos = None
prev_pos = None

font = pygame.font.SysFont(None, 24)
text_active = False
text_input = ""
text_pos = (0,0)

# ========= BUTTON =========
class Button:
    def __init__(self, x, y, w, h, text, value):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.value = value

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        txt = font.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x+5, self.rect.y+5))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ========= TOOL BUTTONS =========
buttons = [
    Button(1010,10,80,30,"Pencil","pencil"),
    Button(1010,50,80,30,"Line","line"),
    Button(1010,90,80,30,"Rect","rect"),
    Button(1010,130,80,30,"Circle","circle"),
    Button(1010,170,80,30,"Square","square"),
    Button(1010,210,80,30,"Tri R","rtriangle"),
    Button(1010,250,80,30,"Tri E","etriangle"),
    Button(1010,290,80,30,"Rhomb","rhombus"),
    Button(1010,330,80,30,"Fill","fill"),
    Button(1010,370,80,30,"Text","text"),
    Button(1010,410,80,30,"Eraser","eraser"),
]

size_buttons = [
    Button(1010,460,80,30,"S",2),
    Button(1010,500,80,30,"M",5),
    Button(1010,540,80,30,"L",10),
]

# ========= COLORS =========
colors = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0)]
color_buttons = []
for i,c in enumerate(colors):
    color_buttons.append((pygame.Rect(1010+(i%2)*40,580+(i//2)*40,30,30),c))


# ========= LOOP =========
while True:
    screen.fill((180,180,180))
    screen.blit(canvas,(0,0))

    for b in buttons:
        b.draw(screen)
    for b in size_buttons:
        b.draw(screen)

    for rect,c in color_buttons:
        pygame.draw.rect(screen,c,rect)
        pygame.draw.rect(screen,BLACK,rect,2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos

            for b in buttons:
                if b.clicked(event.pos):
                    tool = b.value

            for b in size_buttons:
                if b.clicked(event.pos):
                    brush_size = b.value

            for rect,c in color_buttons:
                if rect.collidepoint(event.pos):
                    color = c

            if x < TOOLBAR_WIDTH:
                if tool == "fill":
                    flood_fill(canvas,x,y,color)

                elif tool == "text":
                    text_active = True
                    text_pos = (x,y)
                    text_input = ""

                else:
                    drawing = True
                    start_pos = (x,y)
                    prev_pos = (x,y)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                draw_color = WHITE if tool=="eraser" else color

                if tool=="line":
                    draw_line(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="rect":
                    draw_rect(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="circle":
                    draw_circle(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="square":
                    draw_square(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="rtriangle":
                    draw_right_triangle(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="etriangle":
                    draw_equilateral_triangle(canvas,draw_color,start_pos,end_pos,brush_size)
                elif tool=="rhombus":
                    draw_rhombus(canvas,draw_color,start_pos,end_pos,brush_size)

                drawing=False

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool in ["pencil","eraser"]:
                draw_color = WHITE if tool=="eraser" else color
                pygame.draw.line(canvas,draw_color,prev_pos,event.pos,brush_size)
                prev_pos = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            if text_active:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input,True,color)
                    canvas.blit(txt,text_pos)
                    text_active=False
                elif event.key == pygame.K_ESCAPE:
                    text_active=False
                elif event.key == pygame.K_BACKSPACE:
                    text_input=text_input[:-1]
                else:
                    text_input+=event.unicode

    # preview
    if drawing and tool not in ["pencil","eraser","fill","text"]:
        mouse_pos = pygame.mouse.get_pos()
        draw_color = WHITE if tool=="eraser" else color

        if tool=="line":
            draw_line(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="rect":
            draw_rect(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="circle":
            draw_circle(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="square":
            draw_square(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="rtriangle":
            draw_right_triangle(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="etriangle":
            draw_equilateral_triangle(screen,draw_color,start_pos,mouse_pos,brush_size)
        elif tool=="rhombus":
            draw_rhombus(screen,draw_color,start_pos,mouse_pos,brush_size)

    if text_active:
        preview = font.render(text_input,True,color)
        screen.blit(preview,text_pos)

    pygame.display.flip()
    clock.tick(60)