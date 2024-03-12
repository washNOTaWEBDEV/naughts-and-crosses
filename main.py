import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
default_font = pygame.font.SysFont('kaikokupmm9n', 30)

clock = pygame.time.Clock()


screen_height = screen_width = 600
square_size = screen_height//5

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Naughts and Crosses')

######################## MISCELLANEOUS VARIABLES ######################

clicked = False

player = -1            # alternates between 1 and -1 representing turns
switch_naughts_and_crosses = -1
draw_data = [False, 0]
draw_limit = 3
turns = 0
gameover = False
winner = 0
winning_line_data_draw = ('direction', 'start', 'end')
play_again_rect = Rect(square_size + 10, square_size*2 + 42, square_size*3 - 20, square_size - 82)


############################# GAME SETUP ##############################

board = []

def fill_board():
    global board
    board = []
    for _ in range(5):
        board.append([0]*5)

fill_board()

def draw_gridlines():
    white_bg = (255, 245, 255)
    black_gridline = (50, 50, 90)
    screen.fill(white_bg)
    line_width = 5
    for i in range(2,4):
        pygame.draw.line(screen, black_gridline, (square_size, square_size * i), (square_size*4, square_size * (i)), line_width)
        pygame.draw.line(screen, black_gridline, (square_size * i, square_size), (square_size * i, square_size*4), line_width)
        

def draw_boardstate():
    margin = 15
    cross = pygame.image.load('cross.png')
    cross = pygame.transform.scale(cross, (square_size - margin*2, square_size-margin*2))
    circle = pygame.image.load('circle.png')
    circle = pygame.transform.scale(circle, (square_size - margin*2, square_size-margin*2))

    for rowID, row in enumerate(board):
        for yID, item in enumerate(row):
            if item == switch_naughts_and_crosses: # cross
                pygame.Surface.blit(screen, cross, ((yID) * square_size + margin, (rowID)*square_size + margin))
            elif item == -switch_naughts_and_crosses: # circle
                pygame.Surface.blit(screen, circle, ((yID) * square_size + margin, (rowID)*square_size + margin))

def check_gameover():
    global winning_line_data_draw
    def circle_winner():
        global winner, gameover
        winner = 'circle'
        gameover = True
    def cross_winner():
        global winner, gameover
        winner = 'cross'
        gameover = True
    # rows
    for rowID, row in enumerate(board):
        for a in range(3):
            if row[a]+row[a+1]+row[a+2] == 3:
                circle_winner()
                winning_line_data_draw = ('row', a, a+2, rowID)
            elif row[a]+row[a+1]+row[a+2] == -3:
                cross_winner()
                winning_line_data_draw = ('row', a, a+2, rowID)
    #columns
    for i in range(5):
        for a in range(3):
            if board[a][i] + board[a+1][i] + board[a+2][i] == 3:
                circle_winner()
                winning_line_data_draw = ('column', a, a+2, i)
            elif board[a][i] + board[a+1][i] + board[a+2][i] == -3:
                cross_winner()
                winning_line_data_draw = ('column', a, a+2, i)
    ######### DIAGONALS ########
    for i in range(3):
        for a in range(3):
            if board[i][a] + board[i+1][a+1] + board[i+2][a+2] == 3:
                circle_winner()
                winning_line_data_draw = ('diagonal', i, a, i+2, a+2)
            elif board[i][a] + board[i+1][a+1] + board[i+2][a+2] == -3:
                cross_winner()
                winning_line_data_draw = ('diagonal', i, a, i+2, a+2)
    
    for i in range(3):
        for a in range(2,5):
            if board[i][a] + board[i+1][a-1] + board[i+2][a-2] == 3:
                circle_winner()
                winning_line_data_draw = ('diagonal', i, a, i+2, a-2)
            elif board[i][a] + board[i+1][a-1] + board[i+2][a-2] == -3:
                cross_winner()
                winning_line_data_draw = ('diagonal', i, a, i+2, a-2)

    
    
def end_of_game():
    global winning_line_data_draw
    if winner == 0:
        text = "試合終了。drawだ"
    elif winner == "circle" and switch_naughts_and_crosses == -1 or winner == 'cross' and switch_naughts_and_crosses == 1:
        text = "試合終了！The naughts have won."
    else:
        text = "試合終了！The crosses have won."
    

    end_text = default_font.render(text, True, (0, 0, 0))
    center_text = end_text.get_rect()
    center_text.center = (screen_width//2, square_size*9 //2 - 5)
    screen.blit(end_text, (center_text))

    ############## LINE TO SHOW GAME WINNING STREAK, VARIABLES ##################
    
    color = (140, 140, 200)
    thickness = 6

    if not draw_data[0]:
        if winning_line_data_draw[0] == 'row':
            pygame.draw.line(screen, color, (winning_line_data_draw[1]*square_size + square_size//2 - 5 , winning_line_data_draw[3]*square_size + square_size//2), ((winning_line_data_draw[2]*square_size + square_size//2 + 5 ,winning_line_data_draw[3]*square_size + square_size//2)), thickness)
        elif winning_line_data_draw[0] == "column":
            pygame.draw.line(screen, color, (winning_line_data_draw[3] * square_size + square_size//2, winning_line_data_draw[1] * square_size + square_size//2), (winning_line_data_draw[3] * square_size + square_size//2, winning_line_data_draw[2] * square_size + square_size//2), thickness)
        elif winning_line_data_draw[0] == 'diagonal':
            pygame.draw.line(screen, color, (winning_line_data_draw[2] * square_size + square_size//2, winning_line_data_draw[1] * square_size + square_size//2), (winning_line_data_draw[4] * square_size + square_size//2, winning_line_data_draw[3] * square_size + square_size//2), thickness)

    if not draw_data[0] and draw_data[1] < draw_limit:
        play_again_text = "お前、本当に馬鹿だな。"
    elif not draw_data[0] and draw_data[1] >= draw_limit:
        play_again_text = 'お前ロリが好きだよね？'
    else:
        play_again_text = 'ドローでござる、、:^('

    play_again_img = default_font.render(play_again_text, True, (0, 0, 0))
    play_again_center = play_again_img.get_rect()
    play_again_center.center = (screen_width//2, screen_height//2)
    pygame.draw.rect(screen, (230, 185, 230), play_again_rect)
    screen.blit(play_again_img, (play_again_center))




############################# MAIN LOOP ##################################
run = True
while run:
    draw_gridlines()
    draw_boardstate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if gameover == False:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked==False:
                clicked=True
            elif event.type == pygame.MOUSEBUTTONUP and clicked:
                clicked=False

                mouse_pos = pygame.mouse.get_pos()
                columnID, rowID = map(lambda x: x//square_size, mouse_pos)
                if player == 1 or turns == 9:   # OP PLAYER
                    if -1 < rowID < 5 and -1 < columnID < 5 and board[rowID][columnID] == 0:
                        board[rowID][columnID] = player
                        player *= -1
                        turns += 1
                        check_gameover()
                        if not gameover and turns >= 9:
                            if draw_data[1] < draw_limit: # HOW MANY DRAWS BEFORE CHEAT MODE STARTS
                                draw_data[0] = True
                                gameover = True

                elif player == -1: # HANDICAPPED
                    if 0 < rowID < 4 and 0 < columnID < 4 and board[rowID][columnID] == 0:
                        board[rowID][columnID] = player
                        player *= -1
                        turns += 1
                        check_gameover()
                        if not gameover and turns >= 9:
                            if draw_data[1] < draw_limit: # HOW MANY DRAWS BEFORE CHEAT MODE STARTS
                                draw_data[0] = True
                                gameover = True
    if not gameover and turns == 10:
        draw_data[0] = True
        gameover = True
    if gameover:
        end_of_game()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked==False:
            clicked=True
        elif event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked=False
            pos = pygame.mouse.get_pos()
            if play_again_rect.collidepoint(pos):
                gameover = False
                switch_naughts_and_crosses *= -1
                winner = 0
                turns = 0
                player = -1
                draw_data[0] = False
                draw_data[1] += 1
                fill_board()
                

    pygame.display.flip()
    clock.tick(30)
pygame.quit()