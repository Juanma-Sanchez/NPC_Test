from narrator import Narrator
from npc_list import NPCList
from npc import NPC
from player import Player
import settings

if __name__ == "__main__":
    player = Player(**settings.PLAYER_DATA)
    narrator = Narrator(
        NPCList(
            [
                NPC(**npc_data) for npc_data in settings.NPC_DATA
            ]
        )
    )
    print(
          "Bienvenido.",
          "Eres un joven purificador en la ciudad de Leukopolis, puedes hablar con quien encuentres para obtener información y objetos.",
          "\n"
    )
    narrator.start_game(player)