# RACAMOJO -
# SoftDev
# P01
# 2024-12-03
# time spent: 0.5 hrs

import os

def findKey(file):
    path = os.path.join(os.getcwd(),"app/keys", file)
    with open(path, 'r') as key:
        return key.read()

googleFonts_Key = findKey("key_GoogleFonts.txt")
randomImage_Key = findKey("key_RandomImage.txt")

# print("-----")
# print(memeShow(memes))
