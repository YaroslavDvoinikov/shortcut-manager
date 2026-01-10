from pynput.keyboard import Key, KeyCode


def normalize_key(key):
    if key in (Key.ctrl_l, Key.ctrl_r):
        return "Ctrl"
    if key in (Key.shift, Key.shift_l, Key.shift_r):
        return "Shift"
    if key in (Key.alt_l, Key.alt_r, Key.alt_gr):
        return "Alt"
    if key == Key.cmd:
        return "Meta"

    special_keys = {
        Key.space: "Space",
        Key.enter: "Enter",
        Key.tab: "Tab",
        Key.backspace: "Backspace",
        Key.delete: "Delete",
        Key.esc: "Esc",
        Key.up: "Up",
        Key.down: "Down",
        Key.left: "Left",
        Key.right: "Right",
        Key.home: "Home",
        Key.end: "End",
        Key.page_up: "PageUp",
        Key.page_down: "PageDown",
        Key.caps_lock: "CapsLock",
    }

    if key in special_keys:
        return special_keys[key]

    if hasattr(key, "name") and key.name and key.name.startswith("f"):
        return key.name.upper()

    if isinstance(key, KeyCode):
        if key.char:
            if ord(key.char) >= 1 and ord(key.char) <= 26:
                return chr(ord(key.char) + 64)
            else:
                return key.char.upper()

        if key.vk is not None:
            vk_map = {
                **{i: chr(i) for i in range(65, 91)},
                **{i: chr(i) for i in range(48, 58)},
                96: "Num0",
                97: "Num1",
                98: "Num2",
                99: "Num3",
                100: "Num4",
                101: "Num5",
                102: "Num6",
                103: "Num7",
                104: "Num8",
                105: "Num9",
                186: ";",
                187: "=",
                188: ",",
                189: "-",
                190: ".",
                191: "/",
                192: "`",
                219: "[",
                220: "\\",
                221: "]",
                222: "'",
                106: "Num*",
                107: "Num+",
                109: "Num-",
                110: "Num.",
                111: "Num/",
            }

            if key.vk in vk_map:
                return vk_map[key.vk]

            return f"VK{key.vk}"

    return str(key)


def format_keys(keys_set):
    modifiers = []
    regular_keys = []

    modifier_order = ["Ctrl", "Shift", "Alt", "Meta"]

    for key in keys_set:
        normalized = normalize_key(key)
        if normalized in modifier_order:
            modifiers.append(normalized)
        elif normalized:
            regular_keys.append(normalized)

    sorted_modifiers = sorted(modifiers, key=lambda x: modifier_order.index(x))

    all_keys = sorted_modifiers + sorted(regular_keys)

    return "+".join(all_keys) if all_keys else ""
