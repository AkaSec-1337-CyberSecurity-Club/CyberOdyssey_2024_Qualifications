from string import ascii_letters, digits

print('''
###################################################################
#                                                                 #
#   Welcome to pyJail!                                            #
#                                                                 #
#   You have been jailed for using alphanumerics and underscores  #
#                                                                 #
#   Your goal is to break free from this jail.                    #
#                                                                 #
#   If you manage to break free, you will get the flag.           #
#                                                                 #
###################################################################\n''')

code = input('> ')

if any(c in ascii_letters + digits for c in code) or ('__' in code):
    print('No hacking!')
    exit()

eval(code, {'__builtins__': None}, {'__builtins__': None})