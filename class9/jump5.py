###################### 載入套件 ######################
import pygame
import sys
import random


###################### 全域變數 ######################
score = 0  # 當前分數
highest_score = 0  # 最高分數
game_over = False  # 遊戲結束狀態
initial_player_y = 0  # 玩家初始高度（用於計算分數）


###################### 平台類別 ######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台
        x, y: 平台左上角座標\n
        width, height: 平台寬高
        color: 平台顏色 (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製平台
        display_area: pygame顯示區域
        """
        pygame.draw.rect(display_area, self.color, self.rect)


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
        self.speed = 5  # 主角移動速度

        # === 新增跳躍與重力相關屬性 ===
        self.velocity_y = 0  # 垂直速度
        self.jump_power = -12  # 跳躍初始力量（負值代表向上）
        self.gravity = 0.5  # 重力加速度
        self.on_platform = False  # 是否站在平台上

    def draw(self, display_area):
        """
        繪製主角
        display_area: pygame顯示區域
        """
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        控制主角左右移動，並實現穿牆效果
        direction: -1(左), 1(右)
        bg_x: 視窗寬度
        """
        self.rect.x += direction * self.speed
        # 穿牆效果：完全離開左邊界，出現在右側
        if self.rect.right < 0:
            self.rect.left = bg_x
        # 穿牆效果：完全離開右邊界，出現在左側
        if self.rect.left > bg_x:
            self.rect.right = 0

    def apply_gravity(self):
        """
        應用重力，讓主角自動下落或上升
        """
        self.velocity_y += self.gravity  # 垂直速度隨重力增加
        self.rect.y += int(self.velocity_y)  # 更新主角y座標

    def check_platform_collision(self, platforms):
        """
        檢查主角是否與所有平台碰撞，並處理彈跳
        platforms: 平台列表
        """
        # 僅在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度分段檢查，避免高速時穿透平台
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                # 計算每個檢查點的y座標
                check_y = (
                    self.rect.bottom
                    - int(self.velocity_y)
                    + int(step * self.velocity_y / steps)
                )
                check_rect = pygame.Rect(self.rect.left, check_y, self.rect.width, 1)
                for platform in platforms:
                    # 主角底部與平台頂部重疊，且左右有交集
                    if (
                        check_rect.colliderect(platform.rect)
                        and self.rect.right > platform.rect.left
                        and self.rect.left < platform.rect.right
                    ):
                        # 將主角底部對齊平台頂部
                        self.rect.bottom = platform.rect.top
                        # 讓主角跳起
                        self.velocity_y = self.jump_power
                        self.on_platform = True
                        return  # 一旦碰到平台就結束檢查
            self.on_platform = False
        else:
            self.on_platform = False


###################### 初始化設定 ######################
pygame.init()
FPS = pygame.time.Clock()

###################### 字型設定 ######################
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 28)  # 微軟正黑體

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Doodle Jump - Step 7")

###################### 主角設定 ######################
player_width = 30
player_height = 30
player_color = (0, 200, 0)  # 綠色
player_x = (win_width - player_width) // 2
player_y = win_height - player_height - 50
player = Player(player_x, player_y, player_width, player_height, player_color)
initial_player_y = player.rect.y  # 記錄初始高度

###################### 平台設定 ######################
platform_width = 60
platform_height = 10
platform_color = (255, 255, 255)  # 白色

# === 步驟6：隨機產生多個平台，並支援動態生成 ===
platforms = []

# 產生底部平台，確保玩家不會掉下去
platform_x = (win_width - platform_width) // 2
platform_y = win_height - platform_height - 10
base_platform = Platform(
    platform_x, platform_y, platform_width, platform_height, platform_color
)
platforms.append(base_platform)

# 隨機產生 8~10 個平台，y座標依序往上排列，間距60像素
platform_count = random.randint(8, 10)
for i in range(platform_count):
    x = random.randint(0, win_width - platform_width)
    y = (win_height - 100) - (i * 60)
    platform = Platform(x, y, platform_width, platform_height, platform_color)
    platforms.append(platform)


###################### 畫面捲動與平台生成函式 ######################
def update_camera_and_platforms(
    player,
    platforms,
    win_height,
    win_width,
    platform_width,
    platform_height,
    platform_color,
):
    """
    畫面捲動與平台動態生成
    - 當主角上升到畫面中間以上時，畫面跟著主角往上移動
    - 超出畫面底部的平台會被移除
    - 在頂端自動生成新平台，保持平台數量
    - 於此函式內直接加分
    """
    global score, highest_score  # 新增：於此函式直接加分
    screen_middle = win_height // 2  # 螢幕中間y座標
    camera_move = 0
    # 若主角上升到畫面中間以上
    if player.rect.y < screen_middle:
        # 計算要移動的距離
        camera_move = screen_middle - player.rect.y
        # 固定主角在畫面中間
        player.rect.y = screen_middle
        # 所有平台往下移動camera_move
        for plat in platforms:
            plat.rect.y += camera_move
        # 分數計算：每上升10像素加1分
        score += int(camera_move / 10)
        if score > highest_score:
            highest_score = score

    # 移除掉出畫面底部的平台
    platforms[:] = [plat for plat in platforms if plat.rect.top < win_height]

    # 保持平台數量，若不足則在頂端自動生成新平台
    while len(platforms) < platform_count + 1:  # +1是底部平台
        # 找出目前最高的平台y座標
        y_min = min(plat.rect.y for plat in platforms)
        # 新平台y座標在最高平台上方60像素
        new_y = y_min - 60
        new_x = random.randint(0, win_width - platform_width)
        new_platform = Platform(
            new_x, new_y, platform_width, platform_height, platform_color
        )
        platforms.append(new_platform)
    # 不再回傳camera_move


###################### 遊戲重設函式 ######################
def reset_game():
    """
    遊戲重新開始時重設所有狀態
    """
    global score, game_over, player, platforms, platform_count, initial_player_y
    score = 0
    game_over = False
    # 重設主角
    player.rect.x = (win_width - player_width) // 2
    player.rect.y = win_height - player_height - 50
    player.velocity_y = 0
    initial_player_y = player.rect.y
    # 重新產生平台
    platforms.clear()
    base_platform = Platform(
        (win_width - platform_width) // 2,
        win_height - platform_height - 10,
        platform_width,
        platform_height,
        platform_color,
    )
    platforms.append(base_platform)
    platform_count = random.randint(8, 10)
    for i in range(platform_count):
        x = random.randint(0, win_width - platform_width)
        y = (win_height - 100) - (i * 60)
        platform = Platform(x, y, platform_width, platform_height, platform_color)
        platforms.append(platform)


###################### 主程式迴圈 ######################
while True:
    FPS.tick(60)  # 設定每秒更新60次

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 遊戲結束時按任意鍵重新開始
        if game_over and event.type == pygame.KEYDOWN:
            reset_game()

    # 遊戲進行中
    if not game_over:
        # 取得目前按鍵狀態
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, win_width)
        if keys[pygame.K_RIGHT]:
            player.move(1, win_width)

        # 主角自動下落與彈跳
        player.apply_gravity()
        player.check_platform_collision(platforms)

        # 畫面捲動與平台動態生成（分數已於函式內加分）
        update_camera_and_platforms(
            player,
            platforms,
            win_height,
            win_width,
            platform_width,
            platform_height,
            platform_color,
        )

        # 遊戲結束判定：主角掉出畫面底部
        if player.rect.top > win_height:
            game_over = True

    # 畫面繪製
    screen.fill((0, 0, 0))  # 填滿背景（黑色）

    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 顯示分數與最高分數
    score_text = font.render(f"分數: {score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"最高分: {highest_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (10, 40))

    # 遊戲結束畫面
    if game_over:
        over_text = font.render("遊戲結束!", True, (255, 0, 0))
        tip_text = font.render("按任意鍵重新開始", True, (255, 255, 255))
        screen.blit(
            over_text,
            (win_width // 2 - over_text.get_width() // 2, win_height // 2 - 40),
        )
        screen.blit(
            tip_text,
            (win_width // 2 - tip_text.get_width() // 2, win_height // 2 + 10),
        )

    # 更新畫面
    pygame.display.update()
