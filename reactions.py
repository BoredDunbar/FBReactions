# Script for extracting usernames from Reactions pop-up window on Facebook po
# using Copy All Links Firefox add-on
# Version 1.0

import re
import os
import tkinter as tk
import json

# Url parameters associated with reactions pop-up window
reaction_parameter = "fref=pb&hc_location=profile_browser"

# Links are either FB username or user ID
profile_url_1 = "www.facebook.com/"
profile_url_2 = "www.facebook.com/profile.php?id="


# Clear console screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Print ASCII art header
def print_header():
    print("  ______ ____    _____                 _   _ ")
    print(" |  ____|  _ \  |  __ \               | | (_) ")
    print(" | |__  | |_) | | |__) |___  __ _  ___| |_ _  ___  _ __  ___  ")
    print(" |  __| |  _ <  |  _  // _ \/ _` |/ __| __| |/ _ \| '_ \/ __| ")
    print(" | |    | |_) | | | \ \  __/ (_| | (__| |_| | (_) | | | \__ \ ")
    print(" |_|    |____/  |_|  \_\___|\__,_|\___|\__|_|\___/|_| |_|___/ ")
    print()
    print()


# Get content from clipboard that was copied using "Copy all links"
def get_clipboard_content():
    root = tk.Tk()
    # hide window
    root.withdraw()
    return root.clipboard_get()


# Returns a list of dict elements with {date: username list} structure
def get_reactions():
    users = []
    reactions = {}

    print("Enter Post Date / Description (must be unique):")
    reaction_date = input()
    print("Copy links and Press Y")
    link_answer = input()
    link_text = ""
    if link_answer.upper() == "Y":
        try:
            link_text = get_clipboard_content()
        except:
            print("Something went wrong")

    link_list = link_text.split("https://")
    for line in link_list:
        line == line.rstrip()

        # Look for url paramater associated with a reaction
        if re.search(reaction_parameter, line):
            # Conditional to take into account FB profile name vs user id number
            if line.startswith(profile_url_2):
                start = 32
                end = line.find("&fref")
            elif line.startswith(profile_url_1):
                start = 17
                end = line.find("?")
            username = line[start:end]
            users.append(username)

    reactions = {reaction_date: users}
    clear()
    return reactions


# Save Dict item to a text file in json format
def save_json(reaction_dict, filename):
    with open(filename, 'w') as outfile:
        json.dump(reaction_dict, outfile)


# Main program
print_header()
scraping = True
reaction_dict = {}
while scraping:
    reaction_dict.update(get_reactions())
    print_header()
    print("Reactions:")
    print()
    print(reaction_dict)
    print()
    print("Continue? Y/N")
    answer = input()
    if answer.upper() != "Y":
        scraping = False
        print('Enter new filename: (example.txt)')
        filename = input()
        save_json(reaction_dict, filename)
        print("JSON file saved")
        print("Press Enter to exit")
        input()





