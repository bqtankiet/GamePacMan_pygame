#--------------------------------
# Level 1
#--------------------------------
level1 = {
    'speed': 2
}

#--------------------------------
# Level 2
#--------------------------------
level2 = {
    'speed': 3
}

#--------------------------------
# Level 3
#--------------------------------
level3 = {
    'speed': 4
}

def get_level_setting(level):
    if level == 1: return level1
    if level == 2: return level2
    if level == 3: return level3
    else: return None


if __name__ == '__main__':
    print(get_level_setting(2)['speed'])