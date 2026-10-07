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

        # Score
        self.score = 0.0

        # Task 3: Countdown timer
        self.round_time = 30.0
        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()
        self.round_expired = False
        self.timer_event = pygame.USEREVENT + 1

        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        # Input and Submit button
        self.input_box = TextBox(width // 2 - 130, 210, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 + 45, 210, 95, 46)

        # Task 2: Hint button
        self.hint_btn = pygame.Rect(width // 2 - 130, 275, 95, 40)
        self.hint_penalty = 0.25
        self.revealed_positions = []

        # Fonts
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
        # Stop any pending timer event
        pygame.time.set_timer(self.timer_event, 0)

        # Select a new word
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)

        # Clear previous input
        self.input_box.clear()

        # Task 2: Reset hints
        self.revealed_positions = []

        # Task 3: Reset countdown timer
        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()
        self.round_expired = False

        # Reset feedback
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Compare the guess with the actual secret word
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)

            # Start next round
            self.next_round()

        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()

    def use_hint(self):
        """Reveal one unrevealed letter in its correct position."""

        if self.round_expired:
            return

        unrevealed = [
            i
            for i in range(len(self.secret_word))
            if i not in self.revealed_positions
        ]

        if not unrevealed:
            self.feedback_msg = "All letters have already been revealed!"
            self.feedback_color = (240, 170, 50)
            return

        # Select one hidden position
        position = random.choice(unrevealed)
        self.revealed_positions.append(position)

        # Apply hint penalty
        self.score = max(0, self.score - self.hint_penalty)

        revealed_count = len(self.revealed_positions)

        self.feedback_msg = (
            f"Hint used! {revealed_count} letter(s) revealed. "
            f"-{self.hint_penalty:.2f} points."
        )

        self.feedback_color = (240, 200, 80)

    def handle_event(self, event):

        # Task 3: Handle timer expiration
        if event.type == self.timer_event:
            pygame.time.set_timer(self.timer_event, 0)

            self.round_expired = False
            self.next_round()
            return

        # Ignore gameplay input after time expires
        if self.round_expired:
            return

        self.input_box.handle_event(event)

        # Enter key submits the answer
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit_guess()

        # Mouse buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

            elif self.hint_btn.collidepoint(event.pos):
                self.use_hint()

    def update(self):
        # Task 3: Update countdown timer
        if self.round_expired:
            return

        current_time = pygame.time.get_ticks()

        elapsed_seconds = (
            current_time - self.last_time
        ) / 1000.0

        self.time_left -= elapsed_seconds
        self.last_time = current_time

        # Time has expired
        if self.time_left <= 0:
            self.time_left = 0
            self.round_expired = True

            self.feedback_msg = (
                f"Time's up! The word was '{self.secret_word}'."
            )

            self.feedback_color = (240, 80, 80)

            # Move to next round after 1.5 seconds
            pygame.time.set_timer(self.timer_event, 1500)

    def render(self, screen):
        screen.fill((26, 30, 38))

        # Title
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

        # Score
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

        # Task 3: Timer display
        timer_surf = self.font_msg.render(
            f"Time: {self.time_left:.1f}s",
            True,
            (255, 180, 80)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2 - timer_surf.get_width() // 2,
                100
            )
        )

        # Display scrambled letters or revealed letters
        display_letters = []

        for i, letter in enumerate(self.secret_word):

            if i in self.revealed_positions:
                display_letters.append(letter)

            else:
                display_letters.append("_")

        # Before using a hint, show the scrambled word
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
                145
            )
        )

        # Input box
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
                self.submit_btn.centerx
                - btn_text.get_width() // 2,
                self.submit_btn.centery
                - btn_text.get_height() // 2
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
                self.hint_btn.centerx
                - hint_text.get_width() // 2,
                self.hint_btn.centery
                - hint_text.get_height() // 2
            )
        )

        # Feedback message
        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2
                - feedback_surf.get_width() // 2,
                335
            )
        )
