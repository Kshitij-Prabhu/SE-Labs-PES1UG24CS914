import random
import pygame
from game.button import ChoiceButton

# ── TASK 2 constant ───────────────────────────────────────────
WIN_TARGET = 5          # First to 5 wins the match


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton("ROCK",     pygame.Rect(start_x,                  btn_y, btn_w, btn_h), (160, 50,  50),  (200, 70,  70)),
            ChoiceButton("PAPER",    pygame.Rect(start_x + btn_w + gap,    btn_y, btn_w, btn_h), (40,  100, 170), (60,  130, 210)),
            ChoiceButton("SCISSORS", pygame.Rect(start_x + 2*(btn_w + gap),btn_y, btn_w, btn_h), (180, 140, 30),  (220, 180, 50)),
        ]

        self.player_choice = None
        self.cpu_choice    = None
        self.result_text   = "Make your move!"
        self.result_color  = (220, 225, 235)

        self.player_score = 0
        self.cpu_score    = 0

        self.round_resolved_time = 0
        self.display_duration    = 1800
        self.showing_result      = False

        # ── TASK 2 ────────────────────────────────────────────
        self.match_over       = False
        self.match_winner_text = ""

        # ── TASK 3: adaptive AI ───────────────────────────────
        # Track how many times the player has thrown each choice
        self.player_history = {"ROCK": 0, "PAPER": 0, "SCISSORS": 0}
        # What beats each choice
        self.counter = {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud   = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_big   = pygame.font.SysFont(None, 52)

    # ── TASK 1: BUG FIX ───────────────────────────────────────
    def determine_winner(self, player, cpu):
        """
        BUG: The original rules dict had the winners INVERTED.
        e.g. ("ROCK", "SCISSORS"): "CPU"  — but Rock BEATS Scissors,
        so the winner should be PLAYER, not CPU.
        FIX: Swap every "CPU" and "PLAYER" value in the rules dict.
        """
        if player == cpu:
            return "TIE"

        rules = {
            ("ROCK",     "SCISSORS"): "PLAYER",   # Rock beats Scissors
            ("SCISSORS", "PAPER"):    "PLAYER",   # Scissors beats Paper
            ("PAPER",    "ROCK"):     "PLAYER",   # Paper beats Rock
            ("SCISSORS", "ROCK"):     "CPU",      # Rock beats Scissors (CPU wins)
            ("PAPER",    "SCISSORS"): "CPU",      # Scissors beats Paper (CPU wins)
            ("ROCK",     "PAPER"):    "CPU",      # Paper beats Rock (CPU wins)
        }
        return rules.get((player, cpu), "TIE")

    # ── TASK 3: adaptive CPU pick ─────────────────────────────
    def cpu_pick(self):
        """
        After 4+ rounds, if one choice makes up >50% of the player's
        throws, bias the CPU toward the counter-move (70% of the time).
        Otherwise pick randomly.
        """
        total = sum(self.player_history.values())
        if total >= 4:
            most_common = max(self.player_history, key=self.player_history.get)
            if self.player_history[most_common] / total > 0.5:
                # 70% chance to play the counter, 30% random
                if random.random() < 0.7:
                    return self.counter[most_common]
        return random.choice(self.choices)

    def play_round(self, choice):
        if self.match_over or self.showing_result:
            return

        self.player_choice = choice

        # ── TASK 3: record player throw ───────────────────────
        self.player_history[choice] += 1

        # ── TASK 3: use adaptive CPU pick ─────────────────────
        self.cpu_choice = self.cpu_pick()

        outcome = self.determine_winner(self.player_choice, self.cpu_choice)
        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text  = f"You Win! {self.player_choice} beats {self.cpu_choice}."
            self.result_color = (80, 230, 120)
        elif outcome == "CPU":
            self.cpu_score   += 1
            self.result_text  = f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            self.result_color = (240, 80, 80)
        else:
            self.result_text  = f"It's a Draw! Both picked {self.player_choice}."
            self.result_color = (240, 210, 80)

        # ── TASK 2: check for match winner ────────────────────
        if self.player_score >= WIN_TARGET:
            self.match_over        = True
            self.match_winner_text = f"YOU WIN THE MATCH! {WIN_TARGET}-{self.cpu_score}"
        elif self.cpu_score >= WIN_TARGET:
            self.match_over        = True
            self.match_winner_text = f"CPU WINS THE MATCH! {WIN_TARGET}-{self.player_score}"

        self.showing_result      = True
        self.round_resolved_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ── TASK 2: R to restart after match over ─────────
            if self.match_over:
                return
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break
        # ── TASK 2: keyboard R restarts ───────────────────────
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.__init__(self.width, self.height)

    def update(self):
        if self.match_over:
            return
        now = pygame.time.get_ticks()
        if self.showing_result and (now - self.round_resolved_time >= self.display_duration):
            self.player_choice = None
            self.cpu_choice    = None
            self.result_text   = "Make your move!"
            self.result_color  = (190, 195, 205)
            self.showing_result = False

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render("Rock Paper Scissors", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 14))

        p_surf = self.font_hud.render(f"Player Score: {self.player_score}", True, (100, 180, 255))
        c_surf = self.font_hud.render(f"CPU Score: {self.cpu_score}",       True, (255, 120, 120))
        screen.blit(p_surf, (35, 52))
        screen.blit(c_surf, (self.width - c_surf.get_width() - 35, 52))

        # ── TASK 2: show first-to-X target ───────────────────
        target_surf = self.font_hud.render(f"First to {WIN_TARGET} wins!", True, (160, 160, 170))
        screen.blit(target_surf, (self.width // 2 - target_surf.get_width() // 2, 52))

        pygame.draw.line(screen, (45, 52, 66), (25, 82), (self.width - 25, 82), 2)

        p_str = self.player_choice if self.player_choice else "--"
        c_str = self.cpu_choice    if self.cpu_choice    else "--"

        arena_p = self.font_arena.render(f"Your Pick:  {p_str}", True, (225, 225, 230))
        arena_c = self.font_arena.render(f"CPU Pick:  {c_str}",  True, (225, 225, 230))
        screen.blit(arena_p, (self.width // 2 - arena_p.get_width() // 2, 100))
        screen.blit(arena_c, (self.width // 2 - arena_c.get_width() // 2, 140))

        res_surf = self.font_arena.render(self.result_text, True, self.result_color)
        screen.blit(res_surf, (self.width // 2 - res_surf.get_width() // 2, 185))

        # ── TASK 2: match-over banner ─────────────────────────
        if self.match_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            winner_color = (80, 230, 120) if self.player_score >= WIN_TARGET else (240, 80, 80)
            w_surf = self.font_big.render(self.match_winner_text, True, winner_color)
            screen.blit(w_surf, (self.width // 2 - w_surf.get_width() // 2, self.height // 2 - 40))

            r_surf = self.font_hud.render("Press R to play again", True, (200, 200, 200))
            screen.blit(r_surf, (self.width // 2 - r_surf.get_width() // 2, self.height // 2 + 20))
        else:
            for btn in self.buttons:
                btn.render(screen)
