def check_input(username, password):
    if len(username) < 3 or len(username) > 20 or len(password) < 3:
        return False
    for char in username:
        if char == " ":
            return False
    for char in password:
        if char == " ":
            return False
    return True

def string_to_list(string):
    rating_list = string.split(",")
    return rating_list