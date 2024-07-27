import os
import platform
import re
import itertools
import sqlite3
import random

# help message is always shown at the top of the screen
message = "Type 'help' for additional information. Leave blank for a random example."

# to do:
# - waħdanija <n> isn't handled

def main():
    print(message)
    while True:
        user_word = input("> ").lower()
        user_word = user_word.replace("gh", "ġħ")
        if user_word == "q" or user_word == "quit" or user_word == "exit":
            break
        elif user_word == "clear":
            clear()
        elif user_word == "help":
            print("")
            print(
                gold("alignment key"),
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
    delimiters = [
        "ġħ",
        "ie",
        "a",
        "b",
        "ċ",
        "d",
        "e",
        "f",
        "g",
        "ġ",
        "h",
        "ħ",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "z",
        "ż",
    ]
    pattern = "|".join(map(re.escape, delimiters))
    all_segments = re.split(f"({pattern})", user_word)
    all_segments = [item for item in all_segments if item]

    print("")
    print(gold("segments"))
    print(" ".join(all_segments))

    # generate most likely root, assuming we're after trilateral roots that may be geminate or weak
    full_root = remove_vowels(all_segments)
    full_root = [item for item in full_root if item and item.strip()]

    # we make an aggressively reduced root first, which we then use to work out the more likely form.
    if len(full_root) > 3:
        temp_root = mark_passive_participle(full_root)  # ism mafʿūl
        if len(temp_root) > 3:
            temp_root = merge_shaddah(temp_root)
            if len(temp_root) > 3:
                temp_root = remove_weak(temp_root)
            full_root = temp_root

    full_root = [item for item in full_root if item and item.strip()]

    # generate alignment list
    aligned_root = root_alignment(all_segments, full_root)

    radicals = []
    for i in range(len(aligned_root)):
        if aligned_root[i] == "1":
            radicals.append(all_segments[i])

    if (aligned_root.count("1") + aligned_root.count("4")) > 3:

        # check for ism ma
        if all_segments[0] == "m":
            print(warn("assuming participle"))

        # check for t- or n- prefix
        elif all_segments[0] == "t" or all_segments[0] == "n":
            print(warn("assuming binyan pattern"))
            aligned_root[0] = "3"
            type = "b"

        # if none of the above, then we may have a plural, so check for that.
        elif all_segments[len(all_segments) - 1] == "n":
            print(warn("probable plural"))
            aligned_root[len(all_segments) - 1] = "3"

        # if still none of the above, then assume verb form VIII -t- infix
        elif all_segments[find_second(aligned_root)] == "t":
            print(warn("probable mediopassive"))
            aligned_root[find_second(aligned_root)] = "3"

    radicals = []
    for i in range(len(aligned_root)):
        if aligned_root[i] == "1":
            radicals.append(all_segments[i])

    print("")
    print(gold("likely Maltese root"))
    if len(radicals) > 3:
        print(
            "-".join(swap_ġħajn(radicals)),
            warn("no prefix detected, assuming longer root"),
        )
    print("-".join(swap_ġħajn(radicals)))

    print("")
    print(gold("alignment"))
    # making the spacing look a little nicer, even though joining with \t would be simpler and easier
    printable_segments = ""
    gap = " "
    if "ie" in all_segments or "ġħ" in all_segments:
        gap = "  "
    for segment in all_segments:
        printable_segments += segment + (gap if len(segment) > 1 else " " + gap)
    print(printable_segments)
    print((" " + gap).join(aligned_root))

    print("")
    print(gold("possible Arabic roots"))
    isolate(arabify(radicals))
    print("")


def find_second(input_list):
    count = 0
    for index, value in enumerate(input_list):
        if value == "1":
            count += 1
            if count == 2:
                return index
    return -1


def warn(text):
    return f"\033[31m{text}\033[0m"


def blue(text):
    return f"\033[36m{text}\033[0m"


def gold(text):
    return f"\033[33m{text}\033[0m"


def mediopassive():
    pass


def mark_passive_participle(input_list):
    if not input_list:
        return []
    new_list = []
    if input_list[0] == "m":
        for i in range(1, len(input_list)):
            new_list.append(input_list[i])
        return new_list
    else:
        return input_list


def merge_shaddah(input_list):
    if not input_list:
        return []
    new_list = [input_list[0]]

    for i in range(1, len(input_list)):
        if input_list[i] != input_list[i - 1]:
            new_list.append(input_list[i])
    return new_list


def fix_geminate_or_weak_root(input_list):
    # for roots which only have 1 letters but then detected repetition of one, assume it's a geminate root
    if input_list.count("1") == 2 and input_list.count("2") == 1:
        for i in range(len(input_list)):
            if input_list[i] == "2":
                input_list[i] = "1"
                breakpoint
    if input_list.count("1") == 2 and input_list.count("4") == 1:
        for i in range(len(input_list)):
            if input_list[i] == "4":
                input_list[i] = "1"
                breakpoint
    return input_list


def root_alignment(input_list, full_root):
    def remove_internal_vowels(s):
        return "".join(char for char in s if char not in "aeiou")

    root = [remove_internal_vowels(item) for item in input_list]

    new_root = [root[0]]
    for i in range(1, len(root)):
        if root[i] != root[i - 1]:
            new_root.append(root[i])
        else:
            new_root.append("ᵚ")

    if len(full_root) > 3:
        if full_root[0] == "t" or full_root[0] == "n" or full_root[0] == "m":
            for i, item in enumerate(new_root):
                if item == "t" or item == "n" or item == "m":
                    new_root[i] = "3"
                    break

    output_mapping = {"": "0", "3": "3", "j": "4", "ᵚ": "2"}
    output = [output_mapping.get(item, "1") for item in new_root]
    output = fix_geminate_or_weak_root(output)

    # ism al-mafʿūl / passive participle
    if output[0] == "1" and input_list[0] == "m" and full_root[0] != "m":
        output[0] = "3"

    return output


def remove_weak(letters):
    vowels = {"w", "j"}
    return [letter for letter in letters if letter.lower() not in vowels]


def remove_vowels(letters):
    vowels = {"a", "e", "i", "o", "u", "ie"}
    out = []
    for item in letters:
        if item.lower() not in vowels:
            out.append(item)
        else:
            out.append("")
    return out  # [letter for letter in letters if letter.lower() not in vowels]


def arabify(input_list):
    mapping = {
        "ġħ": ["ع", "غ"],
        "'": ["ى", "ي", "ع"],
        "b": ["ب"],
        "d": ["ض", "د", "ذ"],
        "ġ": ["ج"],
        "g": ["قَ", "ك"],
        "ħ": ["ح", "خ"],
        "h": ["ه"],
        "j": ["ي"],
        "k": ["ك"],
        "l": ["ل"],
        "m": ["م"],
        "n": ["ن"],
        "q": ["ق"],
        "r": ["ر"],
        "s": ["س"],
        "t": ["ط", "ت", "ﺙ"],
        "w": ["و", "ﻭ"],
        "x": ["ش"],
        "ż": ["ز"],
    }

    replacement_options = [mapping.get(char, [char]) for char in input_list]
    combinations = list(itertools.product(*replacement_options))
    output_lists = [list(combination) for combination in combinations]

    return output_lists


def swap_ġħajn(input):
    output = []
    for item in input:
        output.append(item.replace("'", "ġħ"))
    return output


def strip_arabic(text):
    arabic_pattern = re.compile(
        "[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB00-\uFB4F\uFE70-\uFEFF]"
    )
    return arabic_pattern.sub("", text)


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def isolate(input_lists):
    results = []
    seen = set()

    for result in input_lists:
        sublist_tuple = tuple(result)
        if sublist_tuple not in seen:
            results.append(result)
            seen.add(sublist_tuple)
        # geminate roots in Arabic occur as AB in the Hans Wehr,
        # not A-B-B as in Maltese, so we need to account for those
        if len(result) > 2 and result[1] == result[2]:
            reduced_result = [result[0], result[1]]
            reduced_tuple = tuple(reduced_result)
            if reduced_tuple not in seen:
                results.append(reduced_result)
                seen.add(reduced_tuple)

    conn = sqlite3.connect("hanswehr.sqlite")
    for result in results:
        result = "".join(result)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT `definition` FROM `DICTIONARY` 
            WHERE `word` LIKE ?
            LIMIT 5
        """,
            (f"%{result}%",),
        )

        rows = cursor.fetchall()

        if len(rows) > 0:
            print("")
            print(blue(" ".join(result[::-1]).replace("ك", "ک")))
            i = 1
            for row in rows:
                e = str(i) + " "
                if i < 10:
                    e = e + " "
                print(blue(e) + strip_arabic(row[0][:100]))
                i += 1


if __name__ == "__main__":
    clear()
    main()
