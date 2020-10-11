
# VERY SIMPLE PROGRAM
# Masks a message by adding a given number to each letter in the string.
# [USAGE 1] To add 2 to every letter in a message string.
#           m = 'some message string'
#           addToEveryLetter(m, 2)
# [USAGE 2] To unmask the previous message, just add -2.
#           m = '<this string would look like gibberish>'
#           addToEveryLetter(m, -2)
def addToEveryLetter(sentence, num):
    result = ''
    for letter in sentence:
        N = ord(letter)
        N += num
        NewLetter = chr(N)
        result += NewLetter
    return result