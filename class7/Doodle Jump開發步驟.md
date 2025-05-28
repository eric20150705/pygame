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
