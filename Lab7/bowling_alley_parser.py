"""
bowling_alley_parser.py  —  Fixed version
Lab 7: Fuzz Testing for Input Validation Bugs

Bugs identified by Hypothesis and fixed:
  format_player_name: AttributeError on None input (name.strip() fails)
  parse_frame       : AttributeError on None (text.strip() fails),
                      IndexError on empty string (text[0] out of range),
                      ValueError on non-digit/non-'X' first character
  parse_scoreboard  : AttributeError on None (text.split() fails),
                      ValueError on missing ':' (unpack fails),
                      ValueError on non-integer score string (int() fails)

Fix strategy: validate / guard-clause at the top of each function and raise
TypeError for None and ValueError for malformed-but-string inputs, so
callers always receive a predictable exception type.
"""

VALID_DIGITS = set('0123456789')


def format_player_name(name):
    """
    Title-cases a player name and cuts it to 10 characters for the scoreboard.

    Args:
        name: player name string.

    Returns:
        str: title-cased name truncated to 10 characters.

    Raises:
        TypeError : if name is not a string.
        ValueError: if name is empty or whitespace-only.
    """
    if name is None or not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")
    stripped = name.strip()
    if not stripped:
        raise ValueError("name must not be empty or whitespace-only")
    return stripped.title()[:10]


def parse_frame(text):
    """
    Converts frame notation into pins knocked down.
        'X'  -> (10, 0)   strike
        '7/' -> (7, 3)    spare
        '45' -> (4, 5)    open frame

    Args:
        text: frame notation string.

    Returns:
        tuple[int, int]: (first_roll_pins, second_roll_pins).

    Raises:
        TypeError : if text is not a string.
        ValueError: if text is empty, too short, or contains invalid notation.
    """
    if text is None or not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")
    normalised = text.strip().upper()
    if not normalised:
        raise ValueError("frame text must not be empty")
    if normalised == 'X':
        return 10, 0
    if len(normalised) < 2:
        raise ValueError(f"frame text too short to be valid: {text!r}")
    first_char = normalised[0]
    if first_char not in VALID_DIGITS:
        raise ValueError(f"invalid first roll character: {first_char!r}")
    first = int(first_char)
    second_char = normalised[1]
    if second_char == '/':
        return first, 10 - first
    if second_char not in VALID_DIGITS:
        raise ValueError(f"invalid second roll character: {second_char!r}")
    second = int(second_char)
    if first + second > 10:
        raise ValueError(f"pins in frame exceed 10: {first}+{second}")
    return first, second


def parse_scoreboard(text):
    """
    Parses 'Asha:150,Ravi:132' into a {name: score} dictionary.

    Args:
        text: comma-separated 'name:score' entries.

    Returns:
        dict[str, int]: mapping of player name to integer score.

    Raises:
        TypeError : if text is not a string.
        ValueError: if any entry is malformed (missing colon, non-integer score,
                    empty name or score).
    """
    if text is None or not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")
    if not text.strip():
        raise ValueError("scoreboard text must not be empty")
    scores = {}
    for entry in text.split(','):
        entry = entry.strip()
        if ':' not in entry:
            raise ValueError(
                f"entry {entry!r} has no ':' separator; expected 'name:score'")
        parts = entry.split(':', 1)   # split on first ':' only
        name  = parts[0].strip()
        score_str = parts[1].strip()
        if not name:
            raise ValueError(f"empty player name in entry {entry!r}")
        if not score_str:
            raise ValueError(f"empty score in entry {entry!r}")
        try:
            score = int(score_str)
        except ValueError:
            raise ValueError(
                f"score {score_str!r} in entry {entry!r} is not a valid integer")
        scores[name] = score
    return scores


def main():
    print("==== Running format_player_name ====")
    value = input("Enter a player name for the scoreboard: ")
    try:
        print("Scoreboard name:", format_player_name(value))
    except (TypeError, ValueError) as e:
        print(f"  Error: {e}")

    print("\n==== Running parse_frame ====")
    value = input("Enter a frame as X (strike), 7/ (spare) or two digits (e.g. 45): ")
    try:
        print("Pins (first roll, second roll):", parse_frame(value))
    except (TypeError, ValueError) as e:
        print(f"  Error: {e}")

    print("\n==== Running parse_scoreboard ====")
    value = input("Enter scores as NAME:SCORE separated by commas (e.g. Asha:150,Ravi:132): ")
    try:
        print("Scoreboard:", parse_scoreboard(value))
    except (TypeError, ValueError) as e:
        print(f"  Error: {e}")


if __name__ == "__main__":
    main()
