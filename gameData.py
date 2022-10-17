#REGINALD HUEY TAN IAN JAY (S10239913) - IT01 (P01)

#====================== GAME FIELD ======================
field = [[[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
         [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
         [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
         [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
         [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]]

#====================== GAME VARIABLES ======================
game_vars = {
    'turn': 1,  # Current Turn
    'monster_kill_target': 20,  # Number of kills needed to win
    'monsters_killed': 0,  # Number of monsters killed so far
    'num_monsters': 0,  # Number of monsters in the field
    'gold': 10,  # Gold for purchasing units
    'threat': 10, # Current threat metre level
    'max_threat': 10,  # Length of threat metre
    'danger_level': 1,  # Rate at which threat increases
    'gold_increase_by_turn': 1, #How much the player's gold increases every turn
    'game_lost': False, #Boolean flag to end game
    'monster_end_game': 'Zombie', #Monster that ends the game
    'defender_spawn_boundary': 3, #How many tiles in each lane can be used for the spawning of defender units
    'timed': False, #boolean flag for timed mode
    'time_out_chance': 3, #number of "lives" player has in timed mode
}

#====================== UNITS (DEFENDERS + MONSTERS) ======================
defender_list = ['ARCHR', 'WALL', 'CANON', 'NINJA']
monster_list = ['ZOMBI', 'WWOLF']

defenders = {
            'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                      'upgrade_cost': 8,
                      'level': 1,
                       },
            'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      'upgrade_cost': 6,
                      'level': 1,
                      },
            'CANON': {'name': 'Cannon',
                       'maxHP': 8,
                       'min_damage': 3,
                       'max_damage': 5,
                       'price': 7,
                     },
            'NINJA': {'name': 'Ninja',
                       'maxHP': 10,
                       'min_damage': 5,
                       'max_damage': 9,
                       'price': 1,
                       },
             }
monsters = {
            'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves': 1,
                      'reward': 2
                      },
            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves': 2,
                      'reward': 3
                      },
            }

#====================== GLOBAL VARIABLES ======================
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
turnEvents = []

#==================================== CREDITS =====================================
#Music I Used: https://www.bensound.com/free-music-for-videos
