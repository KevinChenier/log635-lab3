import re


def correct_hour(text):
    if re.findall("[0-9]\s[h]", text):
        sub = re.findall("[0-9]\s[h]", text)
        x = sub[0].replace(" ", "")
        text = text[:len(text) - 3]
        text += x
    return text
