import pygame
import sys
import random

class GameControl() :
    def __init__(self) -> None:
        pygame.init() # pygame 모듈 초기화
        self.img_neko = [ #애니팡 
            None,
            pygame.image.load("neko1.png"),
            pygame.image.load("neko2.png"),
            pygame.image.load("neko3.png"),
            pygame.image.load("neko4.png"),
            pygame.image.load("neko5.png"), 
            pygame.image.load("neko6.png"),
            pygame.image.load("neko_niku.png")
        ]

        self.map_y = 10
        self.map_x = 8
        self.neko = [[] for _ in range(self.map_y)]
        self.check = [[0 for _ in range(self.map_x)] for _ in range(self.map_y)]
        self.search = [[0 for _ in range(self.map_x)] for _ in range(self.map_y)]
        for i in range(self.map_y):
            for j in range(self.map_x):
                self.neko[i].append(random.choice(range(1,7)))


        self.bg = pygame.image.load("neko_bg.png")
        self.cursor =pygame.image.load("neko_cursor.png")
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화

        display_width = 912
        display_height = 768
        self.gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
        pygame.display.set_caption("애니팡")  # 타이틀

    
    def _drop_neko(self) :
        for y in range(10):
            for x in range(8) :
                if y >= 1 :
                    if self.neko[y][x] == 0 :
                        self.neko[y][x] = self.neko[y-1][x]
                        self.neko[y-1][x] = 0
                if y == 0 :
                    if self.neko[y][x] == 0 :
                        self.neko[y][x] = random.choice(range(1,7))   

    def _check_neko(self, idx):
        for y in range(self.map_y):
            for x in range(self.map_x):
                self.search[y][x] = self.neko[y][x]

        for y in range(1, self.map_y-1):
            for x in range(self.map_x):
                if self.search[y][x] > 0:
                    if self.search[y-1][x] == self.search[y][x] and self.search[y+1][x] == self.search[y][x]:
                        self.neko[y-1][x] = 7
                        self.neko[y][x] = 7
                        self.neko[y+1][x] = 7
                        idx = 1

        for y in range(self.map_y):
            for x in range(1, self.map_x-1):
                if self.search[y][x] > 0:
                    if self.search[y][x-1] == self.search[y][x] and self.search[y][x+1] == self.search[y][x]:
                        self.neko[y][x-1] = 7
                        self.neko[y][x] = 7
                        self.neko[y][x+1] = 7
                        idx = 1
        return idx
    
                    
    def _sweep_neko(self):
        for y in range(self.map_y):
            for x in range(self.map_x):
                if self.neko[y][x] == 7:
                    self.neko[y][x] = 0
                    
    def _draw_neko(self):
        for y in range(self.map_y):
            for x in range(self.map_x):
                if self.neko[y][x] > 0:
                    self.gameDisplay.blit(self.img_neko[self.neko[y][x]], (x*72+20, y*72+20))
                    
    def _draw_cursor(self):
        for y in range(self.map_y):
            for x in range(self.map_x):
                if self.check[y][x] == 1 :
                    self.gameDisplay.blit(self.cursor, (x*72+20, y*72+20))          
                    
    def game_start(self):
        tmr = 0 # 시간 관리 변수
        m = Mouse(self.gameDisplay, self.cursor, self.neko, self.check, self.map_x, self.map_y, self.search)
        idx = 0
        while True:
            tmr += 1 # 매 시간 1초 증가
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.gameDisplay.blit(self.bg, (0,0))
            if idx == 0: # 딜레이 주면서 사진 보이기
                idx = self._check_neko(idx)
            elif 3 > idx >= 1 :
                idx += 1
            elif idx == 3 :
                self._sweep_neko()
                idx = 0
            m.get_move()
            self._draw_cursor()
            self._draw_neko()
            self._drop_neko()
            pygame.display.update() # 화면 업데이트
            self.clock.tick(13) #프레임 레이트 지정

        
        
        
class Mouse:
    def __init__(self, gameDisplay, cursor, neko, check, map_x, map_y, search):
        self.turn = 0
        self.map_y = map_y
        self.map_x = map_x
        self.gameDisplay = gameDisplay
        self.cursor = cursor
        self.neko = neko
        self.check = check
        self.search = search
        
    def get_move(self) :
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(self.map_y):
            for x in range(self.map_x):
                if x*72+20 < mouse[0] < (x+1)*72+20 and y*72+20 < mouse[1] < (y+1)*72+20 :
                    if self.turn == 0 :
                        self.gameDisplay.blit(self.cursor,(x*72+20, y*72+20))
                        if click[0] :
                            self.check[y][x] = 1
                            self.turn = 1
                    else :
                        if (y+1 < self.map_y and self.check[y+1][x] == 1) or \
                            (0 <= y-1 and self.check[y-1][x] == 1) or \
                            (x+1 < self.map_x and self.check[y][x+1] == 1) or \
                            (0<= x-1 and self.check[y][x-1] == 1):
                            self.gameDisplay.blit(self.cursor,(x*72+20, y*72+20))
                            if click[0]:
                                self._switch_neko(y,x)
                                if not self._check_switch(y,x):
                                    self._switch_neko(y,x)
                                self._cursor_set()
                                self.turn = 0
                        if click[2] :
                            self._cursor_set()
                            self.turn = 0
    def _cursor_set(self) :
        for i in range(self.map_y):
            for j in range(self.map_x):
                self.check[i][j] = 0

    def _switch_neko(self, y, x):
        for i in range(self.map_y):
            for j in range(self.map_x):
                if self.check[i][j] == 1:
                    self.neko[i][j], self.neko[y][x] = self.neko[y][x], self.neko[i][j]
                            
    def _check_switch(self,y,x):
        for y in range(10):
            for x in range(8):
                self.search[y][x] = self.neko[y][x]

        for y in range(1, 9):
            for x in range(8):
                if self.search[y][x] > 0:
                    if self.search[y-1][x] == self.search[y][x] and self.search[y+1][x] == self.search[y][x]:
                        return True

        for y in range(10):
            for x in range(1, 7):
                if self.search[y][x] > 0:
                    if self.search[y][x-1] == self.search[y][x] and self.search[y][x+1] == self.search[y][x]:
                        return True
    
if __name__ == "__main__":
    game = GameControl()
    game.game_start()