import random
import time
import csv
import os
from auth import Auth
import getpass


class Sudoku:
    def __init__(self):
        self.board = self.generate_sudoku()
        self.solution = [row[:] for row in self.board]
        self.solve(self.solution)

    def print_board(self):
        # Print column indices
        print("    1 2 3   4 5 6   7 8 9")
        print("  +-------+-------+-------+")
        for i, row in enumerate(self.board):
            # Print row indices and separator lines
            if i % 3 == 0 and i != 0:
                print("  +-------+-------+-------+")
            print(f"{i+1} |", end=" ")
            for j, num in enumerate(row):
                # Print vertical separators
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                # Print numbers or spaces
                print(str(num) if num != 0 else '.', end=" ")
            print("|")
        print("  +-------+-------+-------+")

    def is_valid(self, board, row, col, num):
        # Check row and column, excluding the current position
        for i in range(9):
            if board[row][i] == num and i != col:
                return False
            if board[i][col] == num and i != row:
                return False

        # Calculate the starting position of the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)

        # Check the 3x3 grid, excluding the current position
        for i in range(3):
            for j in range(3):
                if (start_row + i != row or start_col + j != col) and board[start_row + i][start_col + j] == num:
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
        count = random.randint(1, 3)  # Adjusted to make a solvable puzzle
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0
            count -= 1

    def get_hint(self, row, col):
        if self.board[row][col] == 0:
            return self.solution[row][col]
        else:
            return None

    def get_user_solution(self):
        # Copy the board
        user_board = [row[:] for row in self.board]
        print("📝 Enter your solution by specifying the 'row col number' (e.g '1 1 5'), AND start from 1")
        print("✅ Enter 'done' to finish")
        print("💡 Enter 'hint row col' for a hint")
        print("🚪 Enter 'quit' to leave this game")        
        any_input = False
        while True:
            try:
                user_input = input("Enter row, column, answer : ").strip()
                if user_input.lower() == 'quit':
                    print("🚪 Exiting the game. Goodbye!")
                    exit()
                if user_input.lower() == 'done':
                    break
                if user_input.lower().startswith('hint'):
                    _, row, col = user_input.split()
                    row, col = int(row) - 1, int(col) - 1
                    if not (0 <= row < 9 and 0 <= col < 9):
                        raise ValueError("Row and col number must be between 1 and 9.")
                    hint = self.get_hint(row, col)
                    if hint is not None:
                        print(f"💡 Hint: At row {row+1}, column {col+1}, the correct number is {hint}")
                    else:
                        print("⚠️ Smart ShawnD cannot provide a hint for a pre-filled position, if you even need this one, don't do this.")
                    continue
                row, col, num = map(int, user_input.split())
                if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9):
                    raise ValueError("Row, col, and number must be between 1 and 9.")
                if self.board[row-1][col-1] != 0:
                    raise ValueError("You cannot change the given numbers.")
                if not self.is_valid(user_board, row-1, col-1, num):
                    raise ValueError("The number is not valid for this position.")
                user_board[row-1][col-1] = num
                any_input = True
            except ValueError as e:
                print(f"❌ Invalid input: {e}, please try again")
        if any_input:
            return user_board
        else:
            print("Please don't input 'done' directly. If you want to exit, input 'done' again or type to continue.")
            return self.get_user_solution()

    def check_solution(self, user_board):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    if not self.is_valid(user_board, i, j, user_board[i][j]):
                        return False
        return self.solve(user_board)

def main():
    auth = Auth()
    
    print("🎮 Welcome to Sudoku Game!")
    while True:
        choice = input("❓ Do you have an account? (yes/no): ").strip().lower()
        if choice == 'no':
            username = input("🆕 Enter a new username: ").strip()
            if auth.user_exists(username):
                print("❌ Username already exists.")
                continue
            while True:
                password = getpass.getpass("🔐 Enter a new password ( Use SHA-256 to protect your data) : ").strip()
                confirm_password = getpass.getpass("🔐 Confirm your password: ").strip()
                if password == confirm_password:
                    break
                else:
                    print("❌ Passwords do not match. Please try again.")
            success, message = auth.register(username, password)
            print(message)
            if success:
                break
        elif choice == 'yes':
            username = input("🖊️ Enter your username: ").strip()
            password = getpass.getpass("🔑 Enter your password: ").strip()
            success, message = auth.login(username, password)
            print(message)
            if success:
                break
        else:
            print("Invalid choice, please enter 'yes' or 'no'.")

    sudoku = Sudoku()
    print("📋 Generated Sudoku Board:")
    sudoku.print_board()

    # Record start time
    start_time = time.time()

    # Get user solution
    print("\nEnter your solution for the Sudoku:")
    user_solution = sudoku.get_user_solution()

    # Record end time
    end_time = time.time()
    total_time = end_time - start_time

    # Check user solution
    if sudoku.check_solution(user_solution):
        print("\n🎉 Your solution is correct!")
        print(f"⏱️ Time taken to solve the Sudoku: {total_time:.2f} seconds")

        csv_file = "sudoku_times.csv"
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Username", "Time taken (seconds)"])
            writer.writerow([username, total_time])

        # Compare highest point
        times = []
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                times.append((row[0], float(row[1])))

        if times:
            best_time = min(times, key=lambda x: x[1])
            print(f"\n⏱️ Your time: {total_time:.2f} seconds")
            print(f"🏆 Best time: {best_time[1]:.2f} seconds by {best_time[0]}")
        else:
            print("\nNo previous times to compare.")
    else:
        print("\n❌ Your solution is incorrect.")
        print(f"\n⏱️ Your time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
