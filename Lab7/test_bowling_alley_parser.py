"""
Lab 7 — Fuzz Testing with Hypothesis
Student : Kshitij Prabhu
SRN     : PES1UG24CS914
Section : 5B

Goal    : Use Hypothesis to uncover edge-case input validation bugs
          in bowling_alley_parser.py for all three functions.
"""

from hypothesis import given, strategies as st
from bowling_alley_parser import format_player_name, parse_frame, parse_scoreboard


# ── format_player_name ────────────────────────────────────────────────────────

@given(st.text() | st.none())
def test_format_player_name_no_crash(s):
    """
    Property: format_player_name must never crash for any string or None input.
    It should return a string of at most 10 characters, or raise ValueError
    for genuinely invalid input — but must NEVER raise AttributeError, TypeError,
    or any unhandled exception.
    """
    try:
        result = format_player_name(s)
        # If it succeeds, the result must be a string of at most 10 chars
        assert isinstance(result, str), "Result must be a string"
        assert len(result) <= 10, f"Result too long: {len(result)} chars"
    except (ValueError, TypeError):
        # Acceptable: implementation may choose to reject None / empty input
        pass
    except Exception as e:
        assert False, f"format_player_name crashed with unexpected exception: {type(e).__name__}: {e}"


# ── parse_frame ───────────────────────────────────────────────────────────────

@given(st.text() | st.none())
def test_parse_frame_no_crash(s):
    """
    Property: parse_frame must never crash with an unhandled exception.
    For valid frame notation ('X', '7/', '45') it must return a 2-tuple of ints.
    For anything else it must raise ValueError or TypeError — not AttributeError,
    IndexError, or other unguarded exceptions.
    """
    try:
        result = parse_frame(s)
        # If it succeeds, result must be a 2-tuple of non-negative ints summing ≤ 10
        assert isinstance(result, tuple) and len(result) == 2, \
            f"Expected 2-tuple, got {result!r}"
        first, second = result
        assert isinstance(first, int) and isinstance(second, int), \
            f"Tuple elements must be ints: {result!r}"
        assert first >= 0 and second >= 0, \
            f"Pin counts must be non-negative: {result!r}"
        assert first + second <= 10, \
            f"Total pins > 10: {result!r}"
    except (ValueError, TypeError):
        # Acceptable: bad input should raise these
        pass
    except Exception as e:
        assert False, f"parse_frame crashed with unexpected exception: {type(e).__name__}: {e}"


# ── parse_scoreboard ──────────────────────────────────────────────────────────

@given(st.text() | st.none())
def test_parse_scoreboard_no_crash(s):
    """
    Property: parse_scoreboard must never crash with an unhandled exception.
    For valid input ('Asha:150,Ravi:132') it must return a dict mapping str→int.
    For invalid input it must raise ValueError or TypeError — not AttributeError
    or unguarded exceptions from split/unpack/int conversion.
    """
    try:
        result = parse_scoreboard(s)
        # If it succeeds, result must be a dict with str keys and int values
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        for k, v in result.items():
            assert isinstance(k, str), f"Key must be str: {k!r}"
            assert isinstance(v, int), f"Value must be int: {v!r}"
    except (ValueError, TypeError):
        # Acceptable: bad input should raise these
        pass
    except Exception as e:
        assert False, f"parse_scoreboard crashed with unexpected exception: {type(e).__name__}: {e}"
