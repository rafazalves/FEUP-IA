import pygame
import math
import display
import random
import game
import time
import bots
import os
import sys
import copy
import monte_carlo

os.environ['SDL_AUDIODRIVER'] = 'dsp'

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Aboyne")

REGULAR_COLOR_PLAYER1 = (255, 255, 255)
REGULAR_COLOR_PLAYER2 = ( 0, 0, 0 )
SELECTED_COLOR = (0, 255, 0)
winner = 0
p1_moves = 0
p2_moves = -1
p1_time = 0
p2_time = 0

# Menu loop
def menu():
    global winner
    global p1_moves
    global p2_moves
    running = True
    option = 0
    winner = 0
    p1_moves = 0
    p2_moves = -1

    while running:
        if option < 0:
            option = 1
        if option > 1:
            option = 0
        display.start_menu(screen, option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option -= 1
                if event.key == pygame.K_DOWN:
                    option += 1
                if event.key == pygame.K_RETURN:
                    if option == 0:
                        player_type1 = select_player_type("1")
                        player_type2 = select_player_type("2")
                        print(player_type1 + "vs" + player_type2)
                        winner = game_cycle(player_type1, player_type2)
                        end_game(screen, winner)
                    if option == 1:
                        pygame.quit()
                        sys.exit()
                    

def select_player_type(player):
    running = True
    option = 0
    while running:
        if option < 0:
            option = 8
        if option > 8:
            option = 0
        display.menu_player(screen, option, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option -= 1
                if event.key == pygame.K_DOWN:
                    option += 1
                if event.key == pygame.K_RETURN:
                    if option == 0:
                        return "human"
                    elif option == 1:
                        return "random"
                    elif option == 2:
                        return "d_minimax_easy"
                    elif option == 3:
                        return "d_minimax_medium"
                    elif option == 4:
                        return "d_minimax_hard"
                    elif option == 5:
                        return "o_minimax_easy"
                    elif option == 6:
                        return "o_minimax_medium"
                    elif option == 7:
                        return "o_minimax_hard"
                    elif option == 8:
                        return "monte_carlo"
                           

def end_game(screen, winner):
    running = True
    option = 0
    while running:
        if option < 0:
            option = 1
        if option > 1:
            option = 0
        display.end_screen(screen, winner, option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option -= 1
                if event.key == pygame.K_DOWN:
                    option += 1
                if event.key == pygame.K_RETURN:
                    if option == 0:
                        menu()
                    if option == 1:
                        pygame.quit()
                        sys.exit()


def game_cycle(player_type1, player_type2):
    global p1_moves
    global p2_moves
    winner = 0
    instance = game.Game()
    while(winner == 0):
        display.draw_map(screen)
        display.draw_pieces(screen, instance)
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

        if(instance.playing == 1):
            p2_moves += 1
            print("Player 2 did ", p2_moves, " movements until now.")
            match (player_type1):
                case "human":
                    winner = human_play(instance)
                case "random":
                    winner = random_play(instance)
                case "d_minimax_easy":
                    winner = d_minimax_play(instance, 2)
                case "d_minimax_medium":
                    winner = d_minimax_play(instance, 3)
                case "d_minimax_hard":
                    winner = d_minimax_play(instance, 4)
                case "o_minimax_easy":
                    winner = o_minimax_play(instance, 2)
                case "o_minimax_medium":
                    winner = o_minimax_play(instance, 3)
                case "o_minimax_hard":
                    winner = o_minimax_play(instance, 4)
                case "monte_carlo":
                    winner = monte_carlo_play(instance)
        else:
            p1_moves += 1
            print("Player 1 did ", p1_moves, " movements until now.")
            match (player_type2):
                case "human":
                    winner = human_play(instance)
                case "random":
                    winner = random_play(instance)
                case "d_minimax_easy":
                    winner = d_minimax_play(instance, 2)
                case "d_minimax_medium":
                    winner = d_minimax_play(instance, 3)
                case "d_minimax_hard":
                    winner = d_minimax_play(instance, 4)
                case "o_minimax_easy":
                    winner = o_minimax_play(instance, 2)
                case "o_minimax_medium":
                    winner = o_minimax_play(instance, 3)
                case "o_minimax_hard":
                    winner = o_minimax_play(instance, 4)
                case "monte_carlo":
                    winner = monte_carlo_play(instance)

    return winner


def check_piece_selected(mouse_pos, instance):
    if instance.playing == 1:
        pieces = instance.player1
    else:
        pieces = instance.player2
    for piece_pos in pieces:
        piece_x, piece_y = piece_pos
        piece_screen_x = 550 + (piece_x * 50)
        piece_screen_y = 300 + (piece_y * 30)
        distance = math.sqrt((mouse_pos[0] - piece_screen_x)**2 + (mouse_pos[1] - piece_screen_y)**2)
        if distance < 20:
            return piece_pos
    return None

def get_clicked_position(mouse_pos):
    x = (mouse_pos[0] - 550) / 50
    y = (mouse_pos[1] - 300) / 30
    return (round(x), round(y))

# MiniMax Defensive Algorithm Gameplay
def d_minimax_play(instance, depth):
    global p1_time
    global p2_time
    time.sleep(0.2)

    start_time = time.time()

    (evaluation, best_move) = bots.minimax_defensive(instance, depth, float('-inf'), float('inf'), True)
    if best_move is None:
        print("Player ", instance.playing, " has no moves left")
        instance.winner = 1 if instance.playing == 2 else 2
        return instance.winner
    instance.update(best_move[0], best_move[1])
    print(f"Defensive Player {instance.playing} moved ", best_move[0], " to ", best_move[1], "with evaluation ", evaluation)        
    instance.swap_turn()

    end_time = time.time()
    time_taken = end_time - start_time  # Calculate the time taken to make the play
    if(instance.playing == 1):
        p2_time += time_taken
        print("Until now:", p2_time, "seconds")
    else:
        p1_time += time_taken
        print("Until now:", p1_time, "seconds")
    print("Time taken to make the play:", time_taken, "seconds")

    return instance.check_winner()

# MiniMax Offensive Algorithm Gameplay
def o_minimax_play(instance, depth):
    global p1_time
    global p2_time
    time.sleep(0.2)

    start_time = time.time()

    if instance.playing == 1:
        _, best_move = bots.minimax_offensive(instance, depth, True, -math.inf, math.inf)
    else:
        _, best_move = bots.minimax_offensive(instance, depth, False, -math.inf, math.inf)

    if best_move is None:
        print("Player ", instance.playing, " has no moves left")
        instance.winner = 1 if instance.playing == 2 else 2
        return instance.winner
    instance.update(best_move[0], best_move[1])
    print(f"Offensive Player {instance.playing} moved ", best_move[0], " to ", best_move[1], "with evaluation ", _)        
    instance.swap_turn()

    end_time = time.time()
    time_taken = end_time - start_time  # Calculate the time taken to make the play
    if(instance.playing == 1):
        p2_time += time_taken
        print("Until now:", p2_time, "seconds")
    else:
        p1_time += time_taken
        print("Until now:", p1_time, "seconds")
    print("Time taken to make the play:", time_taken, "seconds")

    return instance.check_winner()

# Random Bots Gameplay
def random_play(instance):
    global p1_time
    global p2_time
    time.sleep(0.2)

    start_time = time.time()
    
    valid_moves= [piece for piece in instance.get_all_moves()]
    if(len(valid_moves) == 0):
        print("Player ", instance.playing, " has no moves left")
        instance.winner = 1 if instance.playing == 2 else 2
        return instance.winner
    piece, move = random.choice(valid_moves)
    instance.update(piece, move)
    print(f"Random Player {instance.playing} moved ", piece, " to ", move)
    instance.swap_turn()

    end_time = time.time()
    time_taken = end_time - start_time  # Calculate the time taken to make the play
    if(instance.playing == 1):
        p2_time += time_taken
        print("Until now:", p2_time, "seconds")
    else:
        p1_time += time_taken
        print("Until now:", p1_time, "seconds")
    print("Time taken to make the play:", time_taken, "seconds")

    return instance.check_winner() 
         
# Human Player Gameplay
def human_play(instance):
    running = True
    while running:
        if(instance.get_all_moves() != []):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    winner = -1
                    print("Game ended by user")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        mouse_pos = pygame.mouse.get_pos()
                        print("Mouse position: ", mouse_pos)
                        if instance.selected_piece is None:
                            instance.selected_piece = check_piece_selected(mouse_pos, instance)
                            print("Selected piece: ", instance.selected_piece)
                            running = False
                        else:
                            clicked_pos = get_clicked_position(mouse_pos)
                            if clicked_pos in instance.get_valid_moves(instance.selected_piece):
                                instance.update(instance.selected_piece, clicked_pos)
                                instance.swap_turn()
                            instance.selected_piece = None
                            running = False
                    winner = instance.check_winner()
        else:
            winner = instance.check_winner()
            running = False
    print("Winner: ", winner)
    return winner

# Monte Carlo Gameplay
def monte_carlo_play(instance):
    global p1_time
    global p2_time
    time.sleep(0.2)

    start_time = time.time()

    root = monte_carlo.Node(instance)
    best_child = monte_carlo.monte_carlo_tree_search(root, 100)
    instance.update(best_child.move[0], best_child.move[1])
    print(f"Monte Carlo Player {instance.playing} moved ", best_child.move[0], " to ", best_child.move[1])
    instance.swap_turn()

    end_time = time.time()
    time_taken = end_time - start_time  # Calculate the time taken to make the play
    if(instance.playing == 1):
        p2_time += time_taken
        print("Until now:", p2_time, "seconds")
    else:
        p1_time += time_taken
        print("Until now:", p1_time, "seconds")
    print("Time taken to make the play:", time_taken, "seconds")

    return instance.check_winner()

menu()