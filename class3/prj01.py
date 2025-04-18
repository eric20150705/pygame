######################載入套件######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color):
        """
        初始磚塊\n
        x, y: 磚塊位置\n
        width, height: 磚塊大小\n
        color: 磚塊顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit = False

    def draw(self, display_area):
        """
        畫出磚塊\n
        display_area: 繪製磚塊的區域\n
        """
        if not self.hit:
            pygame.draw.rect(display_area, self.color, self.rect)


######################定義函式區######################

######################初始化設定######################
pygame.init()
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600
bg_size = (bg_x, bg_y)
pygame.display.set_caption("打磚塊遊戲")
screen = pygame.display.set_mode(bg_size)
######################磚塊######################
bricks_row = 9
bricks_col = 11
bricks_w = 58
bricks_h = 16
bricks_gap = 2
bricks = []  # 用來裝磚塊物件的列表
for col in range(bricks_col):
    for row in range(bricks_row):
        x = col * (bricks_w + bricks_gap) + 70  # 70是邊界距離
        y = row * (bricks_h + bricks_gap) + 60  # 60是邊界距離
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        brick = Brick(x, y, bricks_w, bricks_h, color)
        bricks.append(brick)

######################顯示文字設定######################

######################底板設定######################

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for brick in bricks:
        brick.draw(screen)

    pygame.display.update()
