import random
from npc import NPC

class NPCList:
    def __init__(self, npc_list:list):
        self.available_npcs = npc_list
        self.non_available_npcs = []
        self.determine_sight_npcs()
        self.selected_npc = None

    def determine_sight_npcs(self):
        if not self.available_npcs:
            self.available_npcs = self.non_available_npcs
            self.non_available_npcs = []
        self.sight_npcs = random.sample(
            self.available_npcs,
            min(3, len(self.available_npcs))
        )
    
    def select_npc(self, npc:NPC):
        self.available_npcs.remove(npc)
        self.non_available_npcs.append(npc)
        self.selected_npc = npc
    
    def unselect_npc(self):
        self.selected_npc = None
        self.determine_sight_npcs()
