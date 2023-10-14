def return_filename(string):
    i = -1
    while string[i] != '/':
        i -= 1
    return string[i + 1:len(string)]
