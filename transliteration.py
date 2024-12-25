#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
transliteration.py

This file focuses solely on:
 - Limbu <-> Roman dictionaries and logic
 - Limbu <-> Devanagari dictionaries and logic (approx)
 - An offline dictionary mapping Devanagari month names to English
 - Some sample months data for demonstration
 - A test suite (using unittest) to verify everything works

You can run "python transliteration.py" to execute the tests. 
"""

import unittest
import unicodedata


# 1) FULL LIMBU→ROMAN (U+1900..U+194F)


# Base consonants
BASE_CONSONANTS_LIMBU_TO_ROMAN = {
    "\u1900": "ʔ",
    "\u1901": "ka",
    "\u1902": "kha",
    "\u1903": "ga",
    "\u1904": "gha",
    "\u1905": "nga",
    "\u1906": "ca",
    "\u1907": "cha",
    "\u1908": "ja",
    "\u1909": "jha",
    "\u190A": "nya",
    "\u190B": "ta",
    "\u190C": "tha",
    "\u190D": "da",
    "\u190E": "dha",
    "\u190F": "na",
    "\u1910": "pa",
    "\u1911": "pha",
    "\u1912": "ba",
    "\u1913": "bha",
    "\u1914": "ma",
    "\u1915": "ya",
    "\u1916": "ra",
    "\u1917": "la",
    "\u1918": "wa",
    "\u1919": "sha",
    "\u191A": "ssa",
    "\u191B": "sa",
    "\u191C": "ha",
    "\u191D": "gya",
    "\u191E": "tra",
}

# Dependent vowels
DEPENDENT_VOWELS_LIMBU_TO_ROMAN = {
    "\u1920": "a",
    "\u1921": "i",
    "\u1922": "u",
    "\u1923": "ee",
    "\u1924": "ai",
    "\u1925": "oo",
    "\u1926": "au",
    "\u1927": "e",
    "\u1928": "o",
}

# Subjoined letters
# We give subjoined RA a unique string "-rʲ" to avoid clashes with final R
SUBJOINED_LIMBU_TO_ROMAN = {
    "\u1929": "-y",
    "\u192A": "-rʲ",
    "\u192B": "-w",
}

# Final (small) consonants
# We differentiate ᤲ (U+1932) => "-ṃ" and ᤶ (U+1936) => "-m" to avoid collision
FINAL_SMALL_CONSONANTS_LIMBU_TO_ROMAN = {
    "\u1930": "-k",
    "\u1931": "-ng",
    "\u1932": "-ṃ",
    "\u1933": "-t",
    "\u1934": "-n",
    "\u1935": "-p",
    "\u1936": "-m",
    "\u1937": "-r",
    "\u1938": "-l",
}

# Limbu signs
LIMBU_SIGNS_1939_TO_1943 = {
    "\u1939": "~muk",
    "\u193A": "~kem",
    "\u193B": "~sai",
    "\u1940": "~loo",
    "\u1941": "~be",
    "\u1942": "~an",
    "\u1943": "~vis",
}

# Punctuation
PUNCTUATION_LIMBU_TO_ROMAN = {
    "\u1944": "!",
    "\u1945": "?",
}

# Digits
DIGITS_LIMBU_TO_ROMAN = {
    "\u1946": "0",
    "\u1947": "1",
    "\u1948": "2",
    "\u1949": "3",
    "\u194A": "4",
    "\u194B": "5",
    "\u194C": "6",
    "\u194D": "7",
    "\u194E": "8",
    "\u194F": "9",
}

# Merge all into one forward dictionary
LIMBU_TO_ROMAN = {}
LIMBU_TO_ROMAN.update(BASE_CONSONANTS_LIMBU_TO_ROMAN)
LIMBU_TO_ROMAN.update(DEPENDENT_VOWELS_LIMBU_TO_ROMAN)
LIMBU_TO_ROMAN.update(SUBJOINED_LIMBU_TO_ROMAN)
LIMBU_TO_ROMAN.update(FINAL_SMALL_CONSONANTS_LIMBU_TO_ROMAN)
LIMBU_TO_ROMAN.update(LIMBU_SIGNS_1939_TO_1943)
LIMBU_TO_ROMAN.update(PUNCTUATION_LIMBU_TO_ROMAN)
LIMBU_TO_ROMAN.update(DIGITS_LIMBU_TO_ROMAN)

# Build reverse dictionary (Roman->Limbu)
ROMAN_TO_LIMBU = {}

def _add_to_reverse_dict(src_dict):
    for lim_char, rom_str in src_dict.items():
        ROMAN_TO_LIMBU[rom_str] = lim_char

# We add the final+subjoined first so multi-letter combos get recognized
_add_to_reverse_dict(FINAL_SMALL_CONSONANTS_LIMBU_TO_ROMAN)
_add_to_reverse_dict(SUBJOINED_LIMBU_TO_ROMAN)
_add_to_reverse_dict(LIMBU_SIGNS_1939_TO_1943)
_add_to_reverse_dict(BASE_CONSONANTS_LIMBU_TO_ROMAN)
_add_to_reverse_dict(DEPENDENT_VOWELS_LIMBU_TO_ROMAN)
_add_to_reverse_dict(PUNCTUATION_LIMBU_TO_ROMAN)
_add_to_reverse_dict(DIGITS_LIMBU_TO_ROMAN)

# We'll match the longest Roman tokens first
ALL_ROMAN_TOKENS = sorted(ROMAN_TO_LIMBU.keys(), key=len, reverse=True)


# 2) FULL LIMBU->DEVANAGARI (approx) + REVERSE

LIMBU_TO_DEVANAGARI = {
    "\u1900": "अ़",
    "\u1901": "क",
    "\u1902": "ख",
    "\u1903": "ग",
    "\u1904": "घ",
    "\u1905": "ङ",
    "\u1906": "च",
    "\u1907": "छ",
    "\u1908": "ज",
    "\u1909": "झ",
    "\u190A": "ञ",
    "\u190B": "ट",
    "\u190C": "ठ",
    "\u190D": "ड",
    "\u190E": "ढ",
    "\u190F": "न",
    "\u1910": "प",
    "\u1911": "फ",
    "\u1912": "ब",
    "\u1913": "भ",
    "\u1914": "म",
    "\u1915": "य",
    "\u1916": "र",
    "\u1917": "ल",
    "\u1918": "व",
    "\u1919": "श",
    "\u191A": "ष",
    "\u191B": "स",
    "\u191C": "ह",
    "\u191D": "ज्ञ",
    "\u191E": "त्र",

    # dependent vowels
    "\u1920": "ा",
    "\u1921": "ि",
    "\u1922": "ु",
    "\u1923": "ी",
    "\u1924": "ै",
    "\u1925": "ू",
    "\u1926": "ौ",
    "\u1927": "े",
    "\u1928": "ो",

    # subjoined
    "\u1929": "्य",
    "\u192A": "्र",
    "\u192B": "्व",

    # finals
    "\u1930": "्क",
    "\u1931": "ङ्",
    "\u1932": "ं",
    "\u1933": "्त",
    "\u1934": "्न",
    "\u1935": "्प",
    "\u1936": "्म",
    "\u1937": "्र",
    "\u1938": "्ल",

    # signs
    "\u1939": "᤹",
    "\u193A": "᤺",
    "\u193B": "᤻",
    "\u1940": "᥀",
    "\u1941": "᥁",
    "\u1942": "᥂",
    "\u1943": "᥃",

    # punctuation
    "\u1944": "!",
    "\u1945": "?",

    # digits
    "\u1946": "०",
    "\u1947": "१",
    "\u1948": "२",
    "\u1949": "३",
    "\u194A": "४",
    "\u194B": "५",
    "\u194C": "६",
    "\u194D": "७",
    "\u194E": "८",
    "\u194F": "९",
}

DEVANAGARI_TO_LIMBU = {}
ALL_DEV_KEYS = []

def _add_dev(dev_str, lim_char):
    DEVANAGARI_TO_LIMBU[dev_str] = lim_char

for lim_char, dev_str in LIMBU_TO_DEVANAGARI.items():
    _add_dev(dev_str, lim_char)

ALL_DEV_KEYS = sorted(DEVANAGARI_TO_LIMBU.keys(), key=len, reverse=True)


# 3) OFFLINE DEVANAGARI->ENGLISH LOOKUP (MONTHS)

DEVANAGARI_TO_ENGLISH = {
    "कःकफेक्वा":  "Jan/Feb",
    "साःफेक्वा":  "Feb/Mar",
    "चेरेड्‌नाम": "Mar/Apr",
    "थेरेड्‌नाम": "Apr/May",
    "कामेःपा":    "May/Jun",
    "थकमेःपा":    "Jun/Jul",
    "सिसेःकपा":   "Jul/Aug",
    "थेसेःकपा":   "Aug/Sep",
}

def translate_devanagari_to_english(dev_word: str) -> str:
    """
    Offline dictionary for known Devanagari month => English.
    If dev_word isn't in the dictionary, we return a fallback message.
    """
    return DEVANAGARI_TO_ENGLISH.get(
        dev_word, f"No offline translation found for '{dev_word}'"
    )


# 4) TRANSLITERATION FUNCTIONS

def transliterate_limbu_to_roman(limbu_text: str, debug_log=None) -> str:
    """
    Converts Limbu text to Roman by looking up each codepoint in LIMBU_TO_ROMAN.
    If debug_log is provided as a list, we append debug info about each character.
    """
    text = unicodedata.normalize("NFC", limbu_text)
    output_chars = []
    for ch in text:
        if ch in LIMBU_TO_ROMAN:
            roman_str = LIMBU_TO_ROMAN[ch]
            if debug_log is not None:
                debug_log.append(f"Limbu char {ch} => Roman '{roman_str}'")
            output_chars.append(roman_str)
        else:
            # Unmapped: pass it through as is
            if debug_log is not None:
                debug_log.append(f"Limbu char {ch} unmapped, passing through.")
            output_chars.append(ch)
    return "".join(output_chars)

def transliterate_roman_to_limbu(roman_text: str) -> str:
    """
    Converts Roman text back into Limbu by scanning for the longest known tokens first.
    """
    text = unicodedata.normalize("NFC", roman_text)
    output_chars = []
    i = 0
    while i < len(text):
        matched = False
        for token in ALL_ROMAN_TOKENS:
            length = len(token)
            if text[i:i+length] == token:
                output_chars.append(ROMAN_TO_LIMBU[token])
                i += length
                matched = True
                break
        if not matched:
            # Not recognized, pass it through
            output_chars.append(text[i])
            i += 1
    return "".join(output_chars)

def transliterate_limbu_to_devanagari(limbu_text: str) -> str:
    """
    Converts Limbu text to approximate Devanagari, codepoint by codepoint.
    """
    text = unicodedata.normalize("NFC", limbu_text)
    output_chars = []
    for ch in text:
        if ch in LIMBU_TO_DEVANAGARI:
            output_chars.append(LIMBU_TO_DEVANAGARI[ch])
        else:
            output_chars.append(ch)
    return "".join(output_chars)

def transliterate_devanagari_to_limbu(dev_text: str) -> str:
    """
    Converts Devanagari text to Limbu by scanning for the longest known tokens.
    """
    text = unicodedata.normalize("NFC", dev_text)
    output_chars = []
    i = 0
    while i < len(text):
        matched = False
        for key in ALL_DEV_KEYS:
            length = len(key)
            if text[i:i+length] == key:
                output_chars.append(DEVANAGARI_TO_LIMBU[key])
                i += length
                matched = True
                break
        if not matched:
            # Not recognized, pass it as-is
            output_chars.append(text[i])
            i += 1
    return "".join(output_chars)


# 5) SAMPLE MONTHS DATA

MONTHS_DATA = [
    ("Jan/Feb", "ᤓᤰ᤼ᤐ᤼᥄", "कःकफेक्वा"),
    ("Feb/Mar", "ᤕᤰ᤼ᤐ᤼᥄", "साःफेक्वा"),
    ("Mar/Apr", "ᤒ᤺ᤍᤰᤐ᤼᥄", "चेरेड्‌नाम"),
    ("Apr/May", "ᤕ᤺ᤍᤰᤐ᤼᥄", "थेरेड्‌नाम"),
    ("May/Jun", "ᤗᤰᤘᤰᤙᤰ", "कामेःपा"),
    ("Jun/Jul", "ᤗᤰᤘᤰᤙᤰ", "थकमेःपा"),
    ("Jul/Aug", "ᤛᤱᤰᤙᤰ", "सिसेःकपा"),
    ("Aug/Sep", "ᤕᤱᤰᤙᤰ", "थेसेःकपा"),
]

def print_months_table():
    """
    Just a helper to print English, Limbu, Limbu->Roman, and Devanagari in a table.
    """
    print("---------------------------------------------------------")
    print(f"{'English':10} | {'Limbu':15} | {'Limbu->Roman':15} | {'Devanagari':15}")
    print("---------------------------------------------------------")
    for eng, lim, dev in MONTHS_DATA:
        roman = transliterate_limbu_to_roman(lim)
        print(f"{eng:10} | {lim:15} | {roman:15} | {dev:15}")
    print("---------------------------------------------------------")



# 6) UNIT TESTS

class TestFullExample(unittest.TestCase):
    def test_limbu_roman_round_trip(self):
        """
        Try Limbu->Roman->Limbu for all known codepoints (U+1900..U+194F).
        If two different codepoints share the same Roman, you can get conflicts.
        """
        for cp in range(0x1900, 0x1950):
            lim_char = chr(cp)
            if lim_char in LIMBU_TO_ROMAN:
                roman_str = transliterate_limbu_to_roman(lim_char)
                round_trip = transliterate_roman_to_limbu(roman_str)
                self.assertEqual(round_trip, lim_char,
                    f"Round-trip mismatch at U+{cp:04X} (Limbu->Roman->Limbu).")

    def test_devanagari_samples(self):
        """
        Quick checks: ᤁ -> क, ज्ञ -> ᤝ, etc.
        """
        # ᤁ (U+1901) => "क"
        self.assertEqual(transliterate_limbu_to_devanagari("\u1901"), "क")
        # ज्ञ => ᤝ (gya)
        self.assertEqual(transliterate_devanagari_to_limbu("ज्ञ"), "\u191D")

    def test_devanagari_offline_dictionary(self):
        """
        Confirm that known Devanagari month names map to English properly.
        """
        self.assertEqual(translate_devanagari_to_english("कःकफेक्वा"), "Jan/Feb")
        missing = translate_devanagari_to_english("randomword")
        self.assertIn("No offline translation found", missing)

    def test_months_data(self):
        """
        For each row in MONTHS_DATA, check Devanagari->English dictionary is correct.
        """
        for eng, lim, dev in MONTHS_DATA:
            self.assertEqual(translate_devanagari_to_english(dev), eng)



# MAIN (Only if you run "python transliteration.py" directly)

def main():
    # Print the table in your console
    print_months_table()

if __name__ == "__main__":
    # 1) Print table for demonstration
    main()

    # 2) Run tests
    print("\nNow running tests...\n")
    unittest.main(argv=["ignored", "-v"], exit=False)
