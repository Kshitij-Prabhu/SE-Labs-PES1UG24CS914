"""
Lab 6 — Branch Coverage Test Cases
Student : Kshitij Prabhu
SRN     : PES1UG24CS914
Section : 5B

Target  : ≥ 90% BRANCH coverage of bowling_alley.py
Tool    : coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS914_bowling_alley.py
          coverage report -m

Each test below is named for the specific branch it exercises.
"""

import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# ═══════════════════════════════════════════════════════════════════════════════
# lane_cost — branch map
#   B1: day_type not in LANE_RATE  → True (raise) / False (continue)
#   B2: games < 1 or players < 1 or players > 6  → True (raise) / False (continue)
#   B3: shoe_rentals > players  → True (raise) / False (continue)
#   B4: players > 4  → True (surcharge) / False (no surcharge)
#   B5: is_league_member  → True (discount) / False (no discount)
# ═══════════════════════════════════════════════════════════════════════════════

# B1 — True: unknown day_type raises ValueError
def test_lc_b1_unknown_day_type():
    with pytest.raises(ValueError, match="unknown day type"):
        lane_cost("holiday", 1, 2, 0, False)


# B1 — False: known day_type proceeds normally
def test_lc_b1_known_day_type_weekday():
    assert lane_cost("weekday", 1, 2, 0, False) == 400


# B1 — False (second known day_type): weekend rate
def test_lc_b1_known_day_type_weekend():
    assert lane_cost("weekend", 1, 2, 0, False) == 600


# B2 — True: games < 1 raises ValueError
def test_lc_b2_games_zero():
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 0, 2, 0, False)


# B2 — True: players < 1 raises ValueError
def test_lc_b2_players_zero():
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 0, 0, False)


# B2 — True: players > 6 raises ValueError
def test_lc_b2_players_seven():
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 7, 0, False)


# B2 — False: games=1, players=1 passes validation
def test_lc_b2_minimum_valid_booking():
    assert lane_cost("weekday", 1, 1, 0, False) == 400


# B3 — True: shoe_rentals > players raises ValueError
def test_lc_b3_too_many_shoes():
    with pytest.raises(ValueError, match="too many shoe rentals"):
        lane_cost("weekday", 1, 2, 3, False)


# B3 — False: shoe_rentals == players is allowed
def test_lc_b3_shoes_equal_players():
    # weekday 1 game, 2 players, 2 shoes → 400 + 100 = 500
    assert lane_cost("weekday", 1, 2, 2, False) == 500


# B4 — True: players > 4 triggers surcharge
def test_lc_b4_players_five_surcharge():
    # weekday 2 games, 5 players, 0 shoes → (400*2) + (100*2) = 1000
    assert lane_cost("weekday", 2, 5, 0, False) == 1000


# B4 — True: players == 6 (still > 4)
def test_lc_b4_players_six_surcharge():
    # weekend 1 game, 6 players → 600 + 100 = 700
    assert lane_cost("weekend", 1, 6, 0, False) == 700


# B4 — False: players == 4 (no surcharge)
def test_lc_b4_players_four_no_surcharge():
    # weekday 1 game, 4 players → 400 exactly
    assert lane_cost("weekday", 1, 4, 0, False) == 400


# B4 — False: players == 1 (no surcharge)
def test_lc_b4_players_one_no_surcharge():
    assert lane_cost("weekday", 1, 1, 1, False) == 450


# B5 — True: league member discount applied
def test_lc_b5_league_member_discount():
    # weekday 1 game, 2 players → 400; discount = 400//5 = 80 → 320
    assert lane_cost("weekday", 1, 2, 0, True) == 320


# B5 — False: non-member, no discount
def test_lc_b5_non_member_no_discount():
    assert lane_cost("weekday", 1, 2, 0, False) == 400


# ═══════════════════════════════════════════════════════════════════════════════
# frame_score — branch map
#   B6:  first_roll < 0 or first_roll > 10 or second_roll < 0  → True (raise)
#        Each sub-condition (for full branch coverage of the compound guard):
#           B6a: first_roll < 0 is True
#           B6b: first_roll > 10 is True
#           B6c: second_roll < 0 is True
#           B6d: entire condition is False (valid rolls)
#   B7:  first_roll == 10  → True (strike) / False (not a strike)
#   B8:  first_roll + second_roll > 10  → True (raise) / False (continue)
#   B9:  first_roll + second_roll == 10  → True (spare) / False (open frame)
# ═══════════════════════════════════════════════════════════════════════════════

# B6a — first_roll < 0
def test_fs_b6a_negative_first_roll():
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(-1, 4, [])


# B6b — first_roll > 10
def test_fs_b6b_first_roll_over_ten():
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(11, 0, [])


# B6c — second_roll < 0
def test_fs_b6c_negative_second_roll():
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(5, -1, [])


# B6d — guard condition is False (valid input proceeds)
def test_fs_b6d_valid_rolls_proceed():
    assert frame_score(3, 4, []) == 7


# B7 — True: strike (first_roll == 10)
def test_fs_b7_strike_true():
    # Strike with bonus [6, 3] → 10 + 6 + 3 = 19
    assert frame_score(10, 0, [6, 3]) == 19


# B7 — True: strike with zero bonus
def test_fs_b7_strike_zero_bonus():
    assert frame_score(10, 0, [0, 0]) == 10


# B7 — False: first_roll != 10, continues to next checks
def test_fs_b7_not_a_strike():
    # 7 + 3 = spare, not a strike
    assert frame_score(7, 3, [5, 0]) == 15


# B8 — True: first + second > 10 raises (non-strike situation)
def test_fs_b8_invalid_frame_total():
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(6, 5, [])


# B8 — True: boundary case
def test_fs_b8_boundary_eleven():
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(9, 2, [])


# B8 — False: first + second <= 10 (spare)
def test_fs_b8_spare_not_over_ten():
    assert frame_score(7, 3, [4, 0]) == 14


# B8 — False: first + second < 10 (open frame)
def test_fs_b8_open_frame_under_ten():
    assert frame_score(4, 5, []) == 9


# B9 — True: spare (first + second == 10)
def test_fs_b9_spare_true():
    # Spare with bonus[0]=5 → 10 + 5 = 15
    assert frame_score(7, 3, [5, 0]) == 15


# B9 — True: spare from different pins
def test_fs_b9_spare_zero_first():
    assert frame_score(0, 10, [3, 0]) == 13


# B9 — False: open frame (first + second < 10)
def test_fs_b9_open_frame_false():
    assert frame_score(3, 4, []) == 7


# B9 — False: gutter frame
def test_fs_b9_gutter_ball():
    assert frame_score(0, 0, []) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# lane_assignment — branch map
#   B10: lanes_free == 0  → True ("wait") / False (continue)
#   B11: has_kids  → True ("bumper lane") / False (continue)
#   B12: players > 6 and lanes_free >= 2  → True ("two lanes") / False (elif)
#   B13: players > 6 (the elif)  → True ("wait") / False ("standard lane")
#        Sub-conditions of B12:
#           B12a: players > 6 is True but lanes_free < 2 → falls to elif
#           B12b: players > 6 is True and lanes_free >= 2 → "two lanes"
#           B12c: players <= 6 → skips both → "standard lane"
# ═══════════════════════════════════════════════════════════════════════════════

# B10 — True: no lanes free → "wait"
def test_la_b10_no_lanes_free():
    assert lane_assignment(4, False, 0) == "wait"


# B10 — True: large group but still no lanes
def test_la_b10_large_group_no_lanes():
    assert lane_assignment(9, False, 0) == "wait"


# B10 — False: lanes are free, proceeds
def test_la_b10_lanes_available():
    assert lane_assignment(4, False, 2) == "standard lane"


# B11 — True: has kids → "bumper lane"
def test_la_b11_has_kids():
    assert lane_assignment(3, True, 1) == "bumper lane"


# B11 — True: even one kid with many players
def test_la_b11_has_kids_large_group():
    assert lane_assignment(6, True, 3) == "bumper lane"


# B11 — False: no kids, continues to size check
def test_la_b11_no_kids():
    assert lane_assignment(4, False, 1) == "standard lane"


# B12 — True: players > 6 AND lanes_free >= 2 → "two lanes"
def test_la_b12_large_group_two_lanes_available():
    assert lane_assignment(7, False, 2) == "two lanes"


def test_la_b12_very_large_group_many_lanes():
    assert lane_assignment(10, False, 5) == "two lanes"


# B12a / B13 — True: players > 6 but lanes_free == 1 → elif fires → "wait"
def test_la_b12a_large_group_one_lane():
    assert lane_assignment(7, False, 1) == "wait"


def test_la_b12a_nine_players_one_lane():
    assert lane_assignment(9, False, 1) == "wait"


# B12c / B13 — False: players <= 6 → "standard lane"
def test_la_b13_six_players_standard():
    assert lane_assignment(6, False, 1) == "standard lane"


def test_la_b13_one_player_standard():
    assert lane_assignment(1, False, 10) == "standard lane"
