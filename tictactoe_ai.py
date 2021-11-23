import random


def comp_reaction(board_list, player, computer):
    new_board = []
    for i in range(3):
        for j in range(3):
            new_board.append(board_list[i][j])

    x_count = 0
    for place in new_board:
        if place == player:
            x_count += 1

    if x_count <= 1:
        if any(new_board[i] == player for i in (0, 8)):
            new_board[4] = computer
        else:
            for i in (1, 2, 3, 4, 5, 6, 7):
                if new_board[i] == player:
                    new_board[i * 2 - 8 * (i//5)] = computer
    else:
        if not counter_or_winning_move(new_board, computer, computer):
            if not counter_or_winning_move(new_board, player, computer):
                check_special_cases(new_board, player, computer)

    board_list = [[new_board[i + 3 * j] for i in range(3)] for j in range(3)]
    return board_list


def get_methods_for_orientations():
    return [(lambda i, j: i + 3 * j, range(3), range(3), range(3)),
            (lambda i, j: i * 3 + j, range(3), range(3), range(3)),
            (lambda i, j: i * (4 - j) + j, range(3), (0, 2), range(2))]


def counter_or_winning_move(board_list, x_or_o, computer):
    pos_index_list = [i for i in range(9)]
    method_for_each_orientation = get_methods_for_orientations()

    for expression in method_for_each_orientation:
        i_range, j_range, m_range = expression[1:4]
        checked_lines = [[board_list[expression[0](i, j)] for i in i_range] for j in j_range]
        positional_index = [[pos_index_list[expression[0](i, j)] for i in i_range] for j in j_range]

        if any(checked_lines[m][n] == x_or_o and checked_lines[m][o] == x_or_o
               for m in m_range for n in range(0, 2) for o in range(1, 3) if n != o):
            for m in m_range:
                for n in range(0, 2):
                    for o in range(1, 3):
                        if checked_lines[m][n] == x_or_o and checked_lines[m][o] == x_or_o and n != o:
                            del positional_index[m][o], positional_index[m][n]
                            if board_list[positional_index[m][0]] == 0:
                                board_list[positional_index[m][0]] = computer
                                return True
    return False


def check_special_cases(board_list, player, computer):
    if board_list[4] == 0:
        board_list[4] = computer
        return True
    elif any(board_list[i] == player and board_list[j] == player for i in (0, 2, 6, 8) for j in (1, 3, 5, 7)):
        for i in (0, 2, 6, 8):
            for j in (1, 3, 5, 7):
                if (i + 2 * j) - 8 in (0, 2, 4, 6, 8):
                    if board_list[i] == player and board_list[j] == player and board_list[(i + 2 * j) - 8] == 0:
                        board_list[(i + 2 * j) - 8] = computer
                        return True
    elif board_list[0] == player and board_list[4] == player and board_list[2] == 0:
        board_list[2] = computer
        return True
    elif any(board_list[i * 2] == player and board_list[8 - (i * 2)] == player for i in range(2)):
        for i in range(2):
            if board_list[i * 2] == player and board_list[8 - (i * 2)] == player:
                board_list[random.choice((1, 3, 5, 7))] = computer
                return True
    return False


if __name__ == '__main__':
    pass
    # while True:
    #     user_input = input("Choose a number from 1 to 9: ")
    #     if user_input == "exit":
    #         break
    #     elif user_input == "":
    #         continue
    #     else:
    #         if players_choice(user_input, board):
    #             if check_win_condition(board, 1):
    #                 new_board = [0 for i in range(9)]
    #             else:
    #                 comp_reaction(board)
    #                 if check_win_condition(board, 2):
    #                     new_board = [0 for i in range(9)]
    #
