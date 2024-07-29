import os
import platform
import random
import re

from gheruq.string_functions import (
    get_segments,
    get_full_root,
    root_alignment,
    get_radicals,
    swap_ġħajn,
    get_arabic,
    ask_hans,
)

# help message is always shown at the top of the screen
message = "Type 'help' for additional information. Leave blank for a random example."

warning = ""


def main():
    print(message)
    while True:
        user_word = input("\n> ").lower()
        user_word = user_word.replace("gh", "ġħ")
        if user_word == "q" or user_word == "quit" or user_word == "exit":
            break
        elif user_word == "clear":
            clear()
        elif user_word == "help":
            print(
                gold("\nalignment key"),
                "\n1 - primary root radical\n2 - repeated radical\n3 - non-root affix\n4 - weak root radical\n0 - non-root vowel\n",
            )
        elif user_word == "":
            analyse(
                random.choice(
                    (
                        "baġħġħad",
                        "beżżieq",
                        "daħħan",
                        "ddammem",
                        "giddieb",
                        "ħabeż",
                        "ħbejjeb",
                        "ħtalat",
                        "ltemaħ",
                        "nissieġ",
                        "qatta",
                        "settieħa",
                        "tibrid",
                        "tibżil",
                        "waħħad",
                    )
                )
            )
        else:
            analyse(user_word)


def analyse(user_word):
    clear()
    print(message)

    # separate the input based on Maltese orthography
    all_segments = get_segments(user_word)

    print(gold("\nsegments"))
    print(" ".join(all_segments))

    # generate most likely root, assuming we're after trilateral roots that may be geminate or weak
    full_root = get_full_root(user_word)

    # generate alignment list
    alignment = root_alignment(all_segments, full_root)

    # work out radicals
    radicals = get_radicals(alignment, all_segments)

    print(gold("\nlikely Maltese root"))
    print("-".join(swap_ġħajn(radicals)))
    if warning:
        print(warn(warning))

    print(gold("\nalignment"))
    # making the spacing look a little nicer, even though joining with \t would be simpler and easier
    printable_segments = ""
    gap = " "
    if "ie" in all_segments or "ġħ" in all_segments:
        gap = "  "
    for segment in all_segments:
        printable_segments += segment + (gap if len(segment) > 1 else " " + gap)
    print(printable_segments)
    print((" " + gap).join(alignment))

    print(gold("\npossible Arabic roots"))
    arabic_radicals = get_arabic(radicals)

    hans = ask_hans(arabic_radicals)

    for h in hans:
        print(blue("\n" + h[0]))
        for i, row in enumerate(h[1], start=1):
            index_str = f"{i:2}"
            print(blue(index_str) + strip_arabic(row[0][:100]))


def strip_arabic(text):
    return re.sub(
        r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB00-\uFB4F\uFE70-\uFEFF]", "", text
    )


def warn(text):
    return f"\033[31m{text}\033[0m"


def blue(text):
    return f"\033[36m{text}\033[0m"


def gold(text):
    return f"\033[33m{text}\033[0m"


def fix_geminate_or_weak_root(input_list):
    counts = {item: input_list.count(item) for item in set(input_list)}
    if counts.get("1") == 2:
        if counts.get("2") == 1 or counts.get("4") == 1:
            replace_item = "2" if counts.get("2") == 1 else "4"
            input_list = ["1" if item == replace_item else item for item in input_list]
    return input_list


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    clear()
    main()
