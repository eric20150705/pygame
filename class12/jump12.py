###################### 載入套件 ######################
import pygame
import sys
import random
import os  # 新增：用於處理路徑


###################### 全域變數 ######################
os.chdir(sys.path[0])  # 設定當前工作目錄為腳本所在目錄
score = 0  # 當前分數
highest_score = 0  # 最高分數
game_over = False  # 遊戲結束狀態
initial_player_y = 0  # 玩家初始高度（用於計算分數）
special_platform_chance = 0.2  # 特殊平台生成機率（20%）
special_platform_color = (255, 0, 0)  # 紅色

# === 步驟12：新增角色狀態變數 ===
facing_right = True  # 預設面向右
jumping = False  # 預設非跳躍狀態


###################### 平台類別 ######################
class Platform:
    def __init__(self, x, y, width, height, color, is_special=False):
        """
        初始化平台
        x, y: 平台左上角座標\n
        width, height: 平台寬高
        color: 平台顏色 (RGB)
        is_special: 是否為只能踩一次的特殊平台
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_special = is_special  # 是否為特殊平台
        self.used = False  # 標記特殊平台是否已被踩過

    def draw(self, display_area, sprites=None):
        """
        繪製平台
        display_area: pygame顯示區域
        sprites: 圖片字典（可選）
        """
        # 只繪製未被踩過的特殊平台或一般平台
        if not self.is_special or (self.is_special and not self.used):
            # 步驟12：嘗試使用圖片，否則用方塊
            if sprites:
                # 特殊平台用break_platform，一般平台用std_platform
                if self.is_special and "break_platform" in sprites:
                    img = sprites["break_platform"]
                elif not self.is_special and "std_platform" in sprites:
                    img = sprites["std_platform"]
                else:
                    img = None
                if img:
                    # 調整圖片大小與平台一致
                    img = pygame.transform.smoothscale(
                        img, (self.rect.width, self.rect.height)
                    )
                    display_area.blit(img, self.rect)
                    return
            # 找不到圖片時用原本的方塊
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

        # 步驟12：新增狀態
        self.facing_right = True
        self.jumping = False

    def draw(self, display_area, sprites=None):
        """
        繪製主角
        display_area: pygame顯示區域
        sprites: 圖片字典（可選）
        """
        # 步驟12：根據狀態選擇圖片，否則用方塊
        if sprites:
            # 根據主角狀態決定圖片key
            if self.facing_right:
                if self.velocity_y < 0:
                    key = "player_right_jumping"
                else:
                    key = "player_right_falling"
            else:
                if self.velocity_y < 0:
                    key = "player_left_jumping"
                else:
                    key = "player_left_falling"
            img = sprites.get(key)
            if img:
                # 調整圖片大小為主角尺寸
                img = pygame.transform.smoothscale(
                    img, (self.rect.width, self.rect.height)
                )
                display_area.blit(img, self.rect)
                return
        # 找不到圖片時用原本的方塊
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        控制主角左右移動，並實現穿牆效果
        direction: -1(左), 1(右)
        bg_x: 視窗寬度
        """
        self.rect.x += direction * self.speed
        # 步驟12：根據方向設定面向
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False
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
        # 步驟12：根據垂直速度設定跳躍狀態
        self.jumping = self.velocity_y < 0

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
                    # 跳過已被踩過的特殊平台
                    if platform.is_special and platform.used:
                        continue
                    # 主角底部與平台頂部重疊，且左右有交集
                    if (
                        check_rect.colliderect(platform.rect)
                        and self.rect.right > platform.rect.left
                        and self.rect.left < platform.rect.right
                    ):
                        # 特殊平台：踩到後彈跳一次並立即消失
                        if platform.is_special:
                            self.rect.bottom = platform.rect.top
                            self.velocity_y = self.jump_power
                            self.on_platform = True
                            platform.used = True  # 標記為已踩過
                            return
                        # 一般平台：正常彈跳
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = self.jump_power
                        self.on_platform = True
                        return  # 一旦碰到平台就結束檢查
            self.on_platform = False
        else:
            self.on_platform = False

    def check_spring_collision(self, springs):
        """
        檢查主角是否與所有彈簧碰撞，並處理彈簧彈跳
        springs: 彈簧列表
        """
        # 僅在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度分段檢查，避免高速時穿透彈簧
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                # 計算每個檢查點的y座標
                check_y = (
                    self.rect.bottom
                    - int(self.velocity_y)
                    + int(step * self.velocity_y / steps)
                )
                check_rect = pygame.Rect(self.rect.left, check_y, self.rect.width, 1)
                for spring in springs:
                    # 主角底部與彈簧頂部重疊，且左右有交集
                    if (
                        check_rect.colliderect(spring.rect)
                        and self.rect.right > spring.rect.left
                        and self.rect.left < spring.rect.right
                    ):
                        # 將主角底部對齊彈簧頂部
                        self.rect.bottom = spring.rect.top
                        # 讓主角獲得更高的跳躍力（往上跳25像素）
                        self.velocity_y = -25
                        self.on_platform = True
                        return  # 一旦碰到彈簧就結束檢查
            # 若沒碰到彈簧則不處理
        else:
            self.on_platform = False


###################### 彈簧道具類別 ######################
class Spring:
    def __init__(self, x, y, width=20, height=10, color=(255, 255, 0)):
        """
        初始化彈簧道具
        x, y: 彈簧左上角座標
        width, height: 彈簧寬高（預設20x10）
        color: 彈簧顏色（預設黃色）
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area, sprites=None):
        """
        繪製彈簧道具
        display_area: pygame顯示區域
        sprites: 圖片字典（可選）
        """
        # 步驟12：嘗試使用圖片，否則用方塊
        if sprites and "spring_normal" in sprites:
            img = sprites["spring_normal"]
            img = pygame.transform.smoothscale(img, (self.rect.width, self.rect.height))
            display_area.blit(img, self.rect)
        else:
            pygame.draw.rect(display_area, self.color, self.rect)


###################### 載入圖片與精靈處理 ######################
def load_doodle_sprites():
    """
    載入 image 資料夾中的 src.png 圖片，並裁切出各種遊戲物件的圖片。
    同時載入玩家角色的圖片，並以字典方式回傳所有圖片物件。
    """
    # 取得目前執行檔案的資料夾路徑
    # 圖片資料夾路徑
    img_dir = os.path.join("image")
    # 讀取原始大圖
    source_image = pygame.image.load(os.path.join(img_dir, "src.png")).convert_alpha()
    # 定義各物件在大圖中的座標與尺寸，以及玩家圖片路徑
    sprite_data = {
        "std_platform": (0, 0, 116, 30),  # 標準平台
        "break_platform": (0, 145, 124, 33),  # 可破壞平台
        "spring_normal": (376, 188, 71, 35),  # 普通彈簧
        "player_left_jumping": os.path.join(img_dir, "l.png"),  # 左跳躍
        "player_left_falling": os.path.join(img_dir, "ls.png"),  # 左下落
        "player_right_jumping": os.path.join(img_dir, "r.png"),  # 右跳躍
        "player_right_falling": os.path.join(img_dir, "rs.png"),  # 右下落
    }
    sprites = {}
    # 處理需要裁切的圖片
    for key in ["std_platform", "break_platform", "spring_normal"]:
        x, y, w, h = sprite_data[key]
        sprites[key] = source_image.subsurface(pygame.Rect(x, y, w, h)).copy()
    # 處理玩家圖片（直接載入檔案）
    for key in [
        "player_left_jumping",
        "player_left_falling",
        "player_right_jumping",
        "player_right_falling",
    ]:
        sprites[key] = pygame.image.load(sprite_data[key]).convert_alpha()
    return sprites


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

###################### 載入圖片精靈 ######################
sprites = load_doodle_sprites()  # 步驟12：載入圖片

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
spring_chance = 0.2  # 彈簧生成機率（0~1之間）

# === 步驟6：隨機產生多個平台，並支援動態生成 ===
platforms = []
springs = []  # 新增：用來裝彈簧物件的列表

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
    # 分數超過100分後，開始有機率生成特殊平台
    is_special = False
    plat_color = platform_color
    if score > 100 and random.random() < special_platform_chance:
        is_special = True
        plat_color = special_platform_color
    platform = Platform(x, y, platform_width, platform_height, plat_color, is_special)
    platforms.append(platform)
    # 只有一般平台才會生成彈簧
    if not is_special and random.random() < spring_chance:
        spring_x = x + (platform_width - 20) // 2  # 彈簧水平置中
        spring_y = y - 10  # 彈簧放在平台正上方
        springs.append(Spring(spring_x, spring_y))


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
    - 彈簧道具會跟著平台一起移動，並自動移除離開畫面的彈簧
    - 分數超過100分後，頂端新生成的平台有機率為特殊平台
    """
    global score, highest_score, springs
    screen_middle = win_height // 2
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
        # 所有彈簧也要往下移動camera_move
        for spring in springs:
            spring.rect.y += camera_move
        # 分數計算：每上升10像素加1分
        score += int(camera_move / 10)
        if score > highest_score:
            highest_score = score

    # 移除掉出畫面底部的平台（特殊平台踩過也會被移除）
    platforms[:] = [
        plat
        for plat in platforms
        if plat.rect.top < win_height and (not plat.is_special or not plat.used)
    ]
    # 移除掉出畫面底部的彈簧
    springs[:] = [spring for spring in springs if spring.rect.top < win_height]

    # 保持平台數量，若不足則在頂端自動生成新平台
    while len(platforms) < platform_count + 1:  # +1是底部平台
        # 找出目前最高的平台y座標
        y_min = min(plat.rect.y for plat in platforms)
        # 新平台y座標在最高平台上方60像素
        new_y = y_min - 60
        new_x = random.randint(0, win_width - platform_width)
        # 分數超過100分後，頂端新平台有機率為特殊平台
        is_special = False
        plat_color = platform_color
        if score > 100 and random.random() < special_platform_chance:
            is_special = True
            plat_color = special_platform_color
        new_platform = Platform(
            new_x, new_y, platform_width, platform_height, plat_color, is_special
        )
        platforms.append(new_platform)
        # 只有一般平台才會生成彈簧
        if not is_special and random.random() < spring_chance:
            spring_x = new_x + (platform_width - 20) // 2
            spring_y = new_y - 10
            springs.append(Spring(spring_x, spring_y))
    # 不再回傳camera_move


###################### 遊戲重設函式 ######################
def reset_game():
    """
    遊戲重新開始時重設所有狀態
    """
    global score, game_over, player, platforms, platform_count, initial_player_y, springs
    score = 0
    game_over = False
    # 重設主角
    player.rect.x = (win_width - player_width) // 2
    player.rect.y = win_height - player_height - 50
    player.velocity_y = 0
    player.facing_right = True  # 步驟12：重設面向
    player.jumping = False  # 步驟12：重設跳躍狀態
    initial_player_y = player.rect.y
    # 重新產生平台
    platforms.clear()
    springs = []  # 新增：清空彈簧列表
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
        is_special = False
        plat_color = platform_color
        if score > 100 and random.random() < special_platform_chance:
            is_special = True
            plat_color = special_platform_color
        platform = Platform(
            x, y, platform_width, platform_height, plat_color, is_special
        )
        platforms.append(platform)
        if not is_special and random.random() < spring_chance:
            spring_x = x + (platform_width - 20) // 2
            spring_y = y - 10
            springs.append(Spring(spring_x, spring_y))


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

        # 主角自動下落
        player.apply_gravity()
        # 先檢查彈簧碰撞（若碰到彈簧會直接跳很高）
        player.check_spring_collision(springs)
        # 再檢查平台碰撞（若沒碰到彈簧才會檢查平台）
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
    screen.fill((255, 255, 255))  # 步驟12：填滿背景（白色）

    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen, sprites)

    # 新增：繪製所有彈簧
    for spring in springs:
        spring.draw(screen, sprites)

    # 繪製主角
    player.draw(screen, sprites)

    # 顯示分數與最高分數（步驟12：文字改為黑色）
    score_text = font.render(f"分數: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"最高分: {highest_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (10, 40))

    # 遊戲結束畫面
    if game_over:
        over_text = font.render("遊戲結束!", True, (255, 0, 0))
        tip_text = font.render("按任意鍵重新開始", True, (0, 0, 0))
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
