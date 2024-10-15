import numpy as np
import cv2
import random

# กำหนดขนาดของกระดานเกม 2048
GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 10
WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * PADDING
HEIGHT = WIDTH
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# สร้างกระดานเกม
def start_game():
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    add_random_tile(board)
    add_random_tile(board)
    return board

# เพิ่มตัวเลข 2 หรือ 4 ในช่องว่างแบบสุ่ม
def add_random_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

# การวาดกระดานเกม
def draw_board(board):
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:] = BACKGROUND_COLOR

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            x = j * TILE_SIZE + (j + 1) * PADDING
            y = i * TILE_SIZE + (i + 1) * PADDING
            tile_color = TILE_COLORS.get(tile_value, (60, 58, 50))
            cv2.rectangle(img, (x, y), (x + TILE_SIZE, y + TILE_SIZE), tile_color, -1)

            if tile_value > 0:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5 + (len(str(tile_value)) - 1) * 0.1
                text_size, _ = cv2.getTextSize(str(tile_value), font, font_scale, 2)
                text_x = x + (TILE_SIZE - text_size[0]) // 2
                text_y = y + (TILE_SIZE + text_size[1]) // 2
                cv2.putText(img, str(tile_value), (text_x, text_y), font, font_scale, (0, 0, 0), 2)

    return img

# ฟังก์ชันการรวมตัวเลข เช่น เลื่อนซ้าย
def compress_and_merge_line(line):
    # รวมตัวเลขแบบเลื่อนซ้าย
    new_line = [i for i in line if i != 0]
    for i in range(len(new_line) - 1):
        if new_line[i] == new_line[i + 1]:
            new_line[i] *= 2
            new_line[i + 1] = 0
    new_line = [i for i in new_line if i != 0]
    return new_line + [0] * (GRID_SIZE - len(new_line))

def slide_left(board):
    for i in range(GRID_SIZE):
        board[i] = compress_and_merge_line(board[i])
    return board

def slide_right(board):
    for i in range(GRID_SIZE):
        board[i] = compress_and_merge_line(board[i][::-1])[::-1]
    return board

def slide_up(board):
    for j in range(GRID_SIZE):
        column = compress_and_merge_line([board[i][j] for i in range(GRID_SIZE)])
        for i in range(GRID_SIZE):
            board[i][j] = column[i]
    return board

def slide_down(board):
    for j in range(GRID_SIZE):
        column = compress_and_merge_line([board[i][j] for i in range(GRID_SIZE)][::-1])[::-1]
        for i in range(GRID_SIZE):
            board[i][j] = column[i]
    return board

# ตรวจสอบว่าเกมจบหรือไม่
def is_game_over(board):
    if np.any(board == 0):
        return False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return False
    return True

# อัพเดตบอร์ดจากการกดปุ่ม
def update_board(board, key):
    new_board = board.copy()
    if key == ord('a'):  # ซ้าย
        new_board = slide_left(new_board)
    elif key == ord('d'):  # ขวา
        new_board = slide_right(new_board)
    elif key == ord('w'):  # ขึ้น
        new_board = slide_up(new_board)
    elif key == ord('s'):  # ลง
        new_board = slide_down(new_board)

    if not np.array_equal(board, new_board):
        add_random_tile(new_board)
    return new_board

# เริ่มเกม
def main():
    board = start_game()
    while True:
        img = draw_board(board)
        cv2.imshow('2048', img)

        if is_game_over(board):
            cv2.putText(img, "Game Over", (WIDTH // 4, HEIGHT // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.imshow('2048', img)
            cv2.waitKey(10000)  # รอ 10 วินาทีเพื่อให้ผู้เล่นเห็นข้อความ
            break

        key = cv2.waitKey(0)
        if key == 27:  # กด Esc เพื่อออก
            break
        board = update_board(board, key)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
