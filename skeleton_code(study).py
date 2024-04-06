import pygame
import sys
import random



pygame.init()
BLACK= (0,0,0)
map_y = 10
map_x = 8
display_width = 912
display_height = 768
bg = pygame.image.load("./img/neko_ranking_bg.png")
font_1 = pygame.font.SysFont("malgungothic",53)
gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

txt = [font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    font_1.render(f"최봉준 : 1000 point", True, BLACK),
    ]

def game(): # 메인 게임 함수
    
    while True:
        for event in pygame.event.get(): # 윈도운 X 누를 시 나오게끔
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg,(0,0))
        for i in range(len(txt)):
            gameDisplay.blit(txt[i],(283,220+100*i))
            if i == 4 :
                break
        pygame.display.update()
        clock.tick(15)

        

game()