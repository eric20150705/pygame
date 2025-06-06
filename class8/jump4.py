###################### 載入套件 ######################
import pygame
import sys


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
        self.speed = 15  # 主角移動速度

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

    def check_platform_collision(self, platform):
        """
        檢查主角是否與平台碰撞，並處理彈跳
        platform: Platform 物件
        """
        # 僅在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 主角底部與平台頂部重疊，且左右有交集
            if (
                self.rect.bottom >= platform.rect.top
                and self.rect.bottom <= platform.rect.top + 20  # 容錯範圍
                and self.rect.right > platform.rect.left
                and self.rect.left < platform.rect.right
            ):
                # 將主角底部對齊平台頂部
                self.rect.bottom = platform.rect.top
                # 讓主角跳起
                self.velocity_y = self.jump_power
                self.on_platform = True
            else:
                self.on_platform = False
        else:
            self.on_platform = False


###################### 初始化設定 ######################
pygame.init()
FPS = pygame.time.Clock()

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Doodle Jump - Step 4")

###################### 主角設定 ######################
player_width = 30
player_height = 30
player_color = (0, 200, 0)  # 綠色
player_x = (win_width - player_width) // 2
player_y = win_height - player_height - 50
player = Player(player_x, player_y, player_width, player_height, player_color)

###################### 平台設定 ######################
platform_width = 60
platform_height = 10
platform_color = (255, 255, 255)  # 白色
platform_x = (win_width - platform_width) // 2
platform_y = win_height - platform_height - 10
platform = Platform(
    platform_x, platform_y, platform_width, platform_height, platform_color
)

###################### 主程式迴圈 ######################
while True:
    FPS.tick(60)  # 設定每秒更新60次
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 取得目前按鍵狀態
    keys = pygame.key.get_pressed()
    # 若按下左方向鍵，主角向左移動
    if keys[pygame.K_LEFT]:
        player.move(-1, win_width)
    # 若按下右方向鍵，主角向右移動
    if keys[pygame.K_RIGHT]:
        player.move(1, win_width)

    # === 新增：主角自動下落與彈跳 ===
    player.apply_gravity()  # 應用重力
    player.check_platform_collision(platform)  # 檢查平台碰撞

    # 填滿背景（黑色）
    screen.fill((0, 0, 0))

    # 繪製平台
    platform.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    pygame.display.update()
