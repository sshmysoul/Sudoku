def is_valid(board,row,col,num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[col][i] == num:
            return False
    start_row , start_col = 3 * (num//3),3*(col//3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
            
