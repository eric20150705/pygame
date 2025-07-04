# Doodle Jump 遊戲說明

## 0. 遊戲引擎需求

- 使用 Pygame 進行遊戲開發

## 遊戲開發步驟

### 步驟 1: 基本視窗與主角

- 建立基本遊戲視窗 (400x600像素)
- 繪製一個綠色小方塊作為主角 (30x30像素)
- 玩家要用class player來實作
- `__init__(self, x, y, width, height, color)` 來初始化
- `draw(self, display_area)` 來繪製主角
- 主角初始位置放在底部中間（底部上方50像素）
- 簡單的遊戲迴圈與退出功能
### 步驟 2: 主角移動控制

- 加入鍵盤左右控制功能：
  - 在主程式迴圈中，使用 `pygame.key.get_pressed()` 取得目前按下的按鍵狀態。
  - 當偵測到 `pygame.K_LEFT`（左方向鍵）時，呼叫 `player.move(-1, bg_x)` 讓主角向左移動。
  - 當偵測到 `pygame.K_RIGHT`（右方向鍵）時，呼叫 `player.move(1, bg_x)` 讓主角向右移動。
- 在 Player 類別中，實作 `move(self, direction, bg_x)` 方法：
  - 根據傳入的 direction（1 為右移，-1 為左移）與主角速度，調整主角的 x 座標。
  - 實現穿牆效果：
    - 當主角完全移出左邊界（`self.rect.right < 0`）時，將主角移到右側（`self.rect.left = bg_x`）。
    - 當主角完全移出右邊界（`self.rect.left > bg_x`）時，將主角移到左側（`self.rect.right = 0`）。
- 保持主角的移動速度為 5 像素每次。
- 其餘遊戲流程與步驟 1 相同，包含遊戲迴圈與退出功能。
### 步驟 3: 平台基本實現

- 新增平台物件（60x10像素的白色長條）
  - 建立 Platform 類別，使用 `__init__(self, x, y, width, height, color)` 來初始化平台，並以 `draw(self, display_area)` 方法繪製平台。
  - Platform 類別屬性：
    - `self.rect`：平台的 pygame.Rect 物件，記錄平台的位置與尺寸。
    - `self.color`：平台顏色 (RGB格式)。
  - `__init__` 方法：
    - 參數說明：x, y 為平台左上角座標，width, height 為平台寬高，color 為顏色。
    - 內容：建立 self.rect 與 self.color。
  - `draw(self, display_area)` 方法：
    - 參數說明：display_area 為要繪製的平台視窗。
    - 內容：使用 `pygame.draw.rect(display_area, self.color, self.rect)` 繪製平台。
- 在玩家腳底下加入一個平台，確保玩家不會掉下去：
  - 平台寬度設為60像素，高度10像素，顏色為白色 (255, 255, 255)。
  - 平台位置設在視窗底部上方10像素，水平置中。
  - 於主程式初始化時建立此平台物件：
    - `platform = Platform(platform_x, platform_y, platform_w, platform_h, (255, 255, 255))`
    - 其中 platform_x = (bg_x - platform_w) // 2，platform_y = bg_y - platform_h - 10。
  - 在每次畫面更新時呼叫其 `draw()` 方法：
    - `platform.draw(screen)`
- 其餘遊戲流程與前述步驟相同，包含主角繪製、移動控制、遊戲迴圈與退出功能。
### 步驟 4: 加入跳躍功能

-   Player 類別新增跳躍與重力屬性：
    -   `velocity_y`：主角的垂直速度。
    -   `jump_power`：跳躍初始力量（如 -12，負值代表向上）。
    -   `gravity`：重力加速度（如 0.5）。
    -   `on_platform`：是否站在平台上。
-   Player 類別新增 `apply_gravity(self)` 方法：
    -   每次呼叫時，將 `velocity_y` 增加 `gravity`，然後將主角的 y 座標加上 `velocity_y`。
-   Player 類別新增 `check_platform_collision(self, platform)` 方法：
    -   僅在主角往下掉（`velocity_y > 0`）時檢查碰撞。
    -   若主角底部與平台頂部重疊，且主角左右邊界與平台有交集，則：
        -   將主角底部對齊平台頂部。
        -   將 `velocity_y` 設為 `jump_power`，讓主角跳起。
        -   設定 `on_platform = True`。
-   在主程式遊戲迴圈中：
    -   每次畫面更新時，呼叫 `player.apply_gravity()` 讓主角自動下落。
    -   呼叫 `player.check_platform_collision(platform)`，讓主角能在平台上彈跳。
-   主角跳躍到最高點後會自動往下掉，並可重複在平台上彈跳。
-   其餘遊戲流程與前述步驟相同，包含主角繪製、移動控制、遊戲迴圈與退出功能。
### 步驟 5: 平台隨機生成與進階碰撞檢測

-   隨機生成 8-10 個平台：

    -   在主程式初始化時，先建立一個底部平台，確保玩家不會掉下去。
    -   其餘平台以 for 迴圈隨機產生，數量為 random.randint(8, 10)。
    -   每個平台的 x 座標隨機，y 座標依序往上排列，間距為 60 像素。
    -   平台寬度 60 像素，高度 10 像素，顏色為白色 (255, 255, 255)。
    -   將所有平台物件加入 platforms 列表。

-   平台生成範例：

    -   platform_x = (bg_x - platform_w) // 2
    -   platform_y = bg_y - platform_h - 10
    -   platform = Platform(platform_x, platform_y, platform_w, platform_h, (255, 255, 255))
    -   platforms.append(platform)
    -   其餘平台：
        -   x = random.randint(0, bg_x - platform_w)
        -   y = (bg_y - 100) - (i \* 60)
        -   platform = Platform(x, y, platform_w, platform_h, (255, 255, 255))
        -   platforms.append(platform)

-   優化碰撞偵測系統：

    -   Player 類別的 check_platform_collision 方法會接收 platforms 列表，檢查所有平台的碰撞。
    -   僅在主角往下掉（velocity_y > 0）時檢查碰撞。
    -   根據主角下落速度自動計算檢測點數量（每 5 像素一個檢測點），以避免高速移動時穿透平台。
    -   在主角移動路徑上分段建立多個檢測點，逐步檢查是否與平台重疊。
    -   若主角底部與平台頂部重疊，且左右邊界有交集，則將主角底部對齊平台頂部，並給予跳躍力。
    -   若無碰撞則回傳 False。

-   其餘遊戲流程與前述步驟相同，包含主角繪製、移動控制、遊戲迴圈與退出功能。
### 步驟 6: 畫面捲動與平台生成

-   相機移動系統實作
    -   建立 update_camera() 函式用於處理相機和平台的動態更新
    -   定義畫面中間位置 screen_middle = bg_y // 2 作為相機參考點
    -   當玩家上升到螢幕中間位置以上時，固定玩家在螢幕中間
    -   計算移動距離 camera_move = screen_middle - player.rect.y
    -   將所有平台往下移動該距離，製造玩家往上移動的效果
-   平台管理機制完善
    -   將總平台數量增加到 random.randint(8, 10) + 10 個
    -   檢測並移除超出畫面底部的平台(使用多行 for 迴圈)
    -   使用 y_min 變數追蹤最高平台的位置
    -   當平台數量小於預設數量時，在最高平台上方 60 像素處自動生成新平台
    -   確保新生成的平台位置隨機但垂直間距保持一致
    ### 步驟 7: 分數與遊戲結束

-   新增全域變數
    ```
    ######################全域變數######################
    score = 0  # 紀錄當前分數
    highest_score = 0  # 紀錄最高分數
    game_over = False  # 紀錄遊戲是否結束
    initial_player_y = 0  # 紀錄玩家的初始高度，用於計算分數
    ```
-   加入文字字體"C:/Windows/Fonts/msjh.ttc"
-   加入分數系統，每上升 10 個像素加 1 分，`score += int(camera_move / 10)`
-   加入遊戲結束判定 (當主角掉出畫面)
-   當遊戲結束的時候會顯示分數以及按下任意鍵重新開始遊戲
### 步驟 8: 彈簧道具

-   新增黃色彈簧道具物件 (20x10 像素)
-   彈簧道具會隨機生成在平台上方，並且不會與平台重疊
-   彈簧要跟著平台一起移動
-   彈簧在離開視窗的時候會自動消失，可以參考平台的移除邏輯(使用多行 for 迴圈+remove())
-   彈簧的生成機率 20%
-   目前玩家看的到隨機彈簧但是不具有任何功能
-   不要動到平台相關的程式碼
### 步驟 9: 實現彈簧功能

-   主角碰到彈簧時會有更高的跳躍力 (往上跳 25 像素)
-   先偵測彈簧碰撞再偵測平台碰撞
-   在 Player 類別中新增 `check_spring_collision(self, springs)` 方法：
    -   檢查主角是否與任何彈簧重疊。
    -   若碰撞，將主角的 y 座標調整到彈簧頂部，並給予額外的跳躍力。
    -   基本上跟 `check_platform_collision()` 方法類似，但只處理彈簧。s
    ### 步驟 10: 只能踩一次的平台

-   當分數超過 100 分後，開始出現特殊平台
-   特殊平台的顏色為紅色，並且會隨機混入一般平台列表中
-   特殊平台的生成機率 20%
-   當玩家踩到消失平台後，該平台會立即消失
-   特殊平台可以跳
### 步驟 11: 載入圖片
新增os套件，這個套件可以拿來設定路徑為目前執行的python檔案的位置
新增一個指令，指令名稱叫做load_doodle_sprites，這個指令是拿來載入image資料夾當中的圖片，有一個圖片是src.png，這張照片當中有很多物件，我們等等要切割他，所以我們先把他讀進來，使用convert_alpha進行轉換存到source_image裡面

新增sprite_data字典，裡面可以放
"std_platform": (0, 0, 116, 30),  # 標準平台
"break_platform": (0, 145, 124, 33),  # 可破壞平台
"spring_normal": (376, 188, 71, 35),  # 普通彈簧
這幾個是存從src.png裁減照片的座標以及寬度高度，另外這個字典還有放玩家圖片及圖片路徑:
"player_left_jumping": os.path.join("image", "l.png"),  # 左跳躍
"player_left_falling": os.path.join("image", "ls.png"),  # 左下落
"player_right_jumping": os.path.join("image", "r.png"),  # 右跳躍
"player_right_falling": os.path.join("image", "rs.png"),  # 右下落

接著在新增一個字典sprites，裡面會放已經處理好的圖片，玩家圖片要做convert_alpha處理，其他要裁減的圖片就用source_image.subsurface進行裁切處理，這個字典的key會跟sprite_data的key相同，製作好sprites之後就可以return出去
### 步驟12
請幫我將角色、平台以及彈簧改成image資料夾當中的照片圖案，如果找不到照片使用原本的方塊圖案顯示
將背景換成白色、文字改為黑色
垂直速度小於0表示上升（跳躍中）
反之當垂直速度大於0表示下降

新增變數facing_right
當direction>0，facing_right=True，反之。
預設面相為右邊

新增變數jumping紀錄玩家跳躍狀態
如果有載入照片的話，確認角色存在，根據角色當前狀態選擇適合的圖片，調整大小為實際尺寸，繪製到視窗上面，如果找不到該角色照片就使用原本的方形