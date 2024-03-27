import pygame
import sys
import random

pygame.init() # pygame 모듈 초기화

img_neko = [ 
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"),
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png"),
]

def drop_neko(): # game 함수 while 이 한 번 돌때마다 
    ...          # 빈 공간(0)이 있을 시 위에 있는 네코가 밑으로 내려와야 됨
                 # 맨위에 있는 칸이 빈공간일 경우는 랜덤으로 생성시켜야 됨

def sweep_neko(): # 7이었던 리스트를 0으로 만들어서 빈공간으로 만들어줘야됨
    ...
    
def check_switch(): # 네코를 옮겼을 경우 조건 만족일 경우(옮겼는데 연속적일 때) return True
    ...             # 아닐 경우(옮겼는데 연속적이지 않을 경우) return False 
                    # False일 경우 switch_neko가 작동 안되게 해야됨
map_y = 10
map_x = 8
display_width = 912
display_height = 768
bg = pygame.image.load("neko_bg.png")
cursor = pygame.image.load("neko_cursor.png")

neko = [[] for _ in range(map_y)]
check = [[0 for _ in range(map_x)] for _ in range(map_y)]
search = [[0 for _ in range(8)] for _ in range(map_y)] #***

for y in range(map_y):
    for x in range(map_x):
        neko[y].append(random.choice(range(1,7)))


gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

class Mouse :
    def __init__(self,cursor,map_y,map_x):
        self.turn = 0
        self.cursor = cursor
        self.map_y = map_y
        self.map_x = map_x

    def get_mouse(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(map_y):
            for x in range(map_x):
                if x*72+20 < position[0] < (x+1)*72+20 and y*72+20 < position[1] < (y+1)*72+20 :
                    if self.turn == 0 :
                        gameDisplay.blit(self.cursor,(x*72+20,y*72+20))
                        if click[0] :
                            self.turn = 1
                            check[y][x] = 1
                    else :
                        if (0 <= y-1 and check[y-1][x] == 1) or (y+1 < self.map_y and check[y+1][x] == 1) \
                            or (self.map_x > x+1 and check[y][x+1] == 1) or (0 <= x-1 and check[y][x-1] == 1):
                            gameDisplay.blit(self.cursor,(x*72+20,y*72+20)) 
                            if click[0] :
                                self.turn = 0
                                switch_neko(y,x)
                                cursor_set()
                            elif click[2] :
                                cursor_set()
                                self.turn = 0

def switch_neko(y,x):
    global check, neko
    for i in range(10):
        for j in range(8):
            if check[i][j] == 1:
                neko[i][j], neko[y][x] = neko[y][x], neko[i][j]

def check_neko():
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7
    # 상화좌우 3 조건 맞추면 7로 바꿔주기 

def cursor_set():
    global check
    check = [[0 for _ in range(8)] for _ in range(10)]
    # 커서 초기화 시켜주기

def cursor_draw():
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x] == 1:
                gameDisplay.blit(cursor,(x*72+20, y*72+20))

def neko_draw():
    for y in range(map_y):
        for x in range(map_x):
            gameDisplay.blit(img_neko[neko[y][x]], (x*72+20, y*72+20))


def game(): # 메인 게임 함수
    
    tmr = 0 # 시간 관리 변수
    # 마우스 클래스 부르기
    m = Mouse(cursor,map_y,map_x)
    while True:
        tmr += 1 # 매 시간 1초 증가
        for event in pygame.event.get(): # 윈도운 X 누를 시 나오게끔
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg,(0,0))
        neko_draw()
        m.get_mouse()
        cursor_draw()
        check_neko()
        pygame.display.update()
        clock.tick(20)

        

game()