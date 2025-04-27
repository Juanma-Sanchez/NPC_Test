from npc import NPC
import settings

if __name__ == "__main__":
    npc_list = [NPC(**npc_data) for npc_data in settings.NPC_DATA]
    while(True):
        text = input("Tu: ")
        output = npc_list[0].talk(None, text)
        print(npc_list[0].name + ':', output['response'])
        if 'item' in output:
            print('Has obtenido', output['item'])
        if not output['keep_talking']:
            print(npc_list[0].name, 'ya no quiere hablar contigo')
            break