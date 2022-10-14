import re

def check_user(username, password):
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

def validate_img_type(image):
    name = image.filename
    regex = "([^\\s]+(\\.(?i)(jpe?g|png))$)"
    comp = re.compile(regex)
    if name == None:
        return False
    if re.search(comp, name):
        return True
    return False