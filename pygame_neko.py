import pygame
import sys
import random

cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0

neko = []
check = []

img_neko = [
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"), 
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png")
]

bg = pygame.image.load("neko_bg.png")
cursor =pygame.image.load("neko_cursor.png")

for i in range(10):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0])
    check.append([0, 0, 0, 0, 0, 0, 0, 0])
    
def draw_neko():
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                screen.blit(img_neko[neko[y][x]],[x*72+60, y*72+60], tag="NEKO")

def check_neko():
    for y in range(10):
        for x in range(8):
            check[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7

    for y in range(10):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7

    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    neko[y-1][x-1] = 7
                    neko[y][x] = 7
                    neko[y+1][x+1] = 7
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    neko[y+1][x-1] = 7
                    neko[y][x] = 7
                    neko[y-1][x+1] = 7

def main():
    global cursor_x, cursor_y
    pygame.init()
    pygame.display.set_caption("고양이 터뜨리기")
    screen = pygame.display.set_mode((912,768))
    clock = pygame.time.Clock()
    tmr = 0
    while True :
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if 660 <= pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 840 and 100 <= pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] < 160 and event.type == pygame.MOUSEBUTTONDOWN :
                check_neko()
            if 24 <= pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 24+72*8 and 24 <= pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] < 24+72*10 :
                cursor_x = int((pygame.mouse.get_pos()[0]-24)/72)
                cursor_y = int((pygame.mouse.get_pos()[1]-24)/72)
                if event.type == pygame.MOUSEBUTTONDOWN :
                    neko[cursor_y][cursor_x] = random.randint(1, 2)
        screen.
        screen.blit(cursor,[cursor_x*72+60, cursor_y*72+60], tag="CURSOR")
        screen.blit(bg,(0,0))
        draw_neko()
        pygame.display.update()
        clock.tick(5)
    
if __name__ == '__main__':
    main()