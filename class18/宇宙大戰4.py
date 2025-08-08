###################### 載入套件 ######################
import pygame
import sys
import os

###################### 初始化設定 ######################
os.chdir(  ####################################################################
    sys.path[0]
)  # 設定當前工作目錄為腳本所在目錄     下次一定要講，不然就完了!!!!!!
pygame.init()  # 下次一定要講，不然就完了!!!!!!
FPS = (
    pygame.time.Clock()
)  ####################################################################
###################### 載入背景圖片並取得尺寸 ######################
# 載入背景圖
bg_img = pygame.image.load("space.png")
# 取得圖片原始寬高
bg_width, bg_height = bg_img.get_size()

###################### 遊戲視窗設定 ######################
# 視窗大小與背景圖一致
screen = pygame.display.set_mode((bg_width, bg_height))
pygame.display.set_caption("宇宙大戰")

# 若背景圖不是100%剛好填滿視窗，可用下行自動縮放（本例已與視窗同尺寸，通常不需）
# bg_img = pygame.transform.smoothscale(bg_img, (bg_width, bg_height))

###################### 捲動參數 ######################
# 兩張背景圖輪流上下捲動，產生無縫循環效果
bg_y1 = (
    0  # 設定圖片的座標                        #######################################
)
bg_y2 = -bg_height  #######################################
bg_scroll_speed = 2  # 捲動速度（像素/幀）          ########################

###################### 主角設定 ######################
# 載入主角圖片
player_img = pygame.image.load("fighter_M.png")
# 取得主角圖片尺寸
player_w, player_h = player_img.get_size()
# 設定主角初始座標（畫面中央下方）
player_x = (bg_width - player_w) // 2
player_y = bg_height - player_h - 30
# 主角移動速度
player_speed = 5
###################### 主程式迴圈 ######################
while True:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 更新背景座標（捲動效果）
    bg_y1 += bg_scroll_speed
    bg_y2 += bg_scroll_speed
    # 當一張圖完全離開畫面時，重設到最上方
    if bg_y1 >= bg_height:
        bg_y1 = -bg_height
    if bg_y2 >= bg_height:
        bg_y2 = -bg_height

    # 處理鍵盤連續按壓（移動主角）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # 限制主角不超出邊界
    if player_x < 0:
        player_x = 0
    if player_x > bg_width - player_w:
        player_x = bg_width - player_w
    if player_y < 0:
        player_y = 0
    if player_y > bg_height - player_h:
        player_y = bg_height - player_h

    # 繪製背景
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))
    # 繪製主角
    screen.blit(player_img, (player_x, player_y))

    # 更新畫面
    pygame.display.update()
