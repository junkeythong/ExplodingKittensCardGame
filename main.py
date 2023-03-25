from game import Game

if __name__ == "__main__":
    number_players = int(input("How many players are there? "))
    while number_players < 2 or number_players > 5:
        number_players = int(input("Please enter a valid number players (2 -> 5): "))
    game = Game(number_players)
    while True:
        game.play_turn()