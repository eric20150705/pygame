######################載入套件######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color, is_glow=False):
        """
        初始磚塊\n
        x, y: 磚塊位置\n
        width, height: 磚塊大小\n
        color: 磚塊顏色\n
        is_glow: 是否發光\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit = False
        self.is_glow = is_glow

    def draw(self, display_area, offset=(0, 0)):
        """
        畫出磚塊
        display_area: 繪製磚塊的區域
        offset: (x, y) 螢幕震動偏移
        """
        if not self.hit:
            rect = self.rect.move(offset)
            if self.is_glow:
                # 發光效果：畫外框光暈
                glow_color = (
                    min(self.color[0] + 80, 255),
                    min(self.color[1] + 80, 255),
                    min(self.color[2] + 80, 255),
                )
                # 多層外框
                for i in range(6, 0, -2):
                    pygame.draw.rect(
                        display_area,
                        glow_color,
                        rect.inflate(i * 2, i * 2),
                        border_radius=6,
                    )
            pygame.draw.rect(display_area, self.color, rect)


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

    def draw(self, display_area, offset=(0, 0)):
        pygame.draw.circle(
            display_area,
            self.color,
            (self.x + offset[0], self.y + offset[1]),
            self.radius,
        )

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
        exploded = False
        exploded_indices = set()
        for idx, brick in enumerate(bricks):
            if not brick.hit:
                dx = abs(self.x - (brick.rect.x + brick.rect.width // 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height // 2))

                if dx <= (self.radius + brick.rect.width // 2) and dy <= (
                    self.radius + brick.rect.height // 2
                ):
                    brick.hit = True
                    hit_count += 1
                    exploded = True
                    # 找到該磚塊在陣列中的(row, col)
                    col = (brick.rect.x - 70) // (bricks_w + bricks_gap)
                    row = (brick.rect.y - 60) // (bricks_h + bricks_gap)
                    # 爆炸周圍8格
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < bricks_row and 0 <= nc < bricks_col:
                                nidx = nc * bricks_row + nr
                                if not bricks[nidx].hit:
                                    bricks[nidx].hit = True
                                    exploded_indices.add(nidx)
                                    hit_count += 1
                    if (
                        self.x < brick.rect.x
                        or self.x > brick.rect.x + brick.rect.width
                    ):
                        self.speed_x = -self.speed_x
                    else:
                        self.speed_y = -self.speed_y
        return hit_count, exploded


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
# 取代原本磚塊產生邏輯，隨機部分磚塊發光
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
        is_glow = random.random() < 0.15  # 15% 機率發光
        brick = Brick(x, y, bricks_w, bricks_h, color, is_glow)
        bricks.append(brick)


######################顯示文字設定######################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 28)
score = 0
lives = 3
game_over = True  # 一開始為True，需點擊滑鼠開始
shake_frames = 0  # 震動剩餘幀數
shake_offset = (0, 0)

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
    global bricks, score, lives, ball, game_over, shake_frames
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
            is_glow = random.random() < 0.15  # 15% 機率發光
            brick = Brick(x, y, bricks_w, bricks_h, color, is_glow)
            bricks.append(brick)
    score = 0
    lives = 3
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.speed_x = 5
    ball.speed_y = -5
    ball.is_moving = False
    game_over = False
    shake_frames = 0


######################主程式######################
while True:
    FPS.tick(60)  # 設定fps

    # 螢幕震動偏移
    if shake_frames > 0:
        shake_offset = (random.randint(-8, 8), random.randint(-8, 8))
        shake_frames -= 1
    else:
        shake_offset = (0, 0)

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
            hit, exploded = ball.check_collision(bg_x, bg_y, bricks, pad)
            score += hit
            if exploded:
                shake_frames = 12  # 爆炸時震動12幀
            # 檢查球是否掉到底
            if not ball.is_moving and ball.y + ball.radius >= bg_y:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ball.x = pad.rect.x + pad.rect.width // 2
                    ball.y = pad.rect.y - ball_radius
                    ball.speed_x = 5
                    ball.speed_y = -5
                    ball.is_moving = False
        # 新增：檢查所有磚塊都被打掉
        if all(brick.hit for brick in bricks):
            game_over = True
            lives = 0  # 讓畫面顯示「遊戲結束」

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
        brick.draw(screen, offset=shake_offset)
    pad.draw(screen, offset=shake_offset)
    ball.draw(screen, offset=shake_offset)

    # 顯示分數與剩餘次數
    score_surf = font.render(f"分數: {score}", True, (255, 255, 255))
    lives_surf = font.render(f"剩餘機會: {lives}", True, (255, 255, 255))
    screen.blit(score_surf, (10 + shake_offset[0], 10 + shake_offset[1]))
    screen.blit(lives_surf, (10 + shake_offset[0], 45 + shake_offset[1]))

    if game_over:
        if lives <= 0 and not all(brick.hit for brick in bricks):
            over_surf = font.render("遊戲結束", True, (255, 0, 0))
            tip_surf = font.render("菜就多練，輸不起就別玩", True, (255, 255, 0))
        elif all(brick.hit for brick in bricks):
            over_surf = font.render("遊戲結束", True, (0, 255, 0))
            tip_surf = font.render("教你爸爸", True, (255, 255, 0))
        else:
            over_surf = font.render("遊戲開始", True, (0, 255, 0))
            tip_surf = None
        restart_surf = font.render("按下滑鼠重新開始", True, (255, 255, 255))
        screen.blit(
            over_surf,
            (
                (bg_x - over_surf.get_width()) // 2 + shake_offset[0],
                bg_y // 2 - 40 + shake_offset[1],
            ),
        )
        if tip_surf:
            screen.blit(
                tip_surf,
                (
                    (bg_x - tip_surf.get_width()) // 2 + shake_offset[0],
                    bg_y // 2 + 10 + shake_offset[1],
                ),
            )
            screen.blit(
                restart_surf,
                (
                    (bg_x - restart_surf.get_width()) // 2 + shake_offset[0],
                    bg_y // 2 + 60 + shake_offset[1],
                ),
            )
        else:
            screen.blit(
                restart_surf,
                (
                    (bg_x - restart_surf.get_width()) // 2 + shake_offset[0],
                    bg_y // 2 + 10 + shake_offset[1],
                ),
            )

    pygame.display.update()
