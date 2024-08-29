import pygame
import sys

# Initialize Pygame
pygame.init()

# Define the map grid
MAP_GRID = [
    [None, None, None, 'medicine', None, None, None, None, None, None],
    [None, None, None, None, None, None, None, 'bad_route', None, None],
    [None, 'police', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, 'helper', None, None, None, None],
    [None, None, None, 'trap', None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, 'destination'],
    [None, None, None, None, None, None, 'bad_route', None, None, None],
    [None, 'trap', None, None, None, None, None, None, None, None],
    [None, None, None, 'helper', None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None]
]


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Quest to Save the Red Panda")

background = pygame.image.load("kidnapper.jpg").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))
background_start = pygame.image.load("explore.jpg").convert()
background_start = pygame.transform.scale(background_start, (screen_width, screen_height))


font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)
white = (255, 255, 255)
red = (255, 0, 0)

# Define the Map class
class Map:
    def __init__(self, map_grid, player):
        self.map_grid = map_grid
        self.player = player
        self.map_width = 150  # Smaller map width
        self.map_height = 150  # Smaller map height
        self.dot_size = 5
        self.font = pygame.font.Font(None, 15)  # Smaller font size

    def draw(self, screen):
        map_surface = pygame.Surface((self.map_width, self.map_height))
        map_surface.fill((50, 50, 50))  # Background color for the map

        for y, row in enumerate(self.map_grid):
            for x, location in enumerate(row):
                if location:
                    location_text = self.font.render(location, True, white)
                    map_surface.blit(location_text, (x * (self.map_width // len(row)), y * (self.map_height // len(self.map_grid))))

        # Draw player position as a dot
        player_x, player_y = self.player.position
        pygame.draw.circle(map_surface, red, (player_x * (self.map_width // len(self.map_grid[0])) + self.dot_size // 2, player_y * (self.map_height // len(self.map_grid)) + self.dot_size // 2), self.dot_size)

        # Display map in bottom-right corner
        screen.blit(map_surface, (screen.get_width() - self.map_width - 10, screen.get_height() - self.map_height - 10))

# Define Player class
class Player:
    def __init__(self):
        self.time = 24  # in hours
        self.health = 100  # in percentage
        self.power = 100  # in percentage
        self.resources = {'Food': 3, 'Water': 3, 'Medicine': 2}  # Inventory
        self.position = [0, 0]  # Starting position on the map

    def display_status(self, screen):
        time_text = font.render(f"Time: {self.time} hours", True, white)
        health_text = font.render(f"Health: {self.health}%", True, white)
        power_text = font.render(f"Power: {self.power}%", True, white)
        resources_text = font.render(f"Resources: {self.resources}", True, white)

        screen.blit(time_text, (50, 50))
        screen.blit(health_text, (50, 100))
        screen.blit(power_text, (50, 150))
        screen.blit(resources_text, (50, 200))

    def update_status(self, time_change, health_change, power_change):
        print(f"Updating status: Time Change={time_change}, Health Change={health_change}, Power Change={power_change}")
        self.time += time_change
        self.health += health_change
        self.power += power_change

        # Cap the values
        self.health = min(max(self.health, 0), 100)
        self.power = min(max(self.power, 0), 100)
        self.time = max(self.time, 0)
        print(f"Updated Player Status: Time={self.time}, Health={self.health}, Power={self.power}")

# Define Game class
# Define Game class
# Define Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.map = Map(MAP_GRID, self.player)
        self.storyline = [
            "You receive an urgent call about a captured red panda.",
            "You must secure permits in Kathmandu. This takes time.",
            "You set off on a treacherous journey through the mountains.",
            "You encounter a scammer posing as a local guide.",
            "You reach a local village where you can gather intel.",
            "You approach the poachers' hideout for the final showdown."
        ]
        self.current_stage = 0
        self.options = ["Option A", "Option B", "Option C", "Option D"]
        self.questions = [
            {
                "question": "You encounter a wild animal in the jungle. What is the best first aid treatment for a bite from a venomous snake?",
                "options": ["Apply a tourniquet above the bite", "Wash the bite area with soap and water",
                            "Suck out the venom with your mouth", "Apply ice to the bite area"],
                "answer_weights": [
                    {"health": -50, "time": 0},  # Incorrect and dangerous
                    {"health": 20, "time": 0},  # Correct
                    {"health": -30, "time": 0},  # Incorrect
                    {"health": -10, "time": 0}  # Suboptimal
                ]
            },
            {
                "question": "You’re in Kathmandu and notice heavy pollution. What is a common traditional remedy used to help purify the air inside homes?",
                "options": ["Burning incense sticks", "Using air purifiers", "Closing all windows tightly",
                            "Spraying air fresheners"],
                "answer_weights": [
                    {"health": 10, "time": 0},  # Traditional and common remedy
                    {"health": 5, "time": -5},  # Effective but not traditional
                    {"health": 0, "time": -10},  # Incorrect, increases indoor pollution
                    {"health": 0, "time": -5}  # Suboptimal, temporary effect
                ]
            },
            {
                "question": "In the jungle, which herb is known to be poisonous and should be avoided?",
                "options": ["Himalayan Yew", "Nettle", "Mint", "Chamomile"],
                "answer_weights": [
                    {"health": -40, "time": 0},  # Correct (poisonous)
                    {"health": -10, "time": 0},  # Suboptimal, can cause irritation
                    {"health": 10, "time": 0},  # Correct and safe herb
                    {"health": 10, "time": 0}  # Correct and safe herb
                ]
            },
            {
                "question": "What is a common practice in Kathmandu to reduce the impact of traffic pollution?",
                "options": ["Using electric vehicles", "Driving with windows open", "Walking instead of driving",
                            "Using public transport"],
                "answer_weights": [
                    {"health": 10, "time": -5},  # Correct, reduces pollution
                    {"health": -5, "time": -5},  # Incorrect, increases exposure
                    {"health": 10, "time": 0},  # Correct, reduces pollution and exercise benefits
                    {"health": 15, "time": -5}  # Correct, widely recommended
                ]
            },
            {
                "question": "You encounter a scammer in Kathmandu. What is a good way to identify if someone is a scammer?",
                "options": ["Verify their credentials through official sources", "Give them immediate money to be safe",
                            "Avoid eye contact", "Agree to all their demands"],
                "answer_weights": [
                    {"health": 0, "time": -5},  # Correct approach
                    {"health": -20, "time": -10},  # Incorrect, encourages scamming
                    {"health": -10, "time": 0},  # Suboptimal, avoids but doesn't solve
                    {"health": -30, "time": -15}  # Incorrect, puts you at risk
                ]
            },
            {
                "question": "Which area in Nepal is known to be particularly prone to landslides during the monsoon season?",
                "options": ["Langtang Valley", "Kathmandu Valley", "Chitwan", "Lumbini"],
                "answer_weights": [
                    {"health": 0, "time": -10},  # Correct, highly prone
                    {"health": -10, "time": 0},  # Incorrect, less prone
                    {"health": -5, "time": 0},  # Incorrect, less prone
                    {"health": -5, "time": 0}  # Incorrect, least prone
                ]
            },
            {
                "question": "In a remote village, how can you effectively gain assistance from the locals?",
                "options": ["Offer them something in return", "Speak aggressively to get their attention",
                            "Ignore their customs and traditions", "Demand help immediately"],
                "answer_weights": [
                    {"health": 0, "time": -5},  # Correct, mutual respect
                    {"health": -20, "time": -10},  # Incorrect, causes hostility
                    {"health": -15, "time": -5},  # Incorrect, offensive
                    {"health": -25, "time": -15}  # Incorrect, very rude
                ]
            },
            {
                "question": "Mad honey is a unique product from Nepal. How does it generally affect your health?",
                "options": ["Increases health but may cause hallucinations", "Decreases health quickly",
                            "Has no effect on health", "Increases energy but reduces health"],
                "answer_weights": [
                    {"health": 20, "time": -10},  # Correct but with side effects
                    {"health": -20, "time": 0},  # Incorrect, harmful
                    {"health": 0, "time": 0},  # Incorrect, neutral
                    {"health": 10, "time": -5}  # Suboptimal, mixed effects
                ]
            },
            {
                "question": "Which season is considered the best for trekking in Nepal due to clear skies and moderate temperatures?",
                "options": ["Winter", "Summer", "Monsoon", "Autumn"],
                "answer_weights": [
                    {"health": -10, "time": -5},  # Incorrect, cold and harsh
                    {"health": -5, "time": -5},  # Incorrect, hot and humid
                    {"health": -20, "time": -10},  # Incorrect, rains and landslides
                    {"health": 10, "time": 0}  # Correct, best trekking season
                ]
            },
            {
                "question": "What should you do if you encounter a snow leopard while trekking in the mountains?",
                "options": ["Stay calm and slowly back away", "Run away quickly", "Make loud noises to scare it",
                            "Try to fight it off"],
                "answer_weights": [
                    {"health": 0, "time": -10},  # Correct, non-threatening response
                    {"health": -30, "time": -15},  # Incorrect, dangerous
                    {"health": -10, "time": -5},  # Suboptimal, might provoke
                    {"health": -40, "time": -20}  # Incorrect, highly dangerous
                ]
            }
        ]
        self.current_question_index = 0
        self.questions_asked = 0

    def display_options(self, screen):
        for i, option in enumerate(self.options):
            option_text = font.render(f"{i + 1}. {option}", True, white)
            screen.blit(option_text, (50, 400 + i * 40))

    def display_question(self, screen, question_data):
        question_text = font.render(question_data["question"], True, white)
        screen.blit(question_text, (50, 350))
        for i, option in enumerate(question_data["options"]):
            option_text = font.render(f"{i + 1}. {option}", True, white)
            screen.blit(option_text, (50, 400 + i * 40))

    def check_answer(self, choice, question_data):
        # Retrieve the effect of the chosen option from answer_weights
        effect = question_data["answer_weights"][choice]
        if effect["health"] > 0:  # Assuming positive health means correct
            print("Correct answer!")
            correct = True
        else:
            print("Incorrect answer!")
            correct = False
        return correct, effect

    def apply_effects(self, effect):
        # Directly use the effects from answer_weights
        self.player.update_status(effect.get("time", 0), effect.get("health", 0), 0)

        # Check for game-over conditions and stop the game loop immediately
        if self.player.health <= 0:
            print("Game Over! Your health has dropped to zero.")
            pygame.quit()
            sys.exit()  # Exit the game
        elif self.player.time <= 0:
            print("Game Over! You've run out of time.")
            pygame.quit()
            sys.exit()  # Exit the game

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle key events specifically on key down
                elif event.type == pygame.KEYDOWN:
                    if self.current_question_index < len(self.questions):
                        question_data = self.questions[self.current_question_index]
                        if event.key == pygame.K_1:
                            correct, effect = self.check_answer(0, question_data)
                            self.apply_effects(effect)
                            self.current_question_index += 1
                        elif event.key == pygame.K_2:
                            correct, effect = self.check_answer(1, question_data)
                            self.apply_effects(effect)
                            self.current_question_index += 1
                        elif event.key == pygame.K_3:
                            correct, effect = self.check_answer(2, question_data)
                            self.apply_effects(effect)
                            self.current_question_index += 1
                        elif event.key == pygame.K_4:
                            correct, effect = self.check_answer(3, question_data)
                            self.apply_effects(effect)
                            self.current_question_index += 1
                    else:
                        # Display storyline and options once all questions are answered
                        if event.key == pygame.K_1:
                            self.next_stage(0)
                        elif event.key == pygame.K_2:
                            self.next_stage(1)
                        elif event.key == pygame.K_3:
                            self.next_stage(2)
                        elif event.key == pygame.K_4:
                            self.next_stage(3)

            # Render the screen
            screen.blit(background, (0, 0))

            if self.current_question_index < len(self.questions):
                question_data = self.questions[self.current_question_index]
                self.display_question(screen, question_data)
            else:
                storyline_text = font.render(self.storyline[self.current_stage], True, white)
                screen.blit(storyline_text, (50, 350))
                self.display_options(screen)

            self.player.display_status(screen)
            self.map.draw(screen)  # Draw the map in the bottom-right corner

            pygame.display.flip()

            # Check for game-over conditions
            if self.player.health <= 0:
                print("Game Over! Your health has dropped to zero.")
                running = False

            elif self.player.time <= 0:
                print("Game Over! You've run out of time.")
                running = False

            elif self.player.position == [9, 9] and self.player.health > 0 and self.player.time > 0:
                print("Congratulations! You've saved the red panda!")
                running = False

    def next_stage(self, choice):
        if self.current_stage < len(self.storyline) - 1:
            self.current_stage += 1
            print(f"You chose: {self.options[choice]}")
            self.player.update_status(time_change=-2, health_change=-10, power_change=-5)
            # Move player to a new position based on choice
            self.update_player_position(choice)
        else:
            print("Congratulations! You've reached the final stage!")
            pygame.quit()
            sys.exit()

    def update_player_position(self, choice):
        # Example of moving player; logic can be adjusted based on game design
        if choice == 0:  # Option A - move right
            self.player.position[0] = min(self.player.position[0] + 1, 9)
        elif choice == 1:  # Option B - move down
            self.player.position[1] = min(self.player.position[1] + 1, 9)
        elif choice == 2:  # Option C - move left
            self.player.position[0] = max(self.player.position[0] - 1, 0)
        elif choice == 3:  # Option D - move up
            self.player.position[1] = max(self.player.position[1] - 1, 0)

class StartScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)

    def display(self, screen):
        screen.blit(background_start, (0, 0))
        title_text = self.font.render("Explore the universe through our Lenses", True, white)
        instruction_text = font.render("Press Enter to Start", True, white)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - title_text.get_height()))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + 50))

        pygame.display.flip()

# Main execution
if __name__ == "__main__":
    start_screen = StartScreen()
    game = Game()

    # Start screen loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.play()
                    break

        start_screen.display(screen)