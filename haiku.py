#!/usr/bin/python3

from syllables import count_syllables
import sys

if __name__ == "__main__":
    words = sys.stdin.read().split()

    count = 0

    detected_first = False
    detected_second = False
    detected_third = False

    stop_point_first = 0
    stop_point_second = 0
    stop_point_third = 0

    for i, word in enumerate(words):
        syllables = count_syllables(word)
        count += syllables

        if count == 5 and not detected_first:
            count = 0
            detected_first = True
            stop_point_first = i + 1

        if count == 7 and detected_first and not detected_second:
            count = 0
            detected_second = True
            stop_point_second = i + 1

        if count == 5 and detected_first and detected_second and not detected_third:
            count = 0
            detected_third = True
            stop_point_third = i + 1
            break

    if detected_third:
        print(*words[0:stop_point_first], sep = " ")
        print(*words[stop_point_first : stop_point_second], sep = " ")
        print(*words[stop_point_second : stop_point_third], sep = " ")
    else:
        print("No haiku.")