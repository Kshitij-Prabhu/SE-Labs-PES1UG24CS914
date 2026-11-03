"""
Lab 6 — Code Coverage Test Cases
Student : Kshitij Prabhu
SRN     : PES1UG24CS914
Section : 5B

Target  : ≥ 90% LINE (code) coverage of bowling_alley.py
Tool    : coverage run -m pytest CodeCoverageTest_PES1UG24CS914_bowling_alley.py
          coverage report -m
"""

import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# ── lane_cost ────────────────────────────────────────────────────────────────

def test_weekday_basic():
    """Weekday, 2 games, 4 players, 2 shoe rentals, non-member."""
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_weekend_basic():
    """Weekend rate is applied correctly."""
    assert lane_cost("weekend", 1, 2, 0, False) == 600


def test_unknown_day_type_raises():
    """Unknown day_type raises ValueError."""
    with pytest.raises(ValueError, match="unknown day type"):
        lane_cost("holiday", 1, 2, 0, False)


def test_zero_games_raises():
    """games < 1 raises ValueError."""
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 0, 2, 0, False)


def test_zero_players_raises():
    """players < 1 raises ValueError."""
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 0, 0, False)


def test_too_many_players_raises():
    """players > 6 raises ValueError."""
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 7, 0, False)


def test_shoe_rentals_exceed_players_raises():
    """shoe_rentals > players raises ValueError."""
    with pytest.raises(ValueError, match="too many shoe rentals"):
        lane_cost("weekday", 1, 3, 4, False)


def test_players_over_four_surcharge():
    """5 players triggers the +100/game surcharge."""
    # weekday 1 game, 5 players, 0 shoes, non-member
    # cost = 400 + 100 = 500
    assert lane_cost("weekday", 1, 5, 0, False) == 500


def test_shoe_rental_cost():
    """Shoe rentals add 50 per pair."""
    # weekday 1 game, 3 players, 3 shoes → 400 + 150 = 550
    assert lane_cost("weekday", 1, 3, 3, False) == 550


def test_league_member_discount():
    """League member receives a 20% discount (cost // 5 subtracted)."""
    # weekday 1 game, 2 players, 0 shoes → 400; discount = 80 → 320
    assert lane_cost("weekday", 1, 2, 0, True) == 320


def test_league_member_with_surcharge_and_shoes():
    """Combination: 5 players, shoes, league member."""
    # weekend 2 games, 5 players, 2 shoes, member
    # base = 600*2 = 1200, surcharge = 100*2 = 200, shoes = 100 → 1500
    # discount = 1500//5 = 300 → 1200
    assert lane_cost("weekend", 2, 5, 2, True) == 1200


# ── frame_score ──────────────────────────────────────────────────────────────

def test_open_frame():
    """Regular open frame: 3 + 4 = 7."""
    assert frame_score(3, 4, []) == 7


def test_strike():
    """Strike: first_roll == 10, add two bonus rolls."""
    assert frame_score(10, 0, [6, 3]) == 19


def test_spare():
    """Spare: first + second == 10, add one bonus roll."""
    assert frame_score(7, 3, [5, 0]) == 15


def test_negative_first_roll_raises():
    """first_roll < 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(-1, 4, [])


def test_first_roll_over_ten_raises():
    """first_roll > 10 raises ValueError."""
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(11, 0, [])


def test_negative_second_roll_raises():
    """second_roll < 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(5, -1, [])


def test_frame_total_over_ten_raises():
    """first + second > 10 (non-strike) raises ValueError."""
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(6, 5, [])


def test_zero_zero_frame():
    """Gutter frame: 0 + 0 = 0."""
    assert frame_score(0, 0, []) == 0


# ── lane_assignment ──────────────────────────────────────────────────────────

def test_no_lanes_free():
    """No lanes available returns 'wait'."""
    assert lane_assignment(4, False, 0) == "wait"


def test_has_kids_gets_bumper_lane():
    """Party with kids gets bumper lane when lanes are free."""
    assert lane_assignment(3, True, 2) == "bumper lane"


def test_standard_lane():
    """Normal party (≤ 6, no kids) gets a standard lane."""
    assert lane_assignment(4, False, 3) == "standard lane"


def test_large_group_two_lanes():
    """Group > 6 with ≥ 2 lanes free gets two lanes."""
    assert lane_assignment(8, False, 2) == "two lanes"


def test_large_group_only_one_lane_waits():
    """Group > 6 with only 1 lane free must wait."""
    assert lane_assignment(8, False, 1) == "wait"
