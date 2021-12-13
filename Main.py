import pygame
import random

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH + 300, HEIGHT))
pygame.display.set_caption("LUDO GAME")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (76, 187, 23)
DARK_GREEN = (0, 124, 16)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 148)
YELLOW = (255, 255, 0)
DARK_YELLOW = (192, 192, 0)
RED = (255, 0, 0)
DARK_RED = (144, 0, 0)
GREY = (100, 100, 100)
GOLD = (164, 129, 17)
SILVER = (176, 187, 192)
BRONZE = (176, 108, 40)

NUM_OF_LINES = 16
SQUARE_SIZE = 40

FPS = 60

RED_PAWN = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\red_pawn.png')
GREEN_PAWN = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\green_pawn.png')
YELLOW_PAWN = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\yellow_pawn.png')
BLUE_PAWN = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\blue_pawn.png')

DICE_ONE = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_one.png')
DICE_TWO = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_two.PNG')
DICE_THREE = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_three.PNG')
DICE_FOUR = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_four.PNG')
DICE_FIVE = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_five.PNG')
DICE_SIX = pygame.image.load(r'C:\Huwaei\Programming\Python_Revision\LudoGame\images\dice_six.PNG')

dices = [DICE_ONE, DICE_TWO, DICE_THREE, DICE_FOUR, DICE_FIVE, DICE_SIX]

medals = [GOLD, SILVER, BRONZE, GREY]

C = [GREEN, RED, BLUE, YELLOW]


class GameWindow:
    def __init__(self):
        pygame.init()
        self.corr = [(2 * SQUARE_SIZE) + 1, (3 * SQUARE_SIZE) + 1, (11 * SQUARE_SIZE) + 1, (12 * SQUARE_SIZE) + 1]
        self.colours = [GREEN_PAWN, RED_PAWN, BLUE_PAWN, YELLOW_PAWN]
        self.found_target = False
        self.next_step = False
        self.pawn_number_choice = False
        self.initial_setup = True
        self.initial = [[1 for _ in range(4)], [1 for _ in range(4)], [1 for _ in range(4)], [1 for _ in range(4)]]
        self.steps = 1
        self.colour_index_increase = lambda x: x + 1 if (x < 3) else 0
        self.colour_index_decrease = lambda x: x - 1 if (x > 0) else 3
        self.ready_to_move_phase_one = False
        self.ready_to_move_phase_two = False
        self.ready_to_move_phase_three = False
        self.game_state_change_one = False
        self.game_state_change_two = False
        self.game_state_change_three = False
        self.up_down_index = 0
        self.confirm_setup = False
        self.roll_the_dice = False
        self.choose_the_pawn = False
        self.choose_other_pawn = False
        self.game_over = False

    def main(self):
        all_pawns = Pawn(self.corr)
        all_pawns.initial_pawn_position()
        all_players = Player()
        clock = pygame.time.Clock()
        index = 0
        prev_index = 0
        all_pawns.pawn_number = 0
        all_pawns.colour_index = 0
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # ------ SECTION 1 - SELECT NUMBER OF STEPS ---------
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2] and \
                        not self.next_step and not self.initial_setup:
                    self.steps = random.randrange(1, 7)
                    self.draw_dice()
                    if self.steps != 6 and 0 not in self.initial[all_pawns.colour_index]:
                        self.game_state_change_one = True
                        pygame.time.delay(500)
                        all_pawns.colour_index = all_players.avoid_finished_players(all_pawns.colour_index)
                        # STILL DISPLAY ROLL THE DICE
                    elif (self.steps != 6 and 0 in self.initial[all_pawns.colour_index]) or self.steps == 6:
                        self.next_step = True
                        self.roll_the_dice = False
                        self.choose_the_pawn = True
                # ------ END OF SECTION 1 -------
                # ------ SECTION 2 - CHOOSE PAWN NUMBER --------
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] and \
                        self.next_step and not self.pawn_number_choice:
                    if all_pawns.which_pawn_to_move(pygame.mouse.get_pos()) and \
                            self.initial[all_pawns.colour_index][all_pawns.pawn_number] != 2:
                        self.pawn_number_choice = True
                    else:
                        self.choose_other_pawn = True
                        self.choose_the_pawn = False
                # ------ END OF SECTION 2 ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    # ------ SECTION 3 - ASSIGN PLAYER NUMBER TO THE PARTICULAR COLOUR ------
                    elif self.initial_setup:
                        if event.key == pygame.K_UP:
                            if not self.confirm_setup:
                                prev_index = self.up_down_index
                            else:
                                self.confirm_setup = False
                            self.up_down_index = all_players.moving_player_to_colour(prev_index, self.up_down_index,
                                                                                     'up')
                        elif event.key == pygame.K_DOWN:
                            if not self.confirm_setup:
                                prev_index = self.up_down_index
                            else:
                                self.confirm_setup = False
                            self.up_down_index = all_players.moving_player_to_colour(prev_index, self.up_down_index,
                                                                                     'down')
                        elif event.key == pygame.K_RETURN:
                            self.confirm_setup = True
                            result = all_players.assign_player_to_colour()
                            prev_index = result[0]
                            self.up_down_index = result[0]
                            self.initial_setup = result[1]
                            self.roll_the_dice = result[2]

                    # ------ END OF SECTION 3 -------
            # ------ SECTION 4 - DISPLAY ALL THE GRAPHIC ELEMENTS -------
            self.draw_game_field(all_pawns, all_players)
            # ------ END OF SECTION 4 -------
            # ------ SECTION 5 - USER CHOSE THE PAWN NUMBER, CHECKING THE POSSIBILITY TO START MOVEMENT ------
            # ------ AFTER GAME STARTS TAKE COLOUR INDEX AS PLAYER INDEX
            if not self.initial_setup:
                all_players.player_index = all_pawns.colour_index
            if self.pawn_number_choice and not self.ready_to_move_phase_one and not self.game_over:
                # ------- SECTION 5.1 - PAWN IN BASE POSITION, NUMBER OF STEPS DRAWN = 6 ------
                start_position_available = True
                if self.initial[all_pawns.colour_index][all_pawns.pawn_number] == 1 and self.steps == 6:
                    # ------- CHECK IF THERE IS ANY PAWN WITH THE SAME COLOUR ON THE STARTING FIELD -------
                    start_position_available = all_pawns.start_pawn_position()
                    if not start_position_available:
                        # ------- STARTING POSITION TAKEN - CHECK WHICH PAWN USER SHOULD MOVE -------
                        if all_pawns.available_pawn_to_move(self.steps, start_position_available):
                            # ------ CHANGE PAWN -------
                            self.game_state_change_two = True
                            # FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS
                            self.choose_other_pawn = True
                            self.choose_the_pawn = False
                        else:
                            # ------ CHANGE PLAYER -> ROLL THE DICE  AND WHETHER POSSIBLE, CHOOSE PAWN -------
                            self.game_state_change_three = True
                            all_pawns.colour_index = all_players.avoid_finished_players(all_pawns.colour_index)
                            # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                            self.roll_the_dice = True
                            self.choose_other_pawn = False
                            self.choose_the_pawn = False
                    else:
                        # ------- STARTING POSITION FREE - MOVE PAWN TO THE STARTING FIELD -------
                        self.initial[all_pawns.colour_index][all_pawns.pawn_number] = 0
                        # ------- CHECK IF THERE IS A PAWN FROM ANOTHER PLAYER ON YOUR STARTING FIELD ------
                        pawn_to_home_pos = all_pawns.diff_colour_collision()
                        if pawn_to_home_pos[2]:
                            # ------- IF PAWN FROM ANOTHER PLAYER FOUND, MOVE IT BACK TO ITS BASE POSITION -------
                            self.initial[pawn_to_home_pos[0]][pawn_to_home_pos[1]] = 1
                            home_x = all_pawns.pawns_base_location[pawn_to_home_pos[0]][pawn_to_home_pos[1]][0]
                            home_y = all_pawns.pawns_base_location[pawn_to_home_pos[0]][pawn_to_home_pos[1]][1]
                            all_pawns.pawns[pawn_to_home_pos[0]][pawn_to_home_pos[1]].x = home_x
                            all_pawns.pawns[pawn_to_home_pos[0]][pawn_to_home_pos[1]].y = home_y
                        # ------ ROLL THE DICE  AND WHETHER POSSIBLE, CHOOSE PAWN -------
                        self.game_state_change_three = True
                        # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                        self.roll_the_dice = True
                        self.choose_the_pawn = False
                # ------- END OF SECTION 5.1 -------
                # ------- SECTION 5.2 - PAWN IN BASE POSITION, NUMBER OF STEPS DRAWN != 6 ------
                elif self.initial[all_pawns.colour_index][all_pawns.pawn_number] == 1 and self.steps != 6:
                    # ------- UNABLE TO START FROM BASE - CHECK WHICH PAWN USER COULD MOVE -------
                    if all_pawns.available_pawn_to_move(self.steps, start_position_available):
                        # ------ CHANGE PAWN -------
                        self.game_state_change_two = True
                        # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                        self.choose_other_pawn = True
                        self.choose_the_pawn = False
                # ------- END OF SECTION 5.2 -------
                # ------- SECTION 5.3 - PAWN IN THE GAME FIELD, ALL NUMBER OF STEPS VALID ------
                elif self.initial[all_pawns.colour_index][all_pawns.pawn_number] == 0 and 0 < self.steps <= 6:
                    # ------ GOOD TO START - PERMISSION TO MOVE TO THE 2ND PHASE OF VERIFICATION -------
                    self.ready_to_move_phase_one = True
                # ------- END OF SECTION 5.3 ---------
            # ------ SECTION 6 - POSSIBLE TO START MOVEMENT, CHECK WHETHER CHANGING POSITION IS VALID ------
            elif not self.found_target and self.pawn_number_choice and self.ready_to_move_phase_one:
                # ------- SECTION 6.1 - PAWN IS OUT OF THE BASE FIELD ------
                # ------- CHECK IF PAWN IS IN THE FINAL AREA [GREY STRAIGHT] -------
                possible_final_moves, in_final_area = all_pawns.final_straight(self.steps)
                team_collision = False
                # ------- IF NO RESTRAINTS FROM FINAL AREA - CALCULATE TARGET --------
                if (possible_final_moves and in_final_area) or (not possible_final_moves and not in_final_area):
                    self.found_target = all_pawns.calculate_target(self.steps)
                    # ------- CHECK IF THE TARGET COLLIDES WITH ONE OF THE PARTICULAR USER PAWNS -------
                    team_collision = all_pawns.same_colour_collision()
                # ------- SECTION 6.2 - TARGET FOUND, PERMISSION TO CHANGE POSITION, MOVE TO 3RD PHASE -------
                if ((not in_final_area) or (possible_final_moves and in_final_area)) and not team_collision:
                    self.ready_to_move_phase_two = True
                # ------- SECTION 6.3 - CHANGING POSITION NOT POSSIBLE -------
                elif team_collision or (in_final_area and not possible_final_moves):
                    self.found_target = False
                    if all_pawns.available_pawn_to_move(self.steps):
                        self.game_state_change_two = True
                        # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                        self.choose_other_pawn = True
                        self.choose_the_pawn = False
                    else:
                        self.game_state_change_three = True
                        all_pawns.colour_index = all_players.avoid_finished_players(all_pawns.colour_index)
                        # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                        self.roll_the_dice = True
                        self.choose_the_pawn = False
                        self.choose_other_pawn = False
                    # ------ GET BACK TO THE PHASE ONE VERIFICATION ------
                    self.ready_to_move_phase_one = False
            # ------- END OF SECTION 6 ---------
            # ------- SECTION 7 - MOVING PAWN TO THE SPECIFIED FIELD -------
            elif self.found_target and not self.ready_to_move_phase_three and self.ready_to_move_phase_two:
                index, self.ready_to_move_phase_three = all_pawns.move_to_specified_field(index)
            # ------- SECTION 8 - IF COLLISION WITH ANOTHER COLOUR, MOVE OPPONENTS PAWN TO THE BASE ------
            # ------- IF PAWN FINISHES ROUND - REMOVE FROM THE GAME FIELD AND INCREASE SCORE -------
            elif self.ready_to_move_phase_three:
                pawn_to_home_pos = all_pawns.diff_colour_collision()
                if pawn_to_home_pos[2]:
                    self.initial[pawn_to_home_pos[0]][pawn_to_home_pos[1]] = 1
                    home_x = all_pawns.pawns_base_location[pawn_to_home_pos[0]][pawn_to_home_pos[1]][0]
                    home_y = all_pawns.pawns_base_location[pawn_to_home_pos[0]][pawn_to_home_pos[1]][1]
                    all_pawns.pawns[pawn_to_home_pos[0]][pawn_to_home_pos[1]].x = home_x
                    all_pawns.pawns[pawn_to_home_pos[0]][pawn_to_home_pos[1]].y = home_y

                if all_pawns.disappear_after_completed_round():
                    self.initial[all_pawns.colour_index][all_pawns.pawn_number] = 2
                    # ------- UPDATE THE SCORE -------
                    all_players.player_score[all_pawns.colour_index] += 1
                    all_pawns.pawns[all_pawns.colour_index][all_pawns.pawn_number].x = 0
                    all_pawns.pawns[all_pawns.colour_index][all_pawns.pawn_number].y = 0
                    # ------- FIND OUT IF THE PLAYER FINISHED ALL FOUR ROUNDS -------
                    if all_players.player_score[all_pawns.colour_index] == 4:
                        all_players.playing_or_finished[all_pawns.colour_index] = 1
                        all_players.final_result.append(all_pawns.colour_index)

                if not any(score < 4 for score in all_players.player_score):
                    self.game_over = True
                else:
                    self.game_state_change_three = True
                    self.roll_the_dice = True
                    self.found_target = False
                    self.ready_to_move_phase_one = False
                    self.ready_to_move_phase_two = False
                    self.ready_to_move_phase_three = False
                    index = 0
                    if self.steps == 6 and all_players.playing_or_finished[all_pawns.colour_index] != 1:
                        all_pawns.colour_index = all_pawns.colour_index
                    else:
                        all_pawns.colour_index = all_players.avoid_finished_players(all_pawns.colour_index)
                # ------ FLAGS FOR CHANGING NOTIFICATION AND GAMEPLAY TIPS -------
                self.choose_the_pawn = False
                self.choose_other_pawn = False
                # ------ MOVE TO THE NEXT AVAILABLE PLAYER ------
            # ------ GAME STATE CHANGE SCENARIOS -------
            # ------ ROLL THE DICE AGAIN WITHOUT CHANGING PAWN NUMBER ------
            if self.game_state_change_one:
                self.next_step = False
            # ------ CHANGE PAWN NUMBER WITHOUT ROLLING THE DICE ------
            elif self.game_state_change_two:
                self.pawn_number_choice = False
            # ------ ROLL THE DICE AND CHANGE PAWN NUMBER ------
            elif self.game_state_change_three:
                self.next_step = False
                self.pawn_number_choice = False
            self.game_state_change_one = False
            self.game_state_change_two = False
            self.game_state_change_three = False
            # ------- END OF SECTION 8 ------

        pygame.quit()

    def draw_dice(self):
        # DICE
        WIN.blit(dices[self.steps - 1], (WIDTH + 80, SQUARE_SIZE * 10 + 1 + 15))
        pygame.display.update()

    def draw_menu(self, all_pawns, all_players):
        # --------------------------- MENU -------------------------------------
        c = [[GREEN, DARK_GREEN], [RED, DARK_RED], [BLUE, DARK_BLUE], [YELLOW, DARK_YELLOW]]
        # FONTS
        font = pygame.font.Font('freesansbold.ttf', 20)
        font_2 = pygame.font.Font('freesansbold.ttf', 15)
        font_3 = pygame.font.Font('freesansbold.ttf', 30)
        # SETUP TEXTS
        colour_names = ['GREEN', 'RED', 'BLUE', 'YELLOW']
        choosing_colour_texts = ["P" + str(i + 1) + " CHOOSE YOUR COLOUR" for i in range(4)]
        one_colour_left_to_choose_text = [" GETS " + colour_names[i] for i in range(4)]
        players_to_colour_texts = ["P" + str(i + 1) for i in range(4)]
        actions = ["PRESS -> [-SPACE-]", "CONFIRM -> [-ENTER-]", "CHOOSE COLOUR -> [-UP-] [-DOWN-]",
                   'PRESS -> [-LEFT MOUSE BUTTON-]']

        if self.initial_setup:
            highlight_player = ["GREY" for _ in range(4)]
            highlight_player[self.up_down_index] = WHITE
            c[self.up_down_index][1] = c[self.up_down_index][0]
            notification = font.render(choosing_colour_texts[all_players.player_index], True, WHITE, BLACK)
            choosing_colour_action = font_2.render(actions[2], True, GREY, BLACK)
            text_action = actions[1]
        else:
            highlight_player = ["GREY" for _ in range(4)]
            highlight_player[all_players.player_index] = WHITE
            c[all_players.player_index][1] = c[all_players.player_index][0]
            player_roll_dice_texts = ["P" + all_players.players_to_colours[i][-1] + " ROLL THE DICE" for i in range(4)]
            player_choose_pawn_texts = ["P" + all_players.players_to_colours[i][-1] + " CHOOSE THE PAWN" for i in
                                        range(4)]
            choose_another_pawn_texts = ["P" + all_players.players_to_colours[i][-1] + " CHOOSE OTHER PAWN" for i in
                                         range(4)]
            #finishing_first_texts = ["P" + all_players.players_to_colours[i][-1] + " YOU WON" for i in range(4)]
            #finishing_second_text = ["P" + all_players.players_to_colours[i][-1] + " 2nd PLACE" for i in range(4)]
            #finishing_third_text = ["P" + all_players.players_to_colours[i][-1] + " 3rd PLACE" for i in range(4)]
            #finishing_last_text = ["P" + all_players.players_to_colours[i][-1] + " 4th PLACE" for i in range(4)]
            # COLOUR NUMBERS
            for i in range(4):
                if i in all_players.final_result:
                    text_result = all_players.possible_places[all_players.final_result.index(i)][0]
                    text_colour = all_players.possible_places[all_players.final_result.index(i)][1]
                else:
                    text_result = ''
                    text_colour = BLACK
                color_one = font_2.render(text_result, True, text_colour, BLACK)
                color_one_rect = color_one.get_rect()
                color_one_rect.center = (WIDTH + 105, SQUARE_SIZE * (1.3 + (i * 1.5)) + 2 + 30)
                WIN.blit(color_one, color_one_rect)

            choosing_colour_action = font_2.render(actions[2], True, BLACK, BLACK)

            if self.roll_the_dice:
                text_notification = player_roll_dice_texts[all_players.player_index]
                text_action = actions[0]
            elif self.choose_the_pawn:
                text_notification = player_choose_pawn_texts[all_players.player_index]
                text_action = actions[3]
            elif self.choose_other_pawn:
                text_notification = choose_another_pawn_texts[all_players.player_index]
                text_action = actions[3]
            elif self.game_over:
                text_notification = 'GAME OVER'
                text_action = 'QUIT -> [ESC]'
            else:
                text_notification = ''
                text_action = ''
            notification = font.render(text_notification, True, WHITE, BLACK)
            if self.roll_the_dice:
                for i in range(4):
                    score_notification = font.render(str(all_players.player_score[i]), True, C[i], GREY)
                    score_notification_rect = score_notification.get_rect()
                    score_notification_rect.center = (all_pawns.final_fields[i][0] + 20, all_pawns.final_fields[i][1] + 20)
                    WIN.blit(score_notification, score_notification_rect)
        # COLOURS IN MENU

        pygame.draw.rect(WIN, c[0][1], pygame.Rect(WIDTH + 50, SQUARE_SIZE * 1 + 30, SQUARE_SIZE - 15, SQUARE_SIZE - 15))
        pygame.draw.rect(WIN, c[1][1],
                         pygame.Rect(WIDTH + 50, SQUARE_SIZE * 2.5 + 30, SQUARE_SIZE - 15, SQUARE_SIZE - 15))
        pygame.draw.rect(WIN, c[2][1], pygame.Rect(WIDTH + 50, SQUARE_SIZE * 4 + 30, SQUARE_SIZE - 15, SQUARE_SIZE - 15))
        pygame.draw.rect(WIN, c[3][1],
                         pygame.Rect(WIDTH + 50, SQUARE_SIZE * 5.5 + 30, SQUARE_SIZE - 15, SQUARE_SIZE - 15))

        circles = [(39, 39), (561, 39), (561, 561), (39, 561)]
        # PLAYER FOREGROUND COLOURS
        for i in range(4):
            pawns = font.render(all_players.players_to_colours[i], True, highlight_player[i], BLACK)
            pawns_rect = pawns.get_rect()
            pawns_rect.center = (WIDTH + 180, SQUARE_SIZE * (1.4 + i * 1.5) + 30)
            WIN.blit(pawns, pawns_rect)
            temp_str = str(all_players.players_to_colours[i])
            if len(temp_str) > 0:
                field_numbers = font_3.render(temp_str[-1], True, highlight_player[i], C[i])
            else:
                field_numbers = font_3.render(temp_str, True, highlight_player[i], C[i])
            field_numbers_rect = field_numbers.get_rect()
            field_numbers_rect.center = circles[i]
            WIN.blit(field_numbers, field_numbers_rect)

        notification_rect = notification.get_rect()
        notification_rect.center = (WIDTH + 150, SQUARE_SIZE * 7.5 + 1 + 30)
        WIN.blit(notification, notification_rect)

        choosing_colour_action_rect = choosing_colour_action.get_rect()
        choosing_colour_action_rect.center = (WIDTH + 150, SQUARE_SIZE - 5)
        WIN.blit(choosing_colour_action, choosing_colour_action_rect)

        dice_roll = font_2.render(text_action, True, GREY, BLACK)
        dice_roll_rect = dice_roll.get_rect()
        dice_roll_rect.center = (WIDTH + 150, SQUARE_SIZE * 8.5 + 1 + 30)
        WIN.blit(dice_roll, dice_roll_rect)

    def draw_game_field(self, all_pawns, all_players):

        # ------- SECTION 1 - STATIC OBJECTS -------

        # BACKGROUND FOR THE GAME FIELD AND MENU FIELD
        WIN.fill(WHITE, rect=(0, 0, WIDTH, HEIGHT))
        WIN.fill(BLACK, rect=(WIDTH, 0, 300, HEIGHT))

        # LINES FOR DIVIDING WINDOW INTO SQUARE FIELDS
        for i in range(NUM_OF_LINES):
            pygame.draw.line(WIN, BLACK, (0, (i * SQUARE_SIZE)), (WIDTH, (i * SQUARE_SIZE)), 1)
            pygame.draw.line(WIN, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 1)

        # SQUARE FIELDS FOR THE FINAL STRAIGHT IN EACH COLOUR
        for i in range(1, 6):
            if i == 1:
                pygame.draw.rect(WIN, GREEN, pygame.Rect((SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 6) + 1, SQUARE_SIZE - 1,
                                                         SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, GREEN, pygame.Rect((SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                                         SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, BLUE,
                                 pygame.Rect(560 - (SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 8) + 1, SQUARE_SIZE - 1,
                                             SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, BLUE,
                                 pygame.Rect(560 - (SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                             SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, RED, pygame.Rect((SQUARE_SIZE * 8) + 1, (SQUARE_SIZE * i) + 1, SQUARE_SIZE - 1,
                                                       SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, RED, pygame.Rect((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * i) + 1, SQUARE_SIZE - 1,
                                                       SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, YELLOW, pygame.Rect((SQUARE_SIZE * 6) + 1, 560 - (SQUARE_SIZE * i) + 1,
                                                          SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, YELLOW, pygame.Rect((SQUARE_SIZE * 7) + 1, 560 - (SQUARE_SIZE * i) + 1,
                                                          SQUARE_SIZE - 1, SQUARE_SIZE - 1))
            else:
                pygame.draw.rect(WIN, GREEN, pygame.Rect((SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                                         SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, BLUE,
                                 pygame.Rect(560 - (SQUARE_SIZE * i) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                             SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, RED, pygame.Rect((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * i) + 1, SQUARE_SIZE - 1,
                                                       SQUARE_SIZE - 1))
                pygame.draw.rect(WIN, YELLOW,
                                 pygame.Rect((SQUARE_SIZE * 7) + 1, 560 - (SQUARE_SIZE * i) + 1, SQUARE_SIZE - 1,
                                             SQUARE_SIZE - 1))

        # PAWNS STORAGE FIELDS
        pygame.draw.rect(WIN, GREEN, pygame.Rect(0, 0, 241, 241))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(40, 40, 160, 160))
        pygame.draw.rect(WIN, BLUE, pygame.Rect(360, 360, 241, 241))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(400, 400, 160, 160))
        pygame.draw.rect(WIN, RED, pygame.Rect(360, 0, 241, 241))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(400, 40, 160, 160))
        pygame.draw.rect(WIN, YELLOW, pygame.Rect(0, 360, 241, 241))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(40, 400, 160, 160))

        pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, SQUARE_SIZE,
                                                 SQUARE_SIZE))
        pygame.draw.rect(WIN, BLACK, pygame.Rect(561, 0, SQUARE_SIZE,
                                                 SQUARE_SIZE))
        pygame.draw.rect(WIN, BLACK, pygame.Rect(561, 561, SQUARE_SIZE,
                                                 SQUARE_SIZE))
        pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 561, SQUARE_SIZE,
                                                 SQUARE_SIZE))

        pygame.draw.circle(WIN, GREEN, (39, 39), 40)
        pygame.draw.circle(WIN, RED, (561, 39), 40)
        pygame.draw.circle(WIN, BLUE, (561, 561), 40)
        pygame.draw.circle(WIN, YELLOW, (39, 561), 40)

        # MIDDLE FIELDS OF THE BOARD
        # MIDDLE FIELD20
        pygame.draw.rect(WIN, GREY, pygame.Rect((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                                SQUARE_SIZE - 1))
        # GREEN
        pygame.draw.rect(WIN, GREY, pygame.Rect((SQUARE_SIZE * 6) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                                SQUARE_SIZE - 1))
        # BLUE
        pygame.draw.rect(WIN, GREY, pygame.Rect((SQUARE_SIZE * 8) + 1, (SQUARE_SIZE * 7) + 1, SQUARE_SIZE - 1,
                                                SQUARE_SIZE - 1))
        # RED
        pygame.draw.rect(WIN, GREY, pygame.Rect((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * 6) + 1, SQUARE_SIZE - 1,
                                                SQUARE_SIZE - 1))
        # YELLOW
        pygame.draw.rect(WIN, GREY, pygame.Rect((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * 8) + 1, SQUARE_SIZE - 1,
                                                SQUARE_SIZE - 1))
        # ------- END OF SECTION 1 -------

        # ------- SECTION 2 - PAWNS -------

        # FUNCTION for multiple pawns movement
        # INPUT: ALL THE PAWN OBJECTS (TEST FOR ONLY TWO),
        # END OF FUNCTION
        self.show_pawns(all_pawns.pawns)

        # ------- END OF SECTION 2 -------

        self.draw_menu(all_pawns, all_players)

        self.draw_dice()

        # ------- END OF SECTION 3 -------

        pygame.display.update()

    def default_positions(self, colour):
        if colour == 'r':
            WIN.blit(RED_PAWN, (self.corr[2], self.corr[0]))
            WIN.blit(RED_PAWN, (self.corr[3], self.corr[0]))
            WIN.blit(RED_PAWN, (self.corr[2], self.corr[1]))
            WIN.blit(RED_PAWN, (self.corr[3], self.corr[1]))
        elif colour == 'y':
            WIN.blit(YELLOW_PAWN, (self.corr[0], self.corr[2]))
            WIN.blit(YELLOW_PAWN, (self.corr[1], self.corr[2]))
            WIN.blit(YELLOW_PAWN, (self.corr[0], self.corr[3]))
            WIN.blit(YELLOW_PAWN, (self.corr[1], self.corr[3]))
        elif colour == 'b':
            WIN.blit(BLUE_PAWN, (self.corr[2], self.corr[2]))
            WIN.blit(BLUE_PAWN, (self.corr[3], self.corr[2]))
            WIN.blit(BLUE_PAWN, (self.corr[2], self.corr[3]))
            WIN.blit(BLUE_PAWN, (self.corr[3], self.corr[3]))
        elif colour == 'g':
            WIN.blit(GREEN_PAWN, (self.corr[0], self.corr[0]))
            WIN.blit(GREEN_PAWN, (self.corr[1], self.corr[0]))
            WIN.blit(GREEN_PAWN, (self.corr[0], self.corr[1]))
            WIN.blit(GREEN_PAWN, (self.corr[1], self.corr[1]))

    def show_pawns(self, pawn):
        locations = [[(self.corr[0], self.corr[0]), (self.corr[1], self.corr[0]), (self.corr[0], self.corr[1]),
                      (self.corr[1], self.corr[1])],
                     [(self.corr[2], self.corr[0]), (self.corr[3], self.corr[0]), (self.corr[2], self.corr[1]),
                  (self.corr[3], self.corr[1])],
                     [(self.corr[2], self.corr[2]), (self.corr[3], self.corr[2]), (self.corr[2], self.corr[3]),
                  (self.corr[3], self.corr[3])],
                     [(self.corr[0], self.corr[2]), (self.corr[1], self.corr[2]), (self.corr[0], self.corr[3]),
                  (self.corr[1], self.corr[3])]]

        all_true = True

        pawn_states = [x for x in range(3)]

        for x in self.initial:
            for y in x:
                if y == 0:
                    all_true = False
                    break

        if all_true:
            self.default_positions('g')
            self.default_positions('r')
            self.default_positions('b')
            self.default_positions('y')
        else:
            for i in range(4):
                for j in range(4):
                    if self.initial[i][j] == pawn_states[0]:
                        WIN.blit(self.colours[i], (pawn[i][j].x, pawn[i][j].y))
                    elif self.initial[i][j] == pawn_states[1]:
                        WIN.blit(self.colours[i], locations[i][j])


class Player:
    def __init__(self):
        self.players = ['PLAYER ' + str(i) for i in range(1, 5)]
        self.players_to_colours = ['' for _ in range(4)]
        self.player_score = [0 for _ in range(4)]
        self.player_index = 0
        self.players_to_colours[self.player_index] = self.players[self.player_index]
        self.playing_or_finished = [0 for _ in range(4)]
        self.possible_places = [(' 1 ', GOLD), (' 2 ', SILVER), (' 3 ', BRONZE), (' 4 ', GREY)]
        self.final_result = []

    def moving_player_to_colour(self, prev_index, up_down_index, direction):
        steps_to_next_colour = 0
        if self.player_index < 3:
            if direction == 'up':
                for i in range(prev_index - 1, prev_index - 4, -1):
                    steps_to_next_colour += 1
                    if self.players_to_colours[i] == '':
                        break
                if up_down_index - steps_to_next_colour >= 0:
                    up_down_index -= steps_to_next_colour
                elif up_down_index - steps_to_next_colour == -1:
                    up_down_index = 3
                elif up_down_index - steps_to_next_colour < -1:
                    temp = steps_to_next_colour - up_down_index
                    up_down_index = 3 - (temp - 1)
            elif direction == 'down':
                for i in range(prev_index + 1, prev_index + 4):
                    steps_to_next_colour += 1
                    if i > 3:
                        temp = i - 4
                    else:
                        temp = i
                    if self.players_to_colours[temp] == '':
                        break
                if up_down_index + steps_to_next_colour <= 3:
                    up_down_index += steps_to_next_colour
                elif up_down_index + steps_to_next_colour == 4:
                    up_down_index = 0
                elif up_down_index + steps_to_next_colour > 4:
                    temp = steps_to_next_colour - (3 - up_down_index)
                    up_down_index = 0 + (temp - 1)
            temp = self.players_to_colours[prev_index]
            self.players_to_colours[prev_index] = self.players_to_colours[up_down_index]
            self.players_to_colours[up_down_index] = temp
        return up_down_index

    def assign_player_to_colour(self):
        temp = 0
        if self.player_index < 3:
            self.player_index += 1
            for i in range(len(self.players_to_colours)):
                if self.players_to_colours[i] == '':
                    temp = i
                    break
            self.players_to_colours[temp] = self.players[self.player_index]
            return temp, True, False
        elif self.player_index == 3:
            self.player_index = 0
            return temp, False, True

    def avoid_finished_players(self, colour_index):
        found_next_player = False
        while not found_next_player:
            if colour_index < 3:
                colour_index += 1
            else:
                colour_index = 0
            if self.playing_or_finished[colour_index] == 0:
                found_next_player = True

        return colour_index


class Pawn:
    def __init__(self, home_corr):
        self.init_corr = [(8 * SQUARE_SIZE + 1, SQUARE_SIZE + 1), (SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1),
                          (13 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1), (6 * SQUARE_SIZE + 1, SQUARE_SIZE * 6 + 1)]
        self.pawns_base_location = [[(home_corr[0], home_corr[0]), (home_corr[1], home_corr[0]),
                                    (home_corr[0], home_corr[1]), (home_corr[1], home_corr[1])],
                                    [(home_corr[2], home_corr[0]), (home_corr[3], home_corr[0]),
                                    (home_corr[2], home_corr[1]), (home_corr[3], home_corr[1])],
                                    [(home_corr[2], home_corr[2]), (home_corr[3], home_corr[2]),
                                    (home_corr[2], home_corr[3]), (home_corr[3], home_corr[3])],
                                    [(home_corr[0], home_corr[2]), (home_corr[1], home_corr[2]),
                                    (home_corr[0], home_corr[3]), (home_corr[1], home_corr[3])]]
        self.final_fields = [((SQUARE_SIZE * 6) + 1, (SQUARE_SIZE * 7) + 1),
                             ((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * 6) + 1),
                             ((SQUARE_SIZE * 8) + 1, (SQUARE_SIZE * 7) + 1),
                             ((SQUARE_SIZE * 7) + 1, (SQUARE_SIZE * 8) + 1)]
        self.pawn_number = 0
        self.colour_index = 0
        self.pawns = []
        self.movement = []

    def which_pawn_to_move(self, mouse_location):
        # colour is given, so the search is rather simple.
        found = False
        for i in range(4):
            temp_x = self.pawns[self.colour_index][i].x
            temp_y = self.pawns[self.colour_index][i].y
            if temp_x <= mouse_location[0] <= temp_x + SQUARE_SIZE and \
                    temp_y <= mouse_location[1] <= temp_y + SQUARE_SIZE:
                self.pawn_number = i
                found = True
        return found

    def start_pawn_position(self):
        x, y = 0, 0
        start = True

        if self.colour_index == 1:
            x = self.init_corr[0][0]
            y = self.init_corr[0][1]
        elif self.colour_index == 0:
            x = self.init_corr[1][0]
            y = self.init_corr[1][1]
        elif self.colour_index == 2:
            x = self.init_corr[2][0]
            y = self.init_corr[2][1]
        elif self.colour_index == 3:
            x = self.init_corr[3][0]
            y = self.init_corr[2][0]

        for i in range(4):
            if self.pawns[self.colour_index][i].x == x and self.pawns[self.colour_index][i].y == y:
                start = False
                index = i

        if start:
            self.pawns[self.colour_index][self.pawn_number].x = x
            self.pawns[self.colour_index][self.pawn_number].y = y
        else:
            print(f"Move pawn {index + 1}")

        return start

    def initial_pawn_position(self):
        for j in range(4):
            four_pawns = []
            for i in range(4):
                pawn_x, pawn_y = self.pawns_base_location[self.colour_index + j][i]
                four_pawns.append(pygame.Rect(pawn_x, pawn_y, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
            self.pawns.append(four_pawns)

    def calculate_target(self, steps):
        points = self._define_points()
        target = [0, 0]
        temp_x = self.pawns[self.colour_index][self.pawn_number].x
        temp_y = self.pawns[self.colour_index][self.pawn_number].y
        temp_steps = steps
        self.movement = []

        while temp_steps > 0:
            x_add_cond_1 = temp_x < points[5][0] and temp_y == points[17][1]
            x_add_cond_2 = temp_x < points[18][0] and temp_y == points[15][1] and self.colour_index == 0
            x_add_cond_3 = points[5][0] <= temp_x < points[6][0] and temp_y == points[5][1] and self.colour_index != 1
            x_add_cond_4 = points[7][0] <= temp_x < points[8][0] and temp_y == points[8][1]
            x_add_cond_5 = points[5][0] <= temp_x < points[18][0] and temp_y == points[18][1] and self.colour_index == 1

            y_add_cond_1 = temp_y < points[15][1] and temp_x == points[18][0] and self.colour_index == 1
            y_add_cond_2 = points[6][1] <= temp_y < points[7][1] and temp_x == points[6][0]
            y_add_cond_3 = points[8][1] <= temp_y < points[9][1] and temp_x == points[8][0] and self.colour_index != 2
            y_add_cond_4 = points[10][1] <= temp_y < points[11][1] and temp_x == points[10][0]
            y_add_cond_5 = points[8][1] <= temp_y < points[20][1] and temp_x == points[8][0] and self.colour_index == 2

            x_sub_cond_1 = points[20][0] >= temp_x > points[21][0] and temp_y == points[20][1] and \
                           self.colour_index == 2
            x_sub_cond_2 = points[9][0] >= temp_x > points[22][0] and temp_y == points[10][1]
            x_sub_cond_3 = points[11][0] >= temp_x > points[12][0] and temp_y == points[12][1] and \
                           self.colour_index != 3
            x_sub_cond_4 = points[13][0] >= temp_x > points[14][0] and temp_y == points[14][1]
            x_sub_cond_5 = points[11][0] >= temp_x > points[22][0] and temp_y == points[22][1] and \
                           self.colour_index == 3

            y_sub_cond_1 = points[22][1] >= temp_y > points[15][1] and temp_x == points[23][0] and \
                           self.colour_index == 3
            y_sub_cond_2 = points[4][1] >= temp_y > points[5][1] and temp_x == points[5][0]
            y_sub_cond_3 = points[12][1] >= temp_y > points[13][1] and temp_x == points[13][0]
            y_sub_cond_4 = points[14][1] >= temp_y > points[17][1] and temp_x == points[17][0]

            # movement x++
            if x_add_cond_1 or x_add_cond_2 or x_add_cond_3 or x_add_cond_4 or x_add_cond_5:
                temp_x += 40
                temp_steps -= 1
                self.movement.append((temp_x, temp_y, 'right'))
            # movement y++
            elif y_add_cond_1 or y_add_cond_2 or y_add_cond_3 or y_add_cond_4 or y_add_cond_5:
                temp_y += 40
                temp_steps -= 1
                self.movement.append((temp_x, temp_y, 'down'))
            # movement x--
            elif x_sub_cond_1 or x_sub_cond_2 or x_sub_cond_3 or x_sub_cond_4 or x_sub_cond_5:
                temp_x -= 40
                temp_steps -= 1
                self.movement.append((temp_x, temp_y, 'left'))
            # movement y--
            elif y_sub_cond_1 or y_sub_cond_2 or y_sub_cond_3 or y_sub_cond_4:
                temp_y -= 40
                temp_steps -= 1
                self.movement.append((temp_x, temp_y, 'up'))

        if len(self.movement) != 0:
            return True
        else:
            return False

    def move_to_specified_field(self, index):
        done = False
        if index < len(self.movement):
            if self.movement[index][2] == 'right':
                self.pawns[self.colour_index][self.pawn_number].x += 10
            elif self.movement[index][2] == 'left':
                self.pawns[self.colour_index][self.pawn_number].x -= 10
            elif self.movement[index][2] == 'down':
                self.pawns[self.colour_index][self.pawn_number].y += 10
            elif self.movement[index][2] == 'up':
                self.pawns[self.colour_index][self.pawn_number].y -= 10

            if self.pawns[self.colour_index][self.pawn_number].x == self.movement[index][0] and \
                    self.pawns[self.colour_index][self.pawn_number].y == self.movement[index][1]:
                index += 1
                done = False

        elif index == len(self.movement):
            done = True

        return index, done

    def diff_colour_collision(self):
        collision_colour_index = 0
        collision_pawn_number = 0
        found = False
        for i in range(4):
            if i != self.colour_index:
                for j in range(4):
                    if self.pawns[self.colour_index][self.pawn_number] == self.pawns[i][j]:
                        collision_colour_index = i
                        collision_pawn_number = j
                        found = True

        return collision_colour_index, collision_pawn_number, found

    def same_colour_collision(self):
        collision = False
        destination = self.movement[-1][:2]
        if any((destination[0], destination[1]) ==
               (self.pawns[self.colour_index][i].x, self.pawns[self.colour_index][i].y) and i != self.pawn_number
               for i in range(4)):
            collision = True
        #for i in range(4):
        #    if i != self.pawn_number and destination[0] == self.pawns[self.colour_index][i].x and \
        #            destination[1] == self.pawns[self.colour_index][i].y:
        #        collision = True

        return collision

    def final_straight(self, steps):
        possible_move = False
        found_in_area = False
        max_steps = 0

        if self.colour_index == 0:
            for i in range(5):
                if self.pawns[self.colour_index][self.pawn_number].x == (SQUARE_SIZE + 1) + i * SQUARE_SIZE and \
                        self.pawns[self.colour_index][self.pawn_number].y == 1 + 7 * SQUARE_SIZE:
                    max_steps = 6 - (i + 1)
                    found_in_area = True
        elif self.colour_index == 1:
            for i in range(5):
                if self.pawns[self.colour_index][self.pawn_number].x == 1 + 7 * SQUARE_SIZE and \
                        self.pawns[self.colour_index][self.pawn_number].y == (SQUARE_SIZE + 1) + i * SQUARE_SIZE:
                    max_steps = 6 - (i + 1)
                    found_in_area = True
        elif self.colour_index == 2:
            for i in range(5):
                if self.pawns[self.colour_index][self.pawn_number].x == (13 * SQUARE_SIZE + 1) - (i * SQUARE_SIZE) \
                        and self.pawns[self.colour_index][self.pawn_number].y == 1 + 7 * SQUARE_SIZE:
                    max_steps = 6 - (i + 1)
                    found_in_area = True
        elif self.colour_index == 3:
            for i in range(5):
                if self.pawns[self.colour_index][self.pawn_number].x == 1 + 7 * SQUARE_SIZE and \
                        self.pawns[self.colour_index][self.pawn_number].y == (13 * SQUARE_SIZE + 1) - (
                        i * SQUARE_SIZE):
                    max_steps = 6 - (i + 1)
                    found_in_area = True

        if max_steps < steps:
            possible_move = False
        else:
            possible_move = True

        return possible_move, found_in_area

    def disappear_after_completed_round(self):
        if self.pawns[self.colour_index][self.pawn_number].x == self.final_fields[self.colour_index][0] and \
                self.pawns[self.colour_index][self.pawn_number].y == self.final_fields[self.colour_index][1]:
            return True
        else:
            return False

    def available_pawn_to_move(self, steps, start=True):
        available_pawns = []
        for i in range(4):
            if i != self.pawn_number:
                if (self.pawns[self.colour_index][i].x != self.pawns_base_location[self.colour_index][i][0] and
                    self.pawns[self.colour_index][i].y != self.pawns_base_location[self.colour_index][i][1] and
                    self.pawns[self.colour_index][i].x != 0 and self.pawns[self.colour_index][i].y != 0) or \
                        (self.pawns[self.colour_index][i].x == self.pawns_base_location[self.colour_index][i][0] and
                         self.pawns[self.colour_index][i].y == self.pawns_base_location[self.colour_index][i][1] and
                         steps == 6 and start):
                    available_pawns.append(i)
        if len(available_pawns) != 0:
            return True
        else:
            return False

    @staticmethod
    def _define_points():
        p_g = (1 * SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1)
        p_r = (8 * SQUARE_SIZE + 1, SQUARE_SIZE + 1)
        p_b = (13 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1)
        p_y = (6 * SQUARE_SIZE + 1, 13 * SQUARE_SIZE + 1)
        p_1 = (6 * SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1)
        p_2 = (6 * SQUARE_SIZE + 1, 1)
        p_3 = (8 * SQUARE_SIZE + 1, 1)
        p_4 = (8 * SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1)
        p_5 = (14 * SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1)
        p_6 = (14 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1)
        p_7 = (8 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1)
        p_8 = (8 * SQUARE_SIZE + 1, 14 * SQUARE_SIZE + 1)
        p_9 = (6 * SQUARE_SIZE + 1, 14 * SQUARE_SIZE + 1)
        p_10 = (6 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1)
        p_11 = (1, 8 * SQUARE_SIZE + 1)
        p_12 = (1, 7 * SQUARE_SIZE + 1)
        p_13 = (6 * SQUARE_SIZE + 1, 7 * SQUARE_SIZE + 1)
        p_14 = (1, 6 * SQUARE_SIZE + 1)
        p_15 = (7 * SQUARE_SIZE + 1, 1)
        p_16 = (7 * SQUARE_SIZE + 1, 6 * SQUARE_SIZE + 1)
        p_17 = (14 * SQUARE_SIZE + 1, 7 * SQUARE_SIZE + 1)
        p_18 = (8 * SQUARE_SIZE + 1, 7 * SQUARE_SIZE + 1)
        p_19 = (7 * SQUARE_SIZE + 1, 14 * SQUARE_SIZE + 1)
        p_20 = (7 * SQUARE_SIZE + 1, 8 * SQUARE_SIZE + 1)

        points = [p_g, p_r, p_b, p_y, p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14, p_15,
                  p_16, p_17, p_18, p_19, p_20]

        return points


g = GameWindow()
g.main()
