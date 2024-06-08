import random
import time
import csv
import os
class Sudoku:
    def __init__(self):
        self.board = self.generate_sudoku()

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def generate_sudoku(self):
        board = [[0]*9 for _ in range(9)]
        self.fill_diagonal(board)
        self.fill_remaining(board, 0, 3)
        self.remove_elements(board)
        return board

    def fill_diagonal(self, board):
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)
    
    def fill_box(self, board, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()

    def fill_remaining(self, board, row, col):
        if col >= 9 and row < 8:
            row += 1
            col = 0
        if row >= 9 and col >= 9:
            return True
        if row < 3:
            if col < 3:
                col = 3
        elif row < 6:
            if col == int(row / 3) * 3:
                col += 3
        else:
            if col == 6:
                row += 1
                col = 0
                if row >= 9:
                    return True
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.fill_remaining(board, row, col + 1):
                    return True
                board[row][col] = 0
        return False

    def remove_elements(self, board):
        count = random.randint(1,2)
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0
            count -= 1

    def get_user_solution(self):
        user_board = [row[:] for row in self.board]
        for i in range(9):
            while True:
                try:
                    row = input(f"Enter row {i + 1} (use space to separate numbers, use 0 for empty cells): ").split()
                    if len(row) != 9:
                        raise ValueError("Each row must contain exactly 9 numbers.")
                    for j in range(9):
                        user_board[i][j] = int(row[j])
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please try again.")
        return user_board

    def check_solution(self, user_board):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and not self.is_valid(user_board, i, j, user_board[i][j]):
                    return False
        return self.solve(user_board)

# Create Sudoku instance and print the generated board
sudoku = Sudoku()
print("Generated Sudoku Board:")
sudoku.print_board()

#record start  time func
start_time =time.time()

# Get user solution
print("\nEnter your solution for the Sudoku:")
user_solution = sudoku.get_user_solution()

#record end time
end_time = time.time()

# Check user solution
if sudoku.check_solution(user_solution):
    print("\nYour solution is correct!")
else:
    print("\nYour solution is incorrect.")

total_time = end_time - start_time
print(f"\nTime taken to solve the Sudoku: {total_time:.2f} seconds")

csv_file = "sudoku_times.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file,mode='a',newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Time taken (seconds)"])
        writer.writerow([total_time])

#compare highest point
times = []
with open(csv_file,mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        times.append(float(row[0]))
if times:
    best_time = min(times)
    print(f"\nBest time is : {best_time: .2f} seconds")
else:
    print(f"\nBro here is no previous time to compare")

"""
#这是可选的，是否打印全部的游戏时间
print("\nAll recorded times are : " )
for idx,time_taken in enumerate(times,start = 1):
    print(f"{idx}. {time_taken = .2f} seconds")"""