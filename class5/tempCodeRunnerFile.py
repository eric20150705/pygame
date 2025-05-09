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

    def check_collision(self, bg_x, bg_y, bricks, pad):
        """
        檢查球是否碰到磚塊\n
        bg_x, bg_y: 背景大小\n
        bricks: 磚塊列表\n
        pad: 底板物件\n
        """
        if self.x - self.radius <= 0 or self.x + self.radius >= bg_x:
            self.speed_x = -self.speed_x

        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

        if self.y + self.radius >= bg_y:
            self.is_moving = False

        if (
            self.y + self.radius >= pad.rect.y
            and self.y + self.radius <= pad.rect.y + pad.rect.height
            and self.x >= pad.rect.x
            and self.x <= pad.rect.x + pad.rect.width
        ):
            self.speed_y = -abs(self.speed_y)

        hit_count = 0
        for brick in bricks:
            if not brick.hit:
                dx = abs(self.x - (brick.rect.x + brick.rect.width // 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height // 2))

                if dx <= (self.radius + brick.rect.width // 2) and dy <= (
                    self.radius + brick.rect.height // 2
                ):
                    brick.hit = True
                    hit_count += 1
                    if (
                        self.x < brick.rect.x
                        or self.x > brick.rect.x + brick.rect.width
                    ):
                        self.speed_x = -self.speed_x
                    else:
                        self.speed_y = -self.speed_y
        return hit_count


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


######################顯示文字設定######################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 28)
score = 0
lives = 3
game_over = True  # 一開始為True，需點擊滑鼠開始

######################底板設定######################
pad = Brick(0, bg_y - 48, bricks_w, bricks_h, (255, 255, 255))
######################球設定######################
ball_radius = 10
ball_color = (255, 215, 0)
ball = Ball(
    pad.rect.x + pad.rect.width // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)
######################遊戲結束設定######################


def reset_game():
    global bricks, score, lives, ball, game_over
    # 重設磚塊
    bricks.clear()
    for col in range(bricks_col):
        for row in range(bricks_row):
            x = col * (bricks_w + bricks_gap) + 70
            y = row * (bricks_h + bricks_gap) + 60
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255),
            )
            brick = Brick(x, y, bricks_w, bricks_h, color)
            bricks.append(brick)
    score = 0
    lives = 3
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.speed_x = 5
    ball.speed_y = -5
    ball.is_moving = False
    game_over = False


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

    if not game_over:
        if not ball.is_moving:
            ball.x = pad.rect.x + pad.rect.width // 2
            ball.y = pad.rect.y - ball_radius
        else:
            ball.move()
            score += ball.check_collision(bg_x, bg_y, bricks, pad)
            # 檢查球是否掉到底
            if not ball.is_moving and ball.y + ball.radius >= bg_y:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # 重設球位置
                    ball.x = pad.rect.x + pad.rect.width // 2
                    ball.y = pad.rect.y - ball_radius
                    ball.speed_x = 5
                    ball.speed_y = -5
                    ball.is_moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            elif not ball.is_moving:
                ball.is_moving = True

    for brick in bricks:
        brick.draw(screen)
    pad.draw(screen)
    ball.draw(screen)

    # 顯示分數與剩餘次數
    score_surf = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))
    lives_surf = font.render(f"剩餘機會: {lives}", True, (255, 255, 255))
    screen.blit(lives_surf, (10, 45))

    if game_over:
        over_surf = font.render("遊戲結束", True, (255, 0, 0))
        restart_surf = font.render("按下滑鼠重新開始", True, (255, 255, 255))
        # 置中顯示
        screen.blit(over_surf, ((bg_x - over_surf.get_width()) // 2, bg_y // 2 - 40))
        screen.blit(
            restart_surf, ((bg_x - restart_surf.get_width()) // 2, bg_y // 2 + 10)
        )

    pygame.display.update()
