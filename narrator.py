from npc_list import NPCList
from npc import NPC
from player import Player


class Narrator:
    def __init__(self, npc_list: NPCList):
        self.npc_list = npc_list

    @property
    def talkable_npcs(self):
        return self.npc_list.sight_npcs

    @property
    def selected_npc(self) -> NPC:
        return self.npc_list.selected_npc
    
    def start_game(self, player:Player):
        while True:
            if self.selected_npc:
                text = input("Tu: ")
                output = self.selected_npc.talk(player, text)
                print(self.selected_npc.name.capitalize() + ':', output['response'])
                if 'item' in output:
                    print('Has obtenido', output['item'])
                    self.selected_npc.give_item(output['item'])
                    player.obtain(output['item'])
                if not output['keep_talking']:
                    print('Narrador:', self.selected_npc.name.capitalize(), 'ya no quiere hablar contigo')
                    self.npc_list.unselect_npc()
            else:
                print(
                    'Narrador: Puedes ver a {}. ¿Quieres hablar con alguien o salir?'.format(
                        '{} {}'.format(
                            'un' if self.talkable_npcs[0].gender == 'M' else 'una',
                            self.talkable_npcs[0].name
                        ) if len(self.talkable_npcs) == 1 else '{} y {} {}'.format(
                            ', '.join(
                                [
                                    '{} {}'.format(
                                        'un' if npc.gender == 'M' else 'una',
                                        npc.name
                                    ) for npc in self.talkable_npcs[:-1]
                                ]
                            ),
                            'un' if self.talkable_npcs[-1].gender == 'M' else 'una',
                            self.talkable_npcs[-1].name
                        )
                    )
                )
                user_input = input('Tu: ')
                if 'salir' in user_input.lower():
                    print(
                        '\nGracias por jugar. {}'.format(
                            'No has conseguido mingún objeto.' if len(
                                player.inventory
                            ) == 0 else 'Has conseguido los siguientes objetos:'
                        )
                    )
                    for item in player.inventory:
                        print(item)
                    break
                else:
                    for npc in self.talkable_npcs:
                        if npc.name in user_input.lower():
                            self.npc_list.select_npc(npc)
                            print("Narrador: te diriges a hablar con {} {}.".format(
                                'el' if self.selected_npc.gender == 'M' else 'la',
                                self.selected_npc.name
                            ))
                    if not self.selected_npc:
                        print('Narrador: Me temo que no entiendo que quieres hacer.')