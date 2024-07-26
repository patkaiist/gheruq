import os
import platform
import re
import itertools
import sqlite3
import random

message = "Type 'help' for additional information. Leave blank for a random example."


def main():
    print(message)
    while True:
        user_word = input("> ").lower()
        user_word = user_word.replace("gh", "għ")
        if user_word == "q" or user_word == "quit" or user_word == "exit":
            break
        elif user_word == "clear":
            clear()
        elif user_word == "help":
            print("")
            print(
                gold("alignment key"),
                "\n1 - primary root radical\n2 - repeated radical (shaddah)\n3 - non-root affix\n4 - weak root radical\n0 - non-root vowel\n",
            )
        elif user_word == "":
            analyse(
                random.choice(
                    (
                        "bagħgħad",
                        "tibrid",
                        "tibżil",
                        "beżżieq",
                        "daħħan",
                        "ddammem",
                        "ħbejjeb",
                        "ħabeż",
                        "ħtalat",
                        "settieħa",
                        "giddieb",
                        "nissieġ",
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
        "għ",
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
        print(temp_root)
        if len(temp_root) > 3:
            temp_root = merge_shaddah(temp_root)
            print(temp_root)
            if len(temp_root) > 3:
                temp_root = remove_weak(temp_root)
                print(temp_root)
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
            print("-".join(swap_għajn(radicals)), warn("assuming participle"))

        # check for t- or n- prefix
        elif all_segments[0] == "t" or all_segments[0] == "n":
            print("-".join(swap_għajn(radicals)), warn("assuming binyan pattern"))

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
            "-".join(swap_għajn(radicals)),
            warn("no prefix detected, assuming longer root"),
        )
        # printed = True

    print("-".join(swap_għajn(radicals)))

    print("")
    print(gold("alignment"))
    print("\t".join(all_segments))
    print("\t".join(aligned_root))

    print("")
    print(gold("possible Arabic roots"))
    isolate(arabify(radicals))
    print("")


end = "\033[0m"


def find_second(input_list):
    count = 0
    for index, value in enumerate(input_list):
        if value == "1":
            count += 1
            if count == 2:
                return index
    return -1


def warn(text):
    start = "\033[31m"
    return f"{start}{text}{end}"


def blue(text):
    start = "\033[36m"
    return f"{start}{text}{end}"


def gold(text):
    start = "\033[33m"
    return f"{start}{text}{end}"


def mediopassive():
    # ltemaħ
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
        "għ": "ع|غ",
        "ġħ": "ع|غ",
        "g": "قَ|ك",
        "d": "ض|د|ذ",
        "b": "ب",
        "s": "س",
        "l": "ل",
        "k": "ك",
        "'": "ى|ي",
        "n": "ن",
        "t": "ط|ت",
        "q": "ق",
        "r": "ر",
        "m": "م",
        "ħ": "ح|خ",
        "x": "ش",
        "j": "ي",
        "ż": "ز",
        "ġ": "ج",
    }

    def replace_match(match):
        return mapping.get(match.group(0), match.group(0))

    def replace_in_string(text):
        for key in mapping:
            pattern = re.compile(re.escape(key))
            text = pattern.sub(replace_match, text)
        return text

    output_list = [replace_in_string(item) for item in input_list]

    return output_list


def swap_għajn(input):
    output = []
    for item in input:
        output.append(item.replace("'", "għ"))
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


def isolate(input_string):
    split_data = [item.split("|") for item in input_string]
    combinations = itertools.product(*split_data)
    results = ["".join(combination) for combination in combinations]
    # geminate roots are still done in Maltese as the full three letters,
    # but not in Arabic, so we create truncated forms for Hans.
    new_results = []
    for result in results:
        new_results.append(result)
        new = ""
        new += result[0]
        for i in range(1, len(result)):
            if result[i] != result[i - 1]:
                new += result[i]
        new_results.append(new)
    results = list(set(new_results))

    conn = sqlite3.connect("hanswehr.sqlite")
    for result in results:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT `definition`, `id` FROM `DICTIONARY` 
            WHERE `word` LIKE ?
            LIMIT 10
        """,
            (f"%{result}%",),
        )

        rows = cursor.fetchall()
        if len(rows) > 0:
            print("")
            print(blue(" ".join(result[::-1]).replace("ك", "ک")))
            i = 1
            for row in rows:
                print(blue(i), gold(row[1]), strip_arabic(row[0][:100]))
                i += 1


if __name__ == "__main__":
    clear()
    main()
