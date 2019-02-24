import json

from interactive_npc import NPCStateMachine
from settings import NPC_JSON


class MyNPC(NPCStateMachine):
    LAST_STATE = 'Cooperative'

    def __init__(self, default_state='Neutral'):
        super().__init__(default_state=default_state)

    def is_last_state(self):
        return self._current_state == self.LAST_STATE

    def bribe(self, quantity):
        pass

    def attack(self):
        pass

    def tell(self, text):
        sentiment = self._get_sentiment(text)
        entities = self._get_entities(text)
        inputs = {
            'sentiment': MyNPC.randomize(sentiment, 0.1),
            'entities': entities
        }
        self._get_next_state(inputs)

    @classmethod
    def create_from_dict(cls, dict: dict):
        my_npc = MyNPC()
        for state in dict['states']:
            my_npc._add_state(state['name'],state['value'],state['next_states'])

        return my_npc

if __name__ == "__main__":
    f = open(NPC_JSON, 'r')
    npc_dict = json.load(f)
    npc =MyNPC.create_from_dict(npc_dict)
    f.close()
    print('NPC:', npc.current_state.value)
    while(not npc.is_last_state()):
        user_input = input('Tu: ')
        npc.tell(user_input)
        print('NPC:', npc.current_state.value)