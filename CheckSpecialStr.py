def CheckSpecialStr(s):
    special_characters = "!@#$%^&*()-+?=,<>/"
    for char in s:
        if char in special_characters:
            return True
    return False