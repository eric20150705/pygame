###################### 載入套件 ######################
import pygame
import sys
import os

###################### 初始化設定 ######################
os.chdir(sys.path[0])  # 設定當前工作目錄為腳本所在目錄
pygame.init()
FPS = pygame.time.Clock()

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
bg_y1 = 0
bg_y2 = -bg_height
bg_scroll_speed = 2  # 捲動速度（像素/幀）

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

    # 繪製背景
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))

    # 更新畫面
    pygame.display.update()
