# configure.py: Configure credentials for gggolfclient
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu

import getpass, sys

#############################
#         SET CREDS         #
#############################

def set_creds():
    configure=True
    while configure:
        username = raw_input("Enter your memberId: ")
        password = getpass.getpass("Enter your password: ")
        location = raw_input("Enter a golf course location: ")
        name = raw_input("Enter your displayed name on gggolf: ")
        # write_creds(username, password, location, name)
        configure=query_yes_no("Would you like to reset your credentials?")


def query_yes_no(question):
    """
    Ask a yes/no question via raw_input()
    return value is True for "yes" or False for "no"
    """
    valid_ans = {"yes": True, "y": True, "no": False, "n": False}
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in valid_ans:
            return valid_ans[choice]
        else:
            sys.stdout.write("Please type 'yes' or 'no' (or 'y' or 'n').\n")