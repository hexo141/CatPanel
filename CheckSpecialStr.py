def CheckSpecialStr(s):
    special_characters = "!@#$%^&*()-+?_=,<>/"
    for char in s:
        if char in special_characters:
            return True
    return False