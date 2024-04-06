import socket
import random
import pygame
from _thread import *
import sys
import time
from threading import Thread

HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
person_num = 3 # 게임 인원
display_width = 912
display_height = 768
client_sockets = []
tri_ready = 0
final_tri = 0
point_dict = {}
BLACK = (0,0,0)

class ready_neko:
    def __init__(self) -> None:
        
        
        

        self.img_neko = [ #애니팡 
            None,
            pygame.image.load("./img/neko1.png"),
            pygame.image.load("./img/neko2.png"),
            pygame.image.load("./img/neko3.png"),
            pygame.image.load("./img/neko4.png"),
            pygame.image.load("./img/neko5.png"), 
            pygame.image.load("./img/neko6.png"),
            pygame.image.load("./img/neko_niku.png")
        ]

        self.bg = pygame.image.load("./img/neko_bg.png")
        self.ranking_bg = pygame.image.load("./img/neko_ranking_bg.png")
        self.mainmenu_start = pygame.image.load("./img/start.png")
        self.mainmenu_start_click = pygame.image.load("./img/start_click.png")
        
        st_g = ''
        
        point_dict = {}

        self.neko = [[0 for _ in range(8)] for _ in range(10)]

    def gameOn(self) :
        global tri_ready, point_fin, final_tri, point_dict
        pygame.init()
        font_1 = pygame.font.SysFont("malgungothic",53)
        pygame.display.set_caption("애니팡 서버")  # 타이틀
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화
        self.gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
        
        def button(img_in, x, y, width, height, img_act, x_act, y_act, action=None):
            mouse = pygame.mouse.get_pos()  # 마우스 좌표
            click = pygame.mouse.get_pressed()  # 클릭여부
            if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
                self.gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
                if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                    time.sleep(0.2)
                    action()
            else:
                self.gameDisplay.blit(img_in, (x, y))
                    
        while tri_ready == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.gameDisplay.blit(self.bg,(0,0))
            for x in range(len(client_sockets)):
                        y = x//8
                        x = x%8
                        if self.neko[y][x] == 0 :
                            self.neko[y][x] = random.choice(range(1,7))

            for i in range(10):
                for j in range(8):
                    if self.neko[i][j] > 0:
                        self.gameDisplay.blit(self.img_neko[self.neko[i][j]], (j*72+20, i*72+20))
            
            button(self.mainmenu_start, 240, 550, 150, 80, self.mainmenu_start_click, 210, 535, start)
            pygame.display.update()
            self.clock.tick(15)
        #--------------------------
        while tri_ready == 1 :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.gameDisplay.blit(self.ranking_bg,(0,0))
            if final_tri == 1 :
                key_rank = point_fin.keys()
                rank = 1
                for i in key_rank :
                    txt = font_1.render(f"{i} : {point_dict[i]} point", True, BLACK)
                    self.gameDisplay.blit(txt,(283,120+100*rank))
                    rank += 1
                    if rank == 6:
                        break
            pygame.display.update()
            self.clock.tick(15)
     
     
        
    def game_start(self) :
        ready_bg = Thread(target = self.gameOn)
        ready_bg.start()

def start():
    global tri_ready
    tri_ready = 1


    

def handle_client(client_socket, _):
    global client_sockets, tri_ready, point_dict, point_fin, final_tri
    while tri_ready == 0 :
        if tri_ready == 1 :
            for client in client_sockets:
                client.send("시작".encode('utf-8'))
                
    point = client_socket.recv(1024).decode('utf-8')
    NAME, point = point.split()
    point_dict[NAME] = int(point)
    point_fin = sorted(point_dict.items(), key=lambda x: x[1], reverse=True)
    point_fin = dict(point_fin)
    final_tri = 1
        # else :
        #     tri_ready = 1


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started, listening on port", PORT)
        
        a = ready_neko()
        a.game_start()
        while True:
            client_socket, _ = server_socket.accept()
            client_sockets.append(client_socket)
            print("Client connected")
            print("참가자 수 : ", len(client_sockets))
            start_new_thread(handle_client, (client_socket, _))
            

if __name__ == "__main__":
    main()