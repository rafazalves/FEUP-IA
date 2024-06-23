import pygame
import math

REGULAR_COLOR_PLAYER1 = (255, 255, 255)
REGULAR_COLOR_PLAYER2 = ( 0, 0, 0 )
SELECTED_COLOR = (0, 255, 0)


# Function to calculate the six points of a hexagon
def calculate_hexagon_points(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i 
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    return points

def draw_arrow(screen, color, start, end):
    pygame.draw.polygon(screen, color, ((start[0], start[1] + 25), (start[0], start[1] + 50), (start[0] + 50, start[1] + 50), (start[0] + 50, start[1] + 75), (start[0] + 75, start[1] + 37.5), (start[0] + 50, start[1]), (start[0] + 50, start[1] + 25)))

def draw_hexagon(surface, color, border_color, center, size):
    border_points = calculate_hexagon_points(center, size)
    inner_points = calculate_hexagon_points(center, size * 0.9)
    pygame.draw.polygon(surface, border_color, border_points)
    pygame.draw.polygon(surface, color, inner_points)

# Function to draw a circle (normal pieces)
def draw_circle(surface, color, border_color, position, radius):
    pygame.draw.circle(surface, border_color, position, radius)
    pygame.draw.circle(surface, color, position, radius - 1)

# Function to draw a circle with a smaller X drawn through it (blocked pieces)
def draw_circle_blocked(surface, color, border_color, position, radius):
    pygame.draw.circle(surface, border_color, position, radius)
    pygame.draw.circle(surface, color, position, radius - 1)
    
    line_length = int(radius / 2)
    # Draw diagonal lines
    pygame.draw.line(surface, border_color, (position[0] - line_length, position[1] - line_length), (position[0] + line_length, position[1] + line_length), 2)
    pygame.draw.line(surface, border_color, (position[0] + line_length, position[1] - line_length), (position[0] - line_length, position[1] + line_length), 2)

def display_turn(screen, current_player):
    font = pygame.font.Font("fonts/JosefinSans-Regular.ttf", 36)
    turn_text = font.render(f"Player {current_player}'s Turn", True, (255, 255, 255))
    screen.blit(turn_text, (10, 10))

# Function to draw the board of the game
def draw_map(screen):
    # Fill the screen with a color
    screen.fill("black")

    space = 60
    counter = 1

    # Drawing the hexagons for the ui
    for _ in range(3):
        for j in range(counter):
            x = 600 + j * 100 - 50 * counter
            y = 0 + space
            draw_hexagon(screen, ( 248, 196, 113 ), ( 175, 96, 26 ), (x, y), 30)
        counter += 1
        space += 30

    for _ in range(5):
        for j in range(4):
            x = 600 + j * 100 - 50 * 4
            y = 0 + space
            draw_hexagon(screen, (248, 196, 113 ), ( 175, 96, 26 ), (x, y), 30)
        space += 30
        for j in range(5):
            x = 600 + j * 100 - 50 * 5
            y = 0 + space
            draw_hexagon(screen, (248, 196, 113 ), ( 175, 96, 26 ), (x, y), 30)
        space += 30

    counter = 4
    for _ in range(4):
        for j in range(counter):
            x = 600 + j * 100 - 50 * counter
            y = 0 + space
            draw_hexagon(screen, (248, 196, 113 ), ( 175, 96, 26 ), (x, y), 30)
        counter -= 1
        space += 30

# Draw the pieces
def draw_pieces(screen, instance):
    
    draw_circle(screen, (255, 0, 0), ( 175, 96, 26 ), (550 , 540), 10)
    draw_circle(screen, (0, 0, 255), ( 175, 96, 26 ), (550 , 60), 10)
        
    for (x,y) in instance.player1:
        color = SELECTED_COLOR if (x,y) == instance.selected_piece else REGULAR_COLOR_PLAYER1
        draw_circle(screen, color, ( 175, 96, 26 ), (550 + (x * 50), 300 + (y * 30)), 20)

    for (x,y) in instance.player2:
        color = SELECTED_COLOR if (x,y) == instance.selected_piece else REGULAR_COLOR_PLAYER2
        draw_circle(screen, color, ( 175, 96, 26 ), (550 + (x * 50), 300 + (y * 30)), 20)

    for (x,y) in instance.p1blocked:
        draw_circle_blocked(screen, REGULAR_COLOR_PLAYER1, ( 175, 96, 26 ), (550 + (x * 50), 300 + (y * 30)), 20)

    for (x,y) in instance.p2blocked:
        draw_circle_blocked(screen, REGULAR_COLOR_PLAYER2, ( 175, 96, 26 ), (550 + (x * 50), 300 + (y * 30)), 20)

    if instance.selected_piece is not None:
        for (x,y) in instance.get_valid_moves(instance.selected_piece):
            draw_circle(screen, (0, 255, 0), ( 175, 96, 26 ), (550 + (x * 50), 300 + (y * 30)), 20)
    # Display current player's turn
    display_turn(screen, instance.playing)

# Draw Main Menu
def start_menu(screen, option):
    screen.fill(( 175, 96, 26 ))

    font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 70)
    title = font.render("Aboyne, 1v1 strategy game", True,(248, 196, 113 ))
    screen.blit(title, (200, 30))

    font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 46)
    text = font.render("Play", True,  (248, 196, 113 ))
    text2 = font.render("Exit", True,  (248, 196, 113 ))
    screen.blit(text, (375, 265))
    screen.blit(text2, (375, 365))

    draw_arrow(screen,(248, 196, 113 ), (250, 250 + 100 * option), (270, 100 + 60 * option))

    pygame.display.flip()

# Draw End Game Menu
def end_screen(screen, winner, option):
    screen.fill(( 175, 96, 26 ))

    font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 70)
    title = font.render("Aboyne, 1v1 strategy game", True,(248, 196, 113 ))
    screen.blit(title, (200, 30))

    font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 60)
    text = font.render(f"Player {winner} wins!", True,  (248, 196, 113 ))
    screen.blit(text, (420, 150))

    back_main_menu = font.render("Back To Main Menu", True,  (248, 196, 113 ))
    exit = font.render("Exit", True,  (248, 196, 113 ))
    screen.blit(back_main_menu, (375, 265))
    screen.blit(exit, (375, 365))

    draw_arrow(screen,(248, 196, 113 ), (250, 250 + 100 * option), (270, 100 + 60 * option))

    pygame.display.flip()

# Draw Menu to Select Player Type
def menu_player(screen, option, player):
        screen.fill(( 175, 96, 26 ))

        font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 70)
        title = font.render("Select Player" + player, True,(248, 196, 113 ))
        screen.blit(title, (200, 30))

        font = pygame.font.Font("fonts/JosefinSans-Bold.ttf", 30)
        text = font.render("Human", True,  (248, 196, 113 ))
        text2 = font.render("Random", True,  (248, 196, 113 ))
        text3 = font.render("MinMax Defensive (Level Easy)", True,  (248, 196, 113 ))
        text4 = font.render("MinMax Defensive (Level Medium)", True,  (248, 196, 113 ))
        text5 = font.render("MinMax Defensive (Level Hard)", True,  (248, 196, 113 ))
        text6 = font.render("MinMax Offensive (Level Easy)", True,  (248, 196, 113 ))
        text7 = font.render("MinMax Offensive (Level Medium)", True,  (248, 196, 113 ))
        text8 = font.render("MinMax Offensive (Level Hard)", True,  (248, 196, 113 ))
        text9 = font.render("Monte Carlo", True,  (248, 196, 113 ))
        screen.blit(text, (375, 130))
        screen.blit(text2, (375, 180))
        screen.blit(text3, (375, 230))
        screen.blit(text4, (375, 280))
        screen.blit(text5, (375, 330))
        screen.blit(text6, (375, 380))
        screen.blit(text7, (375, 430))
        screen.blit(text8, (375, 480))
        screen.blit(text9, (375, 530))

        draw_arrow(screen, (248, 196, 113), (285, 105 + 50 * option), (270, 100 + 60 * option))

        pygame.display.flip()