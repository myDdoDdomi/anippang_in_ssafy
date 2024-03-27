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

tri_ready = 0 # 준비화면 트리거

pygame.init()

img_neko = [ #애니팡 
    None,
    pygame.image.load("./img/neko1.png"),
    pygame.image.load("./img/neko2.png"),
    pygame.image.load("./img/neko3.png"),
    pygame.image.load("./img/neko4.png"),
    pygame.image.load("./img/neko5.png"), 
    pygame.image.load("./img/neko6.png"),
    pygame.image.load("./img/neko_niku.png")
]

bg = pygame.image.load("./img/neko_bg.png")
ranking_bg = pygame.image.load("./img/neko_ranking_bg.png")
mainmenu_start = pygame.image.load("./img/start.png")
mainmenu_start_click = pygame.image.load("./img/start_click.png")
display_width = 912
display_height = 768
gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡 서버")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화
st_g = ''
client_sockets = []
point_dict = {}
send = ''
neko = [[0 for _ in range(8)] for _ in range(10)]

def ranking_show():
    global point_dict
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        gameDisplay.blit(ranking_bg,(0,0))
        pygame.display.update()
        clock.tick(15)
        

# def ranking(client_socket, _):
#     global point_dict, client_sockets
#     # while True :
#     point = client_socket.recv(1024).decode('utf-8')
#     NAME, point = point.split()
#     point_dict[NAME] = point
    # print(point_dict)
        # while True:
        #     print(point_dict)
    
class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            gameDisplay.blit(img_in, (x, y))

def ready_neko():
    global neko, client_sockets, tri_ready, point_dict
    while tri_ready == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.blit(bg,(0,0))
        for x in range(len(client_sockets)):
                    y = x//8
                    x = x%8
                    if neko[y][x] == 0 :
                        neko[y][x] = random.choice(range(1,7))

        for i in range(10):
            for j in range(8):
                if neko[i][j] > 0:
                    gameDisplay.blit(img_neko[neko[i][j]], (j*72+20, i*72+20))
        
        pygame.display.update()
        clock.tick(15)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        gameDisplay.blit(ranking_bg,(0,0))
        pygame.display.update()
        clock.tick(15)

# def start_game():
#     global st_g
#     st_g = 'y'

# def server_ready():
#     st_g = ''
#     while True :
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#         gameDisplay.blit(bg,(0,0))
#         Button(mainmenu_start, 240, 450, 150, 80, mainmenu_start_click, 210, 435, start_game)
#         if st_g == 'y' :
#             return st_g
#         pygame.display.update()
#         clock.tick(15)
        

def handle_client(client_socket, _):
    global client_sockets, tri_ready, point_dict

    
    # client_socket.sendall("Welcome to Up & Down game!".encode('utf-8'))
    # while True:
        # client_socket.sendall("Guess the number: ".encode('utf-8'))
        # guess = client_socket.recv(1024).decode('utf-8').strip().strip()
        # ready_1 = Thread(target = server_ready)
    while send != 'y' :
        ...
    

    client_socket.send("시작".encode('utf-8'))
    tri_ready = 1
    # ranking_bg_show = Thread(target = ranking_show)
    # ranking_bg_show.start()

    point = client_socket.recv(1024).decode('utf-8')
    NAME, point = point.split()
    point_dict[NAME] = int(point)
    point_fin = sorted(point_dict.items(), key=lambda x: x[1], reverse=True)
    point_fin = dict(point_fin)
    key_rank = point_fin.keys()
    rank = 1
    print("-------------------------------------------------------------------------")
    print()
    for i in key_rank :
        print(f"{rank}위 : {i} >> {point_dict[i]} point")
        print()
        rank += 1
        
    # else :
    #     continue
        # try :
        #     guess = int(guess)
        #     if guess == answer:
        #         success_num += 1
        #         client_socket.sendall(f"{success_num}번째 정답!".encode('utf-8'))
        #         print(f"{success_num}번째 정답!")
        #     elif guess < answer:
        #         client_socket.sendall("UP~! 다시 입력하세요.".encode('utf-8'))
        #     elif guess > answer :
        #         client_socket.sendall("Down~! 다시 입력하세요.".encode('utf-8'))
        # except :
        #     if '종료' in guess :
        #         break
        

def main():
    global send
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started, listening on port", PORT)
        ready_bg = Thread(target = ready_neko)
        ready_bg.start()
        while True:
            client_socket, _ = server_socket.accept()
            client_sockets.append(client_socket)
            print("Client connected")
            print("참가자 수 : ", len(client_sockets))
            start_new_thread(handle_client, (client_socket, _))
            if len(client_sockets) >= person_num:
                send = str(input("시작하시겠습니까? : (y/n)"))

if __name__ == "__main__":
    main()