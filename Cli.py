# class Player:
#     def __init__(self):
#         self.time = 24  # in hours
#         self.health = 100  # in percentage
#         self.power = 100  # in percentage
#         self.resources = {'Food': 3, 'Water': 3, 'Medicine': 2}  # Inventory
#
#     def display_status(self):
#         time_icon = "⏳"
#         health_icon = "❤️"
#         power_icon = "⚡"
#         resource_icon = "📦"
#
#         print(f"{time_icon} Time: {self.time} hours")
#         print(f"{health_icon} Health: {self.health}%")
#         print(f"{power_icon} Power: {self.power}%")
#         print(f"{resource_icon} Resources: {self.resources}")
#
#
# class Game:
#     def __init__(self):
#         self.player = Player()
#         self.storyline = [
#             "You receive an urgent call about a captured red panda.",
#             "You must secure permits in Kathmandu. This takes time.",
#             "You set off on a treacherous journey through the mountains.",
#             "You encounter a scammer posing as a local guide.",
#             "You reach a local village where you can gather intel.",
#             "You approach the poachers' hideout for the final showdown."
#         ]
#
#     def play(self):
#         for event in self.storyline:
#             print("\n" + event)
#             self.player.display_status()
#             self.make_choice()
#
#     def make_choice(self):
#         choice = input("\nChoose an action (e.g., 'Proceed', 'Rest', 'Use resource'): ").lower()
#
#         if "proceed" in choice:
#             self.player.time -= 2  # Deduct time for progressing
#             print("You proceed further into your journey, time is ticking...")
#         elif "rest" in choice:
#             self.player.health += 10  # Boost health if resting
#             self.player.time -= 1  # Resting also consumes time
#             print("You take a moment to rest and recover some health.")
#         elif "use" in choice:
#             resource = input("Which resource do you want to use? (Food/Water/Medicine): ").capitalize()
#             if self.player.resources.get(resource, 0) > 0:
#                 if resource == 'Food':
#                     self.player.health += 5
#                 elif resource == 'Water':
#                     self.player.power += 5
#                 elif resource == 'Medicine':
#                     self.player.health += 20
#                 self.player.resources[resource] -= 1
#                 print(f"You used {resource}.")
#             else:
#                 print(f"You have no {resource} left.")
#         else:
#             print("Invalid choice, please try again.")
#
#         # Simulate consequences (example)
#         self.player.health -= 10  # Deduct health for progress
#
#         # Check for end conditions
#         if self.player.time <= 0 or self.player.health <= 0:
#             print("\nGame Over! You've run out of time or health.")
#             exit()
#
# if __name__ == "__main__":
#     game = Game()
#     game.play()
#
#
# import tkinter as tk
#
# class GameGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("The Quest to Save the Red Panda")
#         self.player = Player()
#
#         # Create Labels
#         self.time_label = tk.Label(root, text=f"Time: {self.player.time} hours")
#         self.time_label.pack()
#
#         self.health_label = tk.Label(root, text=f"Health: {self.player.health}%")
#         self.health_label.pack()
#
#         self.power_label = tk.Label(root, text=f"Power: {self.player.power}%")
#         self.power_label.pack()
#
#         self.resources_label = tk.Label(root, text=f"Resources: {self.player.resources}")
#         self.resources_label.pack()
#
#         # Create Buttons
#         self.proceed_button = tk.Button(root, text="Proceed", command=self.proceed)
#         self.proceed_button.pack()
#
#         self.rest_button = tk.Button(root, text="Rest", command=self.rest)
#         self.rest_button.pack()
#
#         self.use_resource_button = tk.Button(root, text="Use Resource", command=self.use_resource)
#         self.use_resource_button.pack()
#
#     def update_status(self):
#         self.time_label.config(text=f"Time: {self.player.time} hours")
#         self.health_label.config(text=f"Health: {self.player.health}%")
#         self.power_label.config(text=f"Power: {self.player.power}%")
#         self.resources_label.config(text=f"Resources: {self.player.resources}")
#
#     def proceed(self):
#         self.player.time -= 2
#         self.player.health -= 10
#         self.update_status()
#
#     def rest(self):
#         self.player.health += 10
#         self.player.time -= 1
#         self.update_status()
#
#     def use_resource(self):
#         # Implementation of resource usage
#         pass
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     game = GameGUI(root)
#     root.mainloop()