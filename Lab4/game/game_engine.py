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

        # Input box
        self.input_box = TextBox(
            width // 2 - 130,
            210,
            160,
            46
        )

        # Submit button
        self.submit_btn = pygame.Rect(
            width // 2 + 45,
            210,
            95,
            46
        )

        # Task 2: Hint button
        self.hint_btn = pygame.Rect(
            width // 2 - 130,
            275,
            95,
            40
        )

        self.hint_penalty = 0.25
        self.revealed_positions = []

        # Task 4: Interactive letter tiles
        self.tile_letters = []
        self.tile_rects = []
        self.selected_tile = None

        # Fonts
        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 40)
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
        pygame.time.set_timer(self.timer_event, 0)

        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(
            self.secret_word
        )

        self.input_box.clear()

        # Reset hints
        self.revealed_positions = []

        # Reset timer
        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()
        self.round_expired = False

        # Task 4: Create fresh letter tiles
        self.tile_letters = list(self.scrambled_word)
        self.tile_rects = []
        self.selected_tile = None

        self.feedback_msg = "Arrange the letters and submit!"
        self.feedback_color = (210, 215, 225)

    def submit_guess(self):
        # If the player typed something, use the typed answer.
        # Otherwise use the arrangement of the letter tiles.
        typed_guess = self.input_box.text.strip().upper()

        if typed_guess:
            guess = typed_guess
        else:
            guess = "".join(self.tile_letters)

        if not guess:
            self.feedback_msg = "Arrange or type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Compare with the actual secret word
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1

            self.feedback_msg = (
                f"CORRECT! '{self.secret_word}' is right."
            )

            self.feedback_color = (80, 230, 110)

            self.next_round()

        else:
            self.feedback_msg = "WRONG GUESS! Rearrange and try again."
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
            self.feedback_msg = (
                "All letters have already been revealed!"
            )
            self.feedback_color = (240, 170, 50)
            return

        position = random.choice(unrevealed)

        self.revealed_positions.append(position)

        self.score = max(
            0,
            self.score - self.hint_penalty
        )

        revealed_letter = self.secret_word[position]

        # Clearly tell the player which letter was revealed
        self.feedback_msg = (
            f"Hint: Letter '{revealed_letter}' is in "
            f"position {position + 1}! "
            f"-{self.hint_penalty:.2f} points."
        )

        self.feedback_color = (240, 200, 80)

    def handle_event(self, event):

        # Task 3: Timer expiration
        if event.type == self.timer_event:
            pygame.time.set_timer(
                self.timer_event,
                0
            )

            self.round_expired = False
            self.next_round()
            return

        if self.round_expired:
            return

        self.input_box.handle_event(event)

        # Keyboard Enter
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.submit_guess()

        # Mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Submit button
                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()

                # Hint button
                elif self.hint_btn.collidepoint(event.pos):
                    self.use_hint()

                # Task 4: Letter tile selection
                else:

                    for index, rect in enumerate(
                        self.tile_rects
                    ):

                        if rect.collidepoint(event.pos):

                            if self.selected_tile is None:

                                # First tile selected
                                self.selected_tile = index

                                self.feedback_msg = (
                                    "Tile selected. "
                                    "Click another tile to swap."
                                )

                                self.feedback_color = (
                                    210,
                                    215,
                                    225
                                )

                            else:

                                # Second tile selected
                                # Swap the two letters
                                if index != self.selected_tile:

                                    (
                                        self.tile_letters[
                                            self.selected_tile
                                        ],
                                        self.tile_letters[index]
                                    ) = (
                                        self.tile_letters[index],
                                        self.tile_letters[
                                            self.selected_tile
                                        ]
                                    )

                                    self.feedback_msg = (
                                        "Letters rearranged!"
                                    )

                                    self.feedback_color = (
                                        210,
                                        215,
                                        225
                                    )

                                self.selected_tile = None

                            break

    def update(self):

        if self.round_expired:
            return

        # Task 3: Countdown timer
        current_time = pygame.time.get_ticks()

        elapsed_seconds = (
            current_time - self.last_time
        ) / 1000.0

        self.time_left -= elapsed_seconds
        self.last_time = current_time

        if self.time_left <= 0:

            self.time_left = 0
            self.round_expired = True

            # Reveal the correct word
            self.feedback_msg = (
                f"Time's up! The word was "
                f"'{self.secret_word}'."
            )

            self.feedback_color = (
                240,
                80,
                80
            )

            # Move to next round after 1.5 seconds
            pygame.time.set_timer(
                self.timer_event,
                1500
            )

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
                self.width // 2
                - title_surf.get_width() // 2,
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
                self.width // 2
                - score_surf.get_width() // 2,
                70
            )
        )

        # Timer
        timer_surf = self.font_msg.render(
            f"Time: {self.time_left:.1f}s",
            True,
            (255, 180, 80)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                100
            )
        )

        # ==================================================
        # TASK 4: INTERACTIVE LETTER TILES
        # ==================================================

        tile_width = 48
        tile_height = 52
        tile_gap = 8

        total_width = (
            len(self.tile_letters) * tile_width
            + (len(self.tile_letters) - 1) * tile_gap
        )

        start_x = (
            self.width // 2
            - total_width // 2
        )

        tile_y = 155

        self.tile_rects = []

        for index, letter in enumerate(
            self.tile_letters
        ):

            x = start_x + index * (
                tile_width + tile_gap
            )

            rect = pygame.Rect(
                x,
                tile_y,
                tile_width,
                tile_height
            )

            self.tile_rects.append(rect)

            # Selected tile
            if index == self.selected_tile:
                tile_color = (100, 160, 240)
            else:
                tile_color = (50, 70, 100)

            pygame.draw.rect(
                screen,
                tile_color,
                rect,
                border_radius=6
            )

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                rect,
                width=2,
                border_radius=6
            )

            letter_surf = self.font_word.render(
                letter,
                True,
                (255, 255, 255)
            )

            screen.blit(
                letter_surf,
                (
                    rect.centerx
                    - letter_surf.get_width() // 2,
                    rect.centery
                    - letter_surf.get_height() // 2
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

        # Feedback
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
