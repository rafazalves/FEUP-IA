import copy
import math

def minimax_defensive(instance, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or instance.check_winner() != 0:
        return instance.evaluate_defensive(), None
    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for (piece,move) in instance.get_all_moves():
            new_instance = copy.deepcopy(instance)
            new_instance.update(piece,move)
            new_instance.swap_turn()
            eval, _ = minimax_defensive(new_instance, depth - 1, alpha, beta, False)
            if eval > maxEval:
                maxEval = eval
                best_move = (piece,move)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for (piece,move) in instance.get_all_moves():
            new_instance = copy.deepcopy(instance)
            new_instance.update(piece, move)
            new_instance.swap_turn()
            eval, _ = minimax_defensive(new_instance, depth - 1, alpha, beta, True)
            if eval < minEval:
                minEval = eval
                best_move = (piece,move)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move
    

def minimax_offensive(instance, depth, maximizing_player, alpha, beta):
        if depth == 0 or instance.check_winner() != 0:
            return instance.evaluate_offensive(), None
        
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in instance.get_all_moves():
                temp_game = copy.deepcopy(instance)
                temp_game.update(move[0], move[1])
                eval, _ = minimax_offensive(temp_game, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in instance.get_all_moves():
                temp_game = copy.deepcopy(instance)
                temp_game.update(move[0], move[1])
                eval, _ = minimax_offensive(temp_game, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move