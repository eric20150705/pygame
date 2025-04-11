######################匯入模組######################
import pygame
import sys

######################初始化######################
pygame.init()
width = 640
height = 320
######################建立視窗及物件######################
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("my first game")
######################建立畫布######################
# 建立畫布
bg = pygame.Surface((width, height))
# 畫布為藍色
bg.fill((79, 148, 205))
######################繪製圖形######################
# 畫圓形
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)
# 畫矩形
pygame.draw.rect(bg, (0, 255, 0), [270, 130, 60, 40], 5)
# 畫圓角矩形
pygame.draw.ellipse(bg, (255, 0, 0), [130, 160, 60, 35], 5)
pygame.draw.ellipse(bg, (255, 0, 0), [400, 160, 60, 35], 5)
# 畫多邊形
pygame.draw.line(bg, (255, 0, 255), (280, 220), (320, 220), 3)

######################循環偵測######################
while True:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("click!!!")
            print(f"mouse pos: {x}, {y}")

    # 繪製畫布於視窗左上角
    screen.blit(bg, (0, 0))
    # 更新視窗
    pygame.display.update()
