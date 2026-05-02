import pygame
import sys
import math

def main():
    pygame.init()
    # Размеры окна
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Advanced Paint: Кисть + Фигуры")
    clock = pygame.time.Clock()
    
    # Холст, на котором мы сохраняем рисунок
    canvas = pygame.Surface((W, H))
    canvas_color = (0, 0, 0) 
    canvas.fill(canvas_color)
    
    # Состояния
    radius = 5
    drawing = False
    erasing = False
    last_pos = None
    start_pos = None
    
    # Режимы: 'brush' (кисть), 'square', 'right_tr', 'equil_tr', 'rhombus'
    mode = 'brush'
    color_mode = 'blue'
    
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255)
    }

    while True:
        current_color = colors[color_mode]
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                # Выбор цвета
                if event.key == pygame.K_r: color_mode = 'red'
                elif event.key == pygame.K_g: color_mode = 'green'
                elif event.key == pygame.K_b: color_mode = 'blue'
                # Выбор режима (Кисть или Фигуры)
                elif event.key == pygame.K_0: mode = 'brush'
                elif event.key == pygame.K_1: mode = 'square'
                elif event.key == pygame.K_2: mode = 'right_tr'
                elif event.key == pygame.K_3: mode = 'equil_tr'
                elif event.key == pygame.K_4: mode = 'rhombus'
                # Очистка и выход
                elif event.key == pygame.K_c:
                    canvas.fill(canvas_color)
                elif event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # ЛКМ
                    drawing = True
                    start_pos = event.pos # Запоминаем где начали рисовать фигуру
                elif event.button == 3: # ПКМ - Ластик
                    erasing = True
                elif event.button == 4: # Скролл вверх
                    radius = min(50, radius + 1)
                elif event.button == 5: # Скролл вниз
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    # Если мы в режиме ФИГУР, рисуем финальную версию на canvas при отпускании кнопки
                    if mode != 'brush' and start_pos:
                        draw_shape(canvas, current_color, start_pos, event.pos, mode, radius)
                    
                    drawing = False
                    last_pos = None
                    start_pos = None
                elif event.button == 3:
                    erasing = False
                    last_pos = None

            if event.type == pygame.MOUSEMOTION:
                # СВОБОДНОЕ РИСОВАНИЕ (только в режиме кисти или ластика)
                if (drawing and mode == 'brush') or erasing:
                    color = canvas_color if erasing else current_color
                    if last_pos:
                        pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    else:
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    last_pos = event.pos

        # --- ОТРИСОВКА ---
        screen.fill((30, 30, 30)) # Серый фон окна
        screen.blit(canvas, (0, 0)) # Рисуем холст
        
        # ПРЕДПРОСМОТР фигуры (рисуем на основном экране, пока кнопка зажата)
        if drawing and mode != 'brush' and start_pos:
            draw_shape(screen, current_color, start_pos, mouse_pos, mode, radius)

        # Индикатор кисти вокруг курсора
        ind_color = (255, 255, 255) if erasing else current_color
        pygame.draw.circle(screen, ind_color, mouse_pos, radius, 1)
        
        # Подсказка по режимам
        display_info(screen, mode, color_mode, radius)

        pygame.display.flip()
        clock.tick(120)

def draw_shape(surface, color, start, end, shape_type, thickness):
    """Функция для расчета и рисования фигур"""
    x1, y1 = start
    x2, y2 = end
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    
    if shape_type == 'square':
        side = max(dx, dy)
        rect = pygame.Rect(min(x1, x2), min(y1, y2), side, side)
        pygame.draw.rect(surface, color, rect, thickness)
        
    elif shape_type == 'right_tr':
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, thickness)
        
    elif shape_type == 'equil_tr':
        # Равносторонний треугольник
        height = dx * math.sqrt(3) / 2
        top = (x1 + (x2 - x1)/2, y1)
        left = (x1, y1 + height)
        right = (x2, y1 + height)
        pygame.draw.polygon(surface, color, [top, left, right], thickness)
        
    elif shape_type == 'rhombus':
        # Ромб по границам прямоугольника выделения
        mid_top = (x1 + (x2 - x1)/2, y1)
        mid_bottom = (x1 + (x2 - x1)/2, y2)
        mid_left = (x1, y1 + (y2 - y1)/2)
        mid_right = (x2, y1 + (y2 - y1)/2)
        pygame.draw.polygon(surface, color, [mid_top, mid_right, mid_bottom, mid_left], thickness)

def display_info(screen, mode, color, radius):
    font = pygame.font.SysFont("Arial", 18)
    txt = f"Mode: {mode} | Color: {color} | Radius: {radius} (0-Brush, 1-Sq, 2-R_Tri, 3-E_Tri, 4-Rhomb)"
    img = font.render(txt, True, (200, 200, 200))
    screen.blit(img, (10, screen.get_height() - 25))

if __name__ == "__main__":
    main()