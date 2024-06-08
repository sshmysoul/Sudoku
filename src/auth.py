import os
import hashlib

class Auth:
    def __init__(self, file_path='users.csv'):
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write("username,password\n")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if self.user_exists(username):
            return False, "Username already exists."
        hashed_password = self.hash_password(password)
        with open(self.file_path, 'a') as file:
            file.write(f"{username},{hashed_password}\n")
        return True, "Registration successful."

    def login(self, username, password):
        hashed_password = self.hash_password(password)
        with open(self.file_path, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == hashed_password:
                    return True, "Login successful."
        return False, "Invalid username or password."

    def user_exists(self, username):
        with open(self.file_path, 'r') as file:
            for line in file:
                stored_username, _ = line.strip().split(',')
                if stored_username == username:
                    return True
        return False
