
class JDMKeyboard:
    keycodes = {
        'A' : 4,
        'B' : 5,
        'C' : 6,
        'D' : 7,
        'E' : 8,
        'F' : 9,
        'G' : 10,
        'H' : 11,
        'I' : 12,
        'J' : 13,
        'K' : 14,
        'L' : 15,
        'M' : 16,
        'N' : 17,
        'O' : 18,
        'P' : 19,
        'Q' : 20,
        'R' : 21,
        'S' : 22,
        'T' : 23,
        'U' : 24,
        'V' : 25,
        'W' : 26,
        'X' : 27,
        'Y' : 28,
        'Z' : 29,
        '1' : 30,
        '2' : 31,
        '3' : 32,
        '4' : 33,
        '5' : 34,
        '6' : 35,
        '7' : 36,
        '8' : 37,
        '9' : 38,
        '0' : 39,
        'ESC' : 41,
        'SPACE': 44,
        'F1' : 58,
        'F2' : 59,
        'F3' : 60,
        'F4' : 61,
        'F5' : 62,
        'F6' : 63,
        'F7' : 64,
        'F8' : 65,
        'F9' : 66,
        'F10' : 67,
        'F11' : 68,
        'F12' : 69,
        'TAB' : 43,
        'CAPS' : 57,
        'LSHIFT' : 225,
        'LCTRL' : 224,
        'MIN' : 45,
        'ADD' : 46,
        'BACKSPAACE' : 42,
        'ENTER' : 40,
        'RSHIFT' : 229,
        'RCTRL' : 228,
    }

    @staticmethod
    def string_to_keycode(value):
        '''Convert a string to a keycode number according to the
        :attr:`Keyboard.keycodes`. If the value is not found in the
        keycodes, it will return -1.
        '''
        return JDMKeyboard.keycodes.get(value, -1)

    @staticmethod
    def keycode_to_string(value):
        '''Convert a keycode number to a string according to the
        :attr:`Keyboard.keycodes`. If the value is not found in the
        keycodes, it will return ''.
        '''
        keycodes = list(JDMKeyboard.keycodes.values())
        if value in keycodes:
            return list(JDMKeyboard.keycodes.keys())[keycodes.index(value)]
        return ''