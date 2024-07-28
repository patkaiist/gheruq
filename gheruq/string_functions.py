import re
import itertools
import sqlite3


class Roots:
    def __init__(self, attribute):
        self.segments = get_segments(attribute)
        self.alignment = root_alignment(self.segments, get_full_root(attribute))
        self.radicals = get_radicals(self.alignment, self.segments)
        self.root = "-".join(swap_ġħajn(self.radicals))


def get_segments(user_word):
    pattern = "|".join(
        map(
            re.escape,
            [
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
            ],
        )
    )
    return [segment for segment in re.split(f"({pattern})", user_word) if segment]


def remove_vowels(letters):
    vowels = {"a", "e", "i", "o", "u", "ie"}
    out = []
    for item in letters:
        if item.lower() not in vowels:
            out.append(item)
        else:
            out.append("")
    return out


def get_full_root(user_word):
    full_root = [
        item for item in remove_vowels(get_segments(user_word)) if item.strip()
    ]
    # we make an aggressively reduced root first, which we then use to work out the more likely form.
    if len(full_root) > 3:
        temp_root = (
            full_root[1:] if full_root and full_root[0] == "m" else full_root
        )  # ism mafʿūl
        if len(temp_root) > 3:
            # merge shaddah
            temp_root = [
                temp_root[i]
                for i in range(len(temp_root))
                if i == 0 or temp_root[i] != temp_root[i - 1]
            ]
            if len(temp_root) > 3:
                # remove_weak radicals
                temp_root = [
                    letter for letter in temp_root if letter.lower() not in {"w", "j"}
                ]
            full_root = temp_root
    return [item for item in full_root if item and item.strip()]


def fix_geminate_or_weak_root(input_list):
    counts = {item: input_list.count(item) for item in set(input_list)}
    if counts.get("1") == 2:
        if counts.get("2") == 1 or counts.get("4") == 1:
            replace_item = "2" if counts.get("2") == 1 else "4"
            input_list = ["1" if item == replace_item else item for item in input_list]
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

    if len(full_root) > 3 and full_root[0] in {"t", "n", "m"}:
        for i, item in enumerate(new_root):
            if item in {"t", "n", "m"}:
                new_root[i] = "3"
                break

    output_mapping = {"": "0", "3": "3", "j": "4", "ᵚ": "2"}
    output = [output_mapping.get(item, "1") for item in new_root]
    output = fix_geminate_or_weak_root(output)

    # ism al-mafʿūl / passive participle
    if output[0] == "1" and input_list[0] == "m" and full_root[0] != "m":
        output[0] = "3"

    return output


def get_radicals(aligned_root, all_segments):
    radicals = []
    for i in range(len(aligned_root)):
        if aligned_root[i] == "1":
            radicals.append(all_segments[i])
    if (aligned_root.count("1") + aligned_root.count("4")) > 3:
        if all_segments[0] == "m":
            # check for ism al-mafʿūl, but don't change anything until root_alignment()
            pass
        elif all_segments[0] == "t" or all_segments[0] == "n":
            # check for t- or n- prefix
            aligned_root[0] = "3"
        # if none of the above, then we may have a plural, so check for that.
        elif all_segments[len(all_segments) - 1] == "n":
            aligned_root[len(all_segments) - 1] = "3"
        # if still none of the above, then assume verb form VIII -t- infix
        elif all_segments[find_second(aligned_root)] == "t":
            aligned_root[find_second(aligned_root)] = "3"
    radicals = []
    for i in range(len(aligned_root)):
        if aligned_root[i] == "1":
            radicals.append(all_segments[i])
    if len(radicals) > 3:
        # no prefix detected, assuming longer root
        pass
    return radicals


def find_second(input_list):
    indices = [index for index, value in enumerate(input_list) if value == "1"]
    return indices[1] if len(indices) > 1 else -1


def get_arabic(maltese_radicals):
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
    replacement_options = [mapping.get(char, [char]) for char in maltese_radicals]
    combinations = list(itertools.product(*replacement_options))
    output_lists = [list(combination) for combination in combinations]
    return output_lists


def swap_ġħajn(input_list):
    return [item.replace("'", "ġħ") for item in input_list]


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

    return results


def ask_hans(arabic_radicals):
    # prints Arabic results assuming hanswehr.db is present
    results = isolate(arabic_radicals)
    conn = sqlite3.connect("hanswehr.db")
    output = []
    for result in results:
        result = "".join(result)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT `definition` FROM `DICTIONARY` 
            WHERE `word` LIKE ?
            LIMIT 15
        """,
            (f"%{result}%",),
        )

        rows = cursor.fetchall()
        if rows:
            output.append([" ".join(result[::-1]).replace("ك", "ک"), rows])
            return output
