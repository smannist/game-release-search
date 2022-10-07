def check_input(username, password):
    for char in username:
        if char == " " or len(username) < 3 or len(username) > 20:
            return False
    for char in password:
        if char == " " or len(password) < 3:
            return False
    return True