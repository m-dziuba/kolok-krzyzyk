import random


def comp_reaction(board_list, pos_index_list, tic_tac_toe_list):
    print("COMPUTERS MOVE:")
    x_count = 0
    for place in board_list:
        if place == "X":
            x_count += 1

    if x_count == 1:
        if any(board_list[i] == "X" for i in (0, 8)):
            board_list[4] = "O"
        else:
            for i in (1, 2, 3, 4, 5, 6, 7):
                if board_list[i] == "X":
                    board_list[i * 2 - 8 * (i//5)] = "O"
    else:
        if not counter_or_winning_move(board_list, "O"):
            if not counter_or_winning_move(board_list, "X"):
                check_special_cases(board_list)

    print_board(board_list, pos_index_list, tic_tac_toe_list)


def get_methods_for_orientations():
    return [(lambda i, j: i + 3 * j, range(3), range(3), range(3)),
            (lambda i, j: i * 3 + j, range(3), range(3), range(3)),
            (lambda i, j: i * (4 - j) + j, range(3), (0, 2), range(2))]


def counter_or_winning_move(board_list, x_or_o):
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
                            if board_list[positional_index[m][0]] == " ":
                                board_list[positional_index[m][0]] = "O"
                                return True
    return False


def check_win_condition(board_list, x_or_o):
    method_for_each_orientation = get_methods_for_orientations()
    for expression in method_for_each_orientation:
        i_range, j_range, m_range = expression[1:4]
        checked_lines = [[board_list[expression[0](i, j)] for i in i_range] for j in j_range]

        for m in m_range:
            if all(checked_lines[m][n] == x_or_o for n in range(3)):
                print("You win!!" if x_or_o == "X" else "You lose :(")
                return True

    if all(board_list[i] != " " for i in range(9)):
        print("Draw")
        return True
    else:
        return False


def check_special_cases(board_list):
    if board_list[4] == " ":
        board_list[4] = "O"
        return True
    elif any(board_list[i] == "X" and board_list[j] == "X" for i in (0, 2, 6, 8) for j in (1, 3, 5, 7)):
        for i in (0, 2, 6, 8):
            for j in (1, 3, 5, 7):
                if board_list[i] == "X" and board_list[j] == "X" and board_list[(i + 2 * j) - 8] == " ":
                    board_list[(i + 2 * j) - 8] = "O"
                    return True
    elif board_list[0] == "X" and board_list[4] == "X" and board_list[2] == " ":
        board_list[2] = "O"
        return True
    elif any(board_list[i * 2] == "X" and board_list[8 - (i * 2)] == "X" for i in range(2)):
        for i in range(2):
            if board_list[i * 2] == "X" and board_list[8 - (i * 2)] == "X":
                board_list[random.choice((1, 3, 5, 7))] = "O"
                return True
    return False


def players_choice(_input, board_list, pos_index_list, tic_tac_toe_list):
    if board_list[int(_input) - 1] == " ":
        board_list[int(_input) - 1] = "X"
        print("YOUR MOVE:")
        print_board(board_list, pos_index_list, tic_tac_toe_list)
        return True
    else:
        print_board(board_list, pos_index_list, tic_tac_toe_list)
        print("!!! You can't place your cross there !!!")
        return False


def print_board(board_list, pos_index_list, tic_tac_toe_list):
    for i in range(len(tic_tac_toe_list)):
        if i in pos_index_list:
            for j in range(len(pos_index_list)):
                if i == pos_index_list[j]:
                    tic_tac_toe_list[i] = board_list[j]
        else:
            tic_tac_toe_list[i] = tic_tac_toe_list[i]
    print("".join(char for char in tic_tac_toe_list))


def setup():
    tic_tac_toe_list = []
    i_count = 0
    for i in range(1, 133):
        if i % 12 == 0:
            i_count += 1
            tic_tac_toe_list.append("\n")
        elif (i_count + 1) % 4 == 0 and i_count != 0:
            tic_tac_toe_list.append("-")
        elif (i - 4) % 12 == 0 or (i - 8) % 12 == 0:
            tic_tac_toe_list.append("|")
        else:
            tic_tac_toe_list.append(" ")
    pos_index_list = [13, 17, 21, 61, 65, 69, 109, 113, 117]
    board_list = [tic_tac_toe_list[index] for index in pos_index_list]
    return tic_tac_toe_list, board_list, pos_index_list


if __name__ == '__main__':
    tic_tac_toe, board, important_positions_indexes = setup()
    print("".join(char for char in tic_tac_toe))
    while True:
        user_input = input("Choose a number from 1 to 9: ")
        if user_input == "exit":
            break
        elif user_input == "":
            continue
        else:
            if players_choice(user_input, board, important_positions_indexes, tic_tac_toe):
                if check_win_condition(board, "X"):
                    tic_tac_toe, board, important_positions_indexes = setup()
                else:
                    comp_reaction(board, important_positions_indexes, tic_tac_toe)
                    if check_win_condition(board, "O"):
                        tic_tac_toe, board, important_positions_indexes = setup()

# todo Error handling
# TODO posprzątać, może skrócić