###################### 載入套件 ######################
import pygame
import sys


###################### 主角類別 ######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角
        x, y: 主角左上角座標\n
        width, height: 主角寬高
        color: 主角顏色 (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製主角
        display_area: pygame顯示區域
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 初始化設定 ######################
pygame.init()
FPS = pygame.time.Clock()

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Doodle Jump - Step 1")

###################### 主角設定 ######################
player_width = 30
player_height = 30
player_color = (0, 200, 0)  # 綠色
# 主角初始位置：底部中間，底部上方50像素
player_x = (win_width - player_width) // 2
player_y = win_height - player_height - 50
player = Player(player_x, player_y, player_width, player_height, player_color)

###################### 主程式迴圈 ######################
while True:
    FPS.tick(60)  # 設定每秒更新60次
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 填滿背景（黑色）
    screen.fill((0, 0, 0))

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    pygame.display.update()
