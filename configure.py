# configure.py: Configure credentials for gggolfclient
#!/usr/bin/env python
# 
# (C) Copyright 2018-2019 Yu-Yueh Liu

import getpass, sys, os, re

#############################
#         SET CREDS         #
#############################

def set_creds():
    configure=True
    
    while configure:
        exists = os.path.isfile('./credentials_info.py')
        username=password=location=name=userHolder=passHolder=locHolder=nameHolder=""
        if exists:
            f = open('./credentials_info.py', 'r+')
            for line in f:
                val=re.findall(r"['\"](.*?)['\"]", line.rstrip())     
                if len(val)==0:
                    continue
                else:
                    val=val[0]

                if line.startswith('location'):
                    location=val
                    locHolder=" ["+val+"]"
                    continue
                if line.startswith('name'):
                    name=val
                    nameHolder=" ["+val+"]"
                    continue
            
                stars=printstars(val)
                if line.startswith('username'):
                    username=val
                    userHolder=" ["+stars+val[-2:]+"]"
                    continue
                if line.startswith('password'):
                    password=val
                    passHolder=" ["+stars+val[-2:]+"]"
                    continue 
            f.close()               
            f = open('./credentials_info.py', 'w')
        else:
            f = open('./credentials_info.py', 'w+')

        username = raw_input("Enter your memberId"+userHolder+": ") or username
        password = getpass.getpass("Enter your password"+passHolder+": ") or password
        location = raw_input("Enter a golf course location"+locHolder+": ") or location
        name = raw_input("Enter your displayed name on gggolf"+nameHolder+": ") or name
        f.write("# These are your credentials to log on to secure GGGolf\n\n")
        f.write("username"+" = '"+username+"'\n")
        f.write("password"+" = '"+password+"'\n")
        f.write("location"+" = '"+location+"'\n")
        f.write("name"+" = '"+name+"'\n")
        f.write("base_url"+" = 'https://secure.gggolf.ca/"+location+"/'\n")
        f.close()
        configure=query_yes_no("Would you like to re-enter your credentials?")
        sys.stdout.write("\n\n")
    sys.stdout.write("Your Credentials are set! You are ready to use gggolfclient now.\n\n")


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


def printstars(string):
    star=""
    for _ in range(len(string)-2):
        star+="*"
    return star