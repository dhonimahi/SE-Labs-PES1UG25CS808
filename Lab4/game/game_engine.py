import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = [
            "PYTHON",
            "PYGAME",
            "PLANET",
            "ROCKET",
            "GALAXY",
            "STREAM",
            "PUZZLE",
            "ALGORITHM"
        ]

        self.secret_word = ""
        self.scrambled_word = ""

        self.score = 0.0
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        self.input_box = TextBox(width // 2 - 130, 210, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 + 45, 210, 95, 46)

        # Task 2: Hint button
        self.hint_btn = pygame.Rect(width // 2 - 130, 275, 95, 40)
        self.hint_penalty = 0.25
        self.revealed_positions = []

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)

        self.next_round()

    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            if shuffled != word or len(word) <= 1:
                return shuffled

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)

        self.input_box.clear()

        # Task 2: Reset hints for the new round
        self.revealed_positions = []

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Compare with the actual secret word
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)
            self.next_round()

        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()

    def use_hint(self):
        """Reveal one unrevealed letter in its correct position."""

        unrevealed = [
            i for i in range(len(self.secret_word))
            if i not in self.revealed_positions
        ]

        if not unrevealed:
            self.feedback_msg = "All letters have already been revealed!"
            self.feedback_color = (240, 170, 50)
            return

        position = random.choice(unrevealed)
        self.revealed_positions.append(position)

        self.score = max(0, self.score - self.hint_penalty)

        revealed_count = len(self.revealed_positions)

        self.feedback_msg = (
            f"Hint used! {revealed_count} letter(s) revealed. "
            f"-{self.hint_penalty:.2f} points."
        )

        self.feedback_color = (240, 200, 80)

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit_guess()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

            elif self.hint_btn.collidepoint(event.pos):
                self.use_hint()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((26, 30, 38))

        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                25
            )
        )

        score_surf = self.font_msg.render(
            f"Score: {self.score:.2f}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                70
            )
        )

        # Show scrambled letters, with revealed letters shown
        # in their correct positions.
        display_letters = []

        for i, letter in enumerate(self.secret_word):

            if i in self.revealed_positions:
                display_letters.append(letter)

            else:
                display_letters.append("_")

        # If no hints have been used, show the original scrambled word.
        if not self.revealed_positions:
            display_letters = list(self.scrambled_word)

        spaced_letters = "  ".join(display_letters)

        scramble_surf = self.font_word.render(
            spaced_letters,
            True,
            (100, 200, 255)
        )

        screen.blit(
            scramble_surf,
            (
                self.width // 2 - scramble_surf.get_width() // 2,
                130
            )
        )

        self.input_box.render(screen)

        # SUBMIT button
        pygame.draw.rect(
            screen,
            (50, 150, 85),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2
            )
        )

        # HINT button
        pygame.draw.rect(
            screen,
            (70, 100, 180),
            self.hint_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.hint_btn,
            width=2,
            border_radius=6
        )

        hint_text = self.font_btn.render(
            "HINT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_text,
            (
                self.hint_btn.centerx - hint_text.get_width() // 2,
                self.hint_btn.centery - hint_text.get_height() // 2
            )
        )

        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                335
            )
        )
