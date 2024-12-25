import pygame
import random
import time
import json
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE, PADDING = 100, 10
WHITE, BLACK, RED, GREEN, GREY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (150, 150, 150)
BROWN, BEIGE, LIGHTSKIN, DARKBLUE, GOLD =(72, 44, 33), (233, 184, 120), (247, 218, 190), (0, 0, 51), (235, 216, 52)
AQUA, PINK =(59, 173, 255), (242, 65, 172)
HIGH_SCORE_FILE = "high_scores.json"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pair Matching - ET2031")
bold_font = pygame.font.SysFont(None, 76, bold=True) 
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
special_font = pygame.font.Font(None, 28)

click_sound = pygame.mixer.Sound("clicksound.wav")
pair_sound = pygame.mixer.Sound("pairsound.wav")
win_sound = pygame.mixer.Sound("winsound.mp3")
lose_sound = pygame.mixer.Sound("losesound.wav")

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, x, y, width, height, inactive_color, active_color, border_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, border_color, (x-5, y-5, width+10, height+10), 0 , 15)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height), 0 , 10)
        if click[0] == 1 and action is not None:
            click_sound.play()
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), 0 , 10)
    draw_text(text, small_font, WHITE, screen, x + width / 2, y + height / 2)

def draw_tile(text, x, y, width, height, inactive_color, active_color, border_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, border_color, (x-3.5, y-3.5, width+7, height+7), 0 , 15)

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height), 0 , 10)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), 0 , 10)

def create_board3():
    tile_images = [
        pygame.image.load("icon1.png"), pygame.image.load("icon2.png"),
        pygame.image.load("icon3.png"), pygame.image.load("icon4.png"),
        pygame.image.load("icon5.png"), pygame.image.load("icon6.png"),
        pygame.image.load("icon7.png"), pygame.image.load("icon8.png"),
        pygame.image.load("icon9.png"), pygame.image.load("icon10.png")
    ]
    tile_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in tile_images]
    tiles = tile_images * 2 
    random.shuffle(tiles)
    rows = 4
    cols = 5
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            tile = tiles.pop()
            board_row.append(tile)
        board.append(board_row)
    return board, rows, cols
    
def create_board2():
    tile_images = [
        pygame.image.load("icon1.png"), pygame.image.load("icon2.png"),
        pygame.image.load("icon3.png"), pygame.image.load("icon4.png"),
        pygame.image.load("icon5.png"), pygame.image.load("icon6.png")
    ]
    tile_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in tile_images]
    tiles = tile_images * 2 
    random.shuffle(tiles)
    rows = 3
    cols = 4
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            tile = tiles.pop()
            board_row.append(tile)
        board.append(board_row)
    return board, rows, cols

def create_board1():
    tile_images = [
        pygame.image.load("icon1.png"), pygame.image.load("icon2.png"),
        pygame.image.load("icon3.png")
    ]
    tile_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in tile_images]
    tiles = tile_images * 2 
    random.shuffle(tiles)
    rows = 2
    cols = 3
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            tile = tiles.pop()
            board_row.append(tile)
        board.append(board_row)
    return board, rows, cols

def all_tiles_revealed(revealed):
    for row in revealed:
        if not all(row):
            return False
    return True

def game_loop1():
    pygame.draw.rect(screen, WHITE, (0,0,800,600))
    time.sleep(0.25)
    board, rows, cols = create_board1()
    revealed = [[False] * cols for _ in range(rows)]
    waiting_time = 0.5
    selected = []
    score = 0
    time_limit = 15
    last_time=time.time()
    start_time = time.time()
    lives = 3
    wrong_select_count = 0
    combo_count = 0
    running = True
    while running:
        background = pygame.image.load('gameback.png')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0)) 
        pygame.draw.rect(screen, LIGHTSKIN , (40,95,cols*100+50,rows*100+40), 0, 15)
        pygame.draw.rect(screen, LIGHTSKIN, (0,24,800,50))
        draw_button("Back", 650, 490, 100, 50, BROWN, BEIGE, BEIGE, difficulty_menu)
        heart_image = pygame.image.load('icon2.png') 
        heart_image = pygame.transform.scale(heart_image, (28, 28))
        for i in range(lives):
            screen.blit(heart_image, (i * 36 + 270, 34))
        draw_text("Lives:", small_font, BROWN, screen, 220, 50)
        elapsed_time = time.time() - start_time
        time_left = max(0, int(time_limit - elapsed_time))
        draw_text(f'Score: {score}', small_font, BROWN, screen, 100, 50)
        draw_text(f'Time Left: {time_left}s', small_font, BROWN, screen, 670, 50)
        if time_left == 0:
            update_high_scores("easy", player_name, score)
            lose_sound.play()
            pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
            over_image = pygame.image.load('ss.png')  
            over_image = pygame.transform.scale(over_image, (500, 500))  
            screen.blit(over_image, (150, 40)) 
            draw_text(f'Score: {score}', font, DARKBLUE, screen, 400, 125)
            pygame.display.update()
            time.sleep(2)
            running = False
            break
        for row in range(rows):
            for col in range(cols):
                x = col * (TILE_SIZE + PADDING) + PADDING +45
                y = row * (TILE_SIZE + PADDING) + PADDING +100  
                if revealed[row][col] and board[row][col] is not None:
                    screen.blit(board[row][col], (x, y))
                elif board[row][col] is None:
                    continue
                else:
                    draw_tile(" ",x,y,TILE_SIZE,TILE_SIZE, BROWN,BEIGE,BEIGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    difficulty_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
                click_sound.play()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - 45) // (TILE_SIZE + PADDING)
                row = (mouse_y - 100) // (TILE_SIZE + PADDING)
                if row >= 0 and row < rows and col < cols:
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        selected.append((row, col))
            if len(selected) == 2:
                r1, c1 = selected[0]
                r2, c2 = selected[1]
                if board[r1][c1] == board[r2][c2]:
                    if board[r1][c1] == board[r2][c2]:
                        pair_sound.play()
                        board[r1][c1] = None
                        board[r2][c2] = None
                        combo_count += 1
                        score += 10 * combo_count
                        if combo_count > 1:
                            draw_text(f"Combo x{combo_count}!", font, RED , screen, 220, 220)
                            pygame.display.update()
                            time.sleep(0.5)
                        selected = []
                        if combo_count == 4:
                            combo_count = 0
                            lives, time_limit= award_power_up(lives, time_limit, revealed, board)
                    else:
                        combo_count = 0
                elif time.time() - last_time > waiting_time:
                    revealed[r1][c1] = False
                    selected = [selected[1]]
                    wrong_select_count += 1
                    combo_count = 0
                    if wrong_select_count == 2:
                        lives -= 1
                        wrong_select_count = 0
                        if lives == 0:
                            update_high_scores("easy", player_name, score)
                            lose_sound.play()
                            pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                            over_image = pygame.image.load('ss.png')  
                            over_image = pygame.transform.scale(over_image, (500, 500))  
                            screen.blit(over_image, (150, 40)) 
                            draw_text(f'Score: {score}', small_font, DARKBLUE, screen, 400, 125)
                            pygame.display.update()
                            time.sleep(2)
                            running = False      
            if all_tiles_revealed(revealed):
                win_sound.play()
                pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                win_image = pygame.image.load('win1.png')  
                win_image = pygame.transform.scale(win_image, (400, 120))  
                screen.blit(win_image, (195, 210)) 
                pygame.display.update()
                time.sleep(2)
                board, rows, cols = create_board1() 
                revealed = [[False] * cols for _ in range(rows)]  
                start_time = time.time()  
                lives += 1
                score += 30
        pygame.display.update()

def game_loop2():
    board, rows, cols = create_board2()
    revealed = [[False] * cols for _ in range(rows)]
    waiting_time = 0.5
    selected = []
    score = 0
    time_limit = 30
    last_time=time.time()
    start_time = time.time()
    lives = 5
    wrong_select_count = 0
    combo_count = 0
    running = True
    while running:
        background = pygame.image.load('gameback.png')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0)) 
        pygame.draw.rect(screen, LIGHTSKIN , (40,95,cols*100+60,rows*100+50), 0, 15)
        pygame.draw.rect(screen, LIGHTSKIN, (0,24,800,50))
        heart_image = pygame.image.load('icon2.png') 
        heart_image = pygame.transform.scale(heart_image, (28, 28))
        for i in range(lives):
            screen.blit(heart_image, (i * 36 + 270, 34))
        draw_text("Lives:", small_font, BROWN, screen, 220, 50)
        draw_button("Back", 650, 490, 100, 50, BROWN, BEIGE, BEIGE, difficulty_menu)
        elapsed_time = time.time() - start_time
        time_left = max(0, int(time_limit - elapsed_time))
        draw_text(f'Score: {score}', small_font, BROWN, screen, 100, 50)
        draw_text(f'Time Left: {time_left}s', small_font, BROWN, screen, 670, 50)
        if time_left == 0:
            update_high_scores("medium", player_name, score)
            lose_sound.play()
            pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
            over_image = pygame.image.load('ss.png')  
            over_image = pygame.transform.scale(over_image, (500, 500))  
            screen.blit(over_image, (150, 40)) 
            draw_text(f'Score: {score}', small_font, DARKBLUE, screen, 400, 125)
            pygame.display.update()
            time.sleep(2)
            running = False
            break
        for row in range(rows):
            for col in range(cols):
                x = col * (TILE_SIZE + PADDING) + PADDING +45
                y = row * (TILE_SIZE + PADDING) + PADDING +100  
                if revealed[row][col] and board[row][col] is not None:
                    screen.blit(board[row][col], (x, y))
                elif board[row][col] is None:
                    continue
                else:
                    draw_tile(" ",x,y,TILE_SIZE,TILE_SIZE, BROWN,BEIGE,BEIGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    difficulty_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
                click_sound.play()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - 45) // (TILE_SIZE + PADDING)
                row = (mouse_y - 100) // (TILE_SIZE + PADDING)
                if row >= 0 and row < rows and col < cols:
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        selected.append((row, col))
            if len(selected) == 2:
                r1, c1 = selected[0]
                r2, c2 = selected[1]
                if board[r1][c1] == board[r2][c2]:
                    if board[r1][c1] == board[r2][c2]:
                        pair_sound.play()
                        board[r1][c1] = None
                        board[r2][c2] = None
                        combo_count += 1
                        score += 10 * combo_count
                        if combo_count > 1:
                            draw_text(f"Combo x{combo_count}!", font, RED , screen, 220, 220)
                            pygame.display.update()
                            time.sleep(0.5)
                        selected = []
                        if combo_count == 4:
                            combo_count = 0
                            lives, time_limit = award_power_up(lives, time_limit, revealed, board)
                    else:
                        combo_count = 0
                elif time.time() - last_time > waiting_time:
                    revealed[r1][c1] = False
                    selected = [selected[1]]
                    wrong_select_count += 1
                    combo_count = 0
                    if wrong_select_count == 2:
                        lives -= 1
                        wrong_select_count = 0
                        if lives == 0:
                            update_high_scores("medium", player_name, score)
                            lose_sound.play()
                            pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                            over_image = pygame.image.load('ss.png')  
                            over_image = pygame.transform.scale(over_image, (500, 500))  
                            screen.blit(over_image, (150, 40)) 
                            draw_text(f'Score: {score}', small_font, DARKBLUE, screen, 400, 125)
                            pygame.display.update()
                            time.sleep(2)
                            running = False
            if all_tiles_revealed(revealed):
                win_sound.play()
                pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                win_image = pygame.image.load('win1.png')  
                win_image = pygame.transform.scale(win_image, (400, 120))  
                screen.blit(win_image, (195, 210)) 
                pygame.display.update()
                time.sleep(2)
                board, rows, cols = create_board2() 
                revealed = [[False] * cols for _ in range(rows)]  
                start_time = time.time()  
                lives += 2
                score += 30 
        pygame.display.update()

def game_loop3():
    board, rows, cols = create_board3()
    revealed = [[False] * cols for _ in range(rows)]
    waiting_time = 0.5
    selected = []
    score = 0
    last_time=time.time()
    lives = 8
    wrong_select_count = 0
    combo_count = 0
    running = True
    while running:
        background = pygame.image.load('gameback.png')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0)) 
        pygame.draw.rect(screen, LIGHTSKIN , (40,95,cols*100+70,rows*100+60), 0, 15)
        pygame.draw.rect(screen, LIGHTSKIN, (0,24,800,50))
        heart_image = pygame.image.load('icon2.png') 
        heart_image = pygame.transform.scale(heart_image, (28, 28))
        for i in range(lives):
            screen.blit(heart_image, (i * 36 + 270, 34))
        draw_text("Lives:", small_font, BROWN, screen, 220, 50)
        draw_button("Back", 650, 490, 100, 50, BROWN, BEIGE, BEIGE, difficulty_menu)
        draw_text(f'Score: {score}', small_font, BROWN, screen, 100, 50)
        for row in range(rows):
            for col in range(cols):
                x = col * (TILE_SIZE + PADDING) + PADDING +45
                y = row * (TILE_SIZE + PADDING) + PADDING +100  
                if revealed[row][col] and board[row][col] is not None:
                    screen.blit(board[row][col], (x, y))
                elif board[row][col] is None:
                    continue
                else:
                    draw_tile(" ",x,y,TILE_SIZE,TILE_SIZE, BROWN, BEIGE, BEIGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    difficulty_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
                click_sound.play()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - 45) // (TILE_SIZE + PADDING)
                row = (mouse_y - 100) // (TILE_SIZE + PADDING)
                if row >= 0 and row < rows and col < cols:
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        selected.append((row, col))
            if len(selected) == 2:
                r1, c1 = selected[0]
                r2, c2 = selected[1]
                if board[r1][c1] == board[r2][c2]:
                    if board[r1][c1] == board[r2][c2]:
                        pair_sound.play()
                        board[r1][c1] = None
                        board[r2][c2] = None
                        combo_count += 1
                        score += 10 * combo_count
                        if combo_count > 1:
                            draw_text(f"Combo x{combo_count}!", font, RED , screen, 220, 220)
                            pygame.display.update()
                            time.sleep(0.5)
                        selected = []
                        if combo_count == 4:
                            combo_count = 0
                            lives = award_power_up1(lives, revealed, board)
                    else:
                        combo_count = 0
                elif time.time() - last_time > waiting_time:
                    revealed[r1][c1] = False
                    selected = [selected[1]]
                    wrong_select_count += 1
                    combo_count = 0
                    if wrong_select_count == 2:
                        lives -= 1
                        wrong_select_count = 0
                        if lives == 0:
                            update_high_scores("hard", player_name, score)
                            lose_sound.play()
                            pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                            over_image = pygame.image.load('ss.png')  
                            over_image = pygame.transform.scale(over_image, (500, 500))  
                            screen.blit(over_image, (150, 40)) 
                            draw_text(f'Score: {score}', small_font, DARKBLUE, screen, 400, 125)
                            pygame.display.update()
                            time.sleep(2)
                            running = False
            if all_tiles_revealed(revealed):
                win_sound.play()
                pygame.draw.rect(screen, WHITE, (0, 0, 800, 600))
                win_image = pygame.image.load('win1.png')  
                win_image = pygame.transform.scale(win_image, (400, 120))  
                screen.blit(win_image, (195, 210)) 
                pygame.display.update()
                time.sleep(2)
                board, rows, cols = create_board3() 
                revealed = [[False] * cols for _ in range(rows)]  
                start_time = time.time() 
                lives += 3
                score += 30 
        pygame.display.update()

def difficulty_menu():
    while True:
        screen.fill(WHITE)
        background = pygame.image.load('pback.jpg')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0)) 
        draw_button("Easy", 250, 150, 300, 50, BROWN, BEIGE, BEIGE, game_loop1)
        draw_button("Medium", 250, 250, 300, 50, BROWN, BEIGE, BEIGE, game_loop2)
        draw_button("Hard", 250, 350, 300, 50, BROWN, BEIGE,BEIGE, game_loop3)
        draw_button("Back", 300, 450, 200, 50, BROWN, BEIGE,BEIGE, input_name)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    input_name()
        pygame.display.update()  

def quit_game():
    pygame.quit()

def instruction_menu():
    while True:
        background = pygame.image.load('pback.jpg')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0))
        draw_button("", 245, 47, 310, 65, BROWN, BROWN, LIGHTSKIN, None)
        draw_text('How to Play', font, WHITE, screen, 400, 80)
        pygame.draw.rect(screen, LIGHTSKIN, (90, 139, 620, 340), 0 , 30)
        instructions = [
            "1. Click on a tile to flip it and see the image underneath.",
            "2. Click on another tile to flip and match.",
            "3. If the images match, they disappear, and you earn points.",
            "4. If not, the previous images will flip back over.",
            "5. Continue matching pairs until all tiles are cleared.",
            "6. If you match consecutive pairs without mistakes, you",
            "   build a Combo! Higher Combos earn you more points!",
            "7. In each game mode, you have a limited number of hearts.",
            "   If you run out of hearts, you lose!",
            "8. Complete the game before time runs out to win!"
        ]
        y_position = 170
        for instruction in instructions:
            draw_text(instruction, special_font, BROWN, screen, 400, y_position)
            y_position += 30 
        draw_button('Back', 670, 500, 80, 50, BROWN, LIGHTSKIN,LIGHTSKIN,main_menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        pygame.display.update()

def award_power_up(lives, time_limit, revealed, board):
    powerup_types = ["extra_time", "extra_heart", "reveal_all"]
    awarded_powerup = random.choice(powerup_types)
    if awarded_powerup == "extra_time":
        time_limit += 10
        draw_text("Extra Time +10s!", font, RED, screen, 600, 300)
    elif awarded_powerup == "extra_heart":
        lives += 1
        draw_text("Extra Heart +1!", font, RED, screen, 600, 300)
    elif awarded_powerup == "reveal_all":
        draw_text("Reveal All Tiles!", font, RED, screen, 600, 300)
        pygame.display.update()
        time.sleep(1)
        temporarily_revealed = [[True] * len(board[0]) for _ in range(len(board))]
        for row in range(len(board)):
            for col in range(len(board[row])):
                x = col * (TILE_SIZE + PADDING) + PADDING + 45
                y = row * (TILE_SIZE + PADDING) + PADDING + 100
                if board[row][col] is not None:
                    screen.blit(board[row][col], (x, y))
        pygame.display.update()
        time.sleep(2)
        for row in range(len(board)):
            for col in range(len(board[row])):
                if not revealed[row][col]:
                    temporarily_revealed[row][col] = False
    pygame.display.update()
    time.sleep(1)
    return lives, time_limit

def award_power_up1(lives, revealed, board):
    powerup_types = ["extra_heart", "reveal_all"]
    awarded_powerup = random.choice(powerup_types)
    if awarded_powerup == "extra_heart":
        lives += 2
        draw_text("Extra Heart +2!", font, RED, screen, 600, 300)
    elif awarded_powerup == "reveal_all":
        draw_text("Reveal All Tiles!", font, RED, screen, 600, 300)
        pygame.display.update()
        time.sleep(1)
        temporarily_revealed = [[True] * len(board[0]) for _ in range(len(board))]
        for row in range(len(board)):
            for col in range(len(board[row])):
                x = col * (TILE_SIZE + PADDING) + PADDING + 45
                y = row * (TILE_SIZE + PADDING) + PADDING + 100
                if board[row][col] is not None:
                    screen.blit(board[row][col], (x, y))
        pygame.display.update()
        time.sleep(2)
        for row in range(len(board)):
            for col in range(len(board[row])):
                if not revealed[row][col]:
                    temporarily_revealed[row][col] = False
    pygame.display.update()
    time.sleep(1)
    return lives
    
if not os.path.exists(HIGH_SCORE_FILE):
    high_scores = {
        "easy": [],
        "medium": [],
        "hard": []
    }
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(high_scores, file)
else:
    with open(HIGH_SCORE_FILE, "r") as file:
        high_scores = json.load(file)

def save_high_scores():
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(high_scores, file)

def input_name():
    clock = pygame.time.Clock()
    input_active = True
    player_name = ""
    while input_active:
        entername = pygame.image.load('entername.png')
        entername = pygame.transform.scale(entername, (800, 600))  
        screen.blit(entername, (0, 0)) 
        draw_text(player_name, small_font, BROWN, screen, SCREEN_WIDTH // 2, 348)
        draw_button('Back', 670, 500, 80, 50, BROWN, BEIGE,BEIGE,main_menu)
        if player_name:
            draw_text("Press Enter to continue", special_font, BEIGE, screen, SCREEN_WIDTH / 2 + 10, 388)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    return player_name
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 15:
                    player_name += event.unicode
        pygame.display.update()
        clock.tick(30)

def update_high_scores(mode, player_name, score):
    if mode not in high_scores:
        return
    high_scores[mode].append({"name": player_name, "score": score})
    high_scores[mode] = sorted(high_scores[mode], key=lambda x: x["score"], reverse=True)[:3]
    save_high_scores()

def show_high_scores():
    running = True
    while running:
        highscore = pygame.image.load('highscore.png')
        highscore = pygame.transform.scale(highscore, (800, 600))  
        screen.blit(highscore, (0, 0)) 
        draw_button("Back", 670, 500, 80, 50, BROWN, LIGHTSKIN, LIGHTSKIN, main_menu)
        if len(high_scores['easy']) > 0:
            draw_text(f"1. {high_scores['easy'][0]['name']}", special_font, GOLD, screen, 150, 325)
            draw_text(f"{high_scores['easy'][0]['score']} point", special_font, WHITE, screen, 150, 350)
        if len(high_scores['easy']) > 1:
            draw_text(f"2. {high_scores['easy'][1]['name']}", special_font, AQUA, screen, 150, 375)
            draw_text(f"{high_scores['easy'][1]['score']} point", special_font, WHITE, screen, 150, 400)
        if len(high_scores['easy']) > 2:
            draw_text(f"3. {high_scores['easy'][2]['name']}", special_font, PINK, screen, 150, 425)
            draw_text(f"{high_scores['easy'][2]['score']} point", special_font, WHITE, screen, 150, 450)
        if len(high_scores['medium']) > 0:
            draw_text(f"1. {high_scores['medium'][0]['name']}", special_font, GOLD, screen, 395, 325)
            draw_text(f"{high_scores['medium'][0]['score']} point", special_font, WHITE, screen, 395, 350)
        if len(high_scores['medium']) > 1:
            draw_text(f"2. {high_scores['medium'][1]['name']}", special_font, AQUA, screen, 395, 375)
            draw_text(f"{high_scores['medium'][1]['score']} point", special_font, WHITE, screen, 395, 400)
        if len(high_scores['medium']) > 2:
            draw_text(f"3. {high_scores['medium'][2]['name']}", special_font, PINK, screen, 395, 425)
            draw_text(f"{high_scores['medium'][2]['score']} point", special_font, WHITE, screen, 395, 450)
        if len(high_scores['hard']) > 0:
            draw_text(f"1. {high_scores['hard'][0]['name']}", special_font, GOLD, screen, 630, 325)
            draw_text(f"{high_scores['hard'][0]['score']} point", special_font, WHITE, screen, 630, 350)
        if len(high_scores['hard']) > 1:
            draw_text(f"2. {high_scores['hard'][1]['name']}", special_font, AQUA, screen, 630, 375)
            draw_text(f"{high_scores['hard'][1]['score']} point", special_font, WHITE, screen, 630, 400)
        if len(high_scores['hard']) > 2:
            draw_text(f"3. {high_scores['hard'][2]['name']}", special_font, PINK, screen, 630, 425)
            draw_text(f"{high_scores['hard'][2]['score']} point", special_font, WHITE, screen, 630, 450)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        pygame.display.update()

def start_game():
    global player_name
    player_name = input_name()
    difficulty_menu()

def main_menu():
    menu = True
    while menu:
        background = pygame.image.load('pairback.png')
        background = pygame.transform.scale(background, (800, 800))  
        screen.blit(background, (0, 0)) 
        draw_button("Play", 300, 200, 200, 50, BROWN, BEIGE,BEIGE, start_game)
        draw_button("High Scores", 415, 300, 150, 50, BROWN, BEIGE,BEIGE, show_high_scores)
        draw_button("Instruction", 235, 300, 150, 50, BROWN, BEIGE,BEIGE, instruction_menu)
        draw_button("Quit", 300, 400, 200, 50, BROWN, BEIGE,BEIGE, quit_game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        pygame.display.update()

main_menu()