def game():


    while True :

        idx = 0

        if idx == 0: # 딜레이 주면서 사진 보이기
            idx = check_neko(idx)
        elif 3 > idx >= 1 :
            idx += 1
        elif idx == 3 :
            sweep_neko()
            idx = 0
        m.get_move()
        draw_cursor()
        draw_neko()
        drop_neko()
        pygame.display.update() # 화면 업데이트
        clock.tick(10) #프레임 레이트 지정