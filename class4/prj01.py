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
FPS = pygame.time.Clock()
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


class Ball:
    def __init__(self, x, y, radius, color):
        """
        初始球\n
        x, y: 球位置\n
        radius: 球大小\n
        color: 球顏色\n
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 5
        self.speed_y = -5
        self.is_moving = False

    def draw(self, display_area):
        """
        畫出球\n
        display_area: 繪製球的區域\n
        """
        pygame.draw.circle(display_area, self.color, (self.x, self.y), self.radius)

    def move(self):
        """
        球移動\n
        """
        if self.is_moving:
            self.x += self.speed_x
            self.y += self.speed_y


######################顯示文字設定######################

######################底板設定######################
pad = Brick(0, bg_y - 48, bricks_w, bricks_h, (255, 255, 255))
######################球設定######################
ball_radius = 10
ball_color = (255, 215, 0)
ball = Ball(
    pad.rect.x + pad.rect.width // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)
######################遊戲結束設定######################

######################磚塊######################
clock = pygame.time.Clock()
######################主程式######################
while True:
    FPS.tick(60)  # 設定fps
    screen.fill((0, 0, 0))
    mos_x, mos_y = pygame.mouse.get_pos()
    pad.rect.x = mos_x - pad.rect.width // 2

    if pad.rect.x < 0:
        pad.rect.x = 0

    if pad.rect.x + pad.rect.width > bg_x:
        pad.rect.x = bg_x - pad.rect.width

    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for brick in bricks:
        brick.draw(screen)

    pad.draw(screen)
    ball.draw(screen)

    pygame.display.update()
