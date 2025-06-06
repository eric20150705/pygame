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