from random import random
from typing import List
import os
import platform

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from settings import PATH

class Condition:
    def __init__(self, condition_type=None, value=None, name=None):
        self.name = name
        self.condition_type = condition_type
        self.value = value

    def is_met(self, input):
        if self.condition_type == 'contains':
            return self.value in input
        elif self.condition_type == 'threshold':
            return self.value[0] < input < self.value[1]
        elif self.condition_type == 'equals':
            return self.value == input
        elif self.condition_type == 'differs':
            return self.value != input

        else:
            return False

class NextState:
    def __init__(self, name=None, conditions: List[Condition]=[]):
        self.name = name
        self.conditions = conditions

    def add_condition(self, name=None, type=None, value=None):
        self.conditions.append(
            Condition(name=name, condition_type=type, value=value)
        )

    def are_conditions_met(self, inputs: dict={}):
        for condition in self.conditions:
            if not condition.is_met(inputs[condition.name]):
                return False

        return True

class State:
    def __init__(self, value=None, next_states: List[NextState]=[]):
        self.value = value
        self.next_states = next_states

    def add_next_state(self, name=None, conditions: List[dict]=[]):
        self.next_states.append(
            NextState(name=name, conditions=[])
        )
        for condition in conditions:
            self.next_states[-1].add_condition(
                name=condition['name'],
                type=condition['type'],
                value=condition['value']
            )

    def get_next_state(self, inputs: dict):
        for possible_next_state in self.next_states:
            if possible_next_state.are_conditions_met(inputs):
                return possible_next_state.name

        return None

class NPCStateMachine:
    def __init__(self, default_state=None, states: dict={}):
        self._current_state = default_state
        self.states = states

        if platform.system() == 'Windows':
            from pathlib import Path

            FULL_PATH = str(Path().absolute()) + '\\' + PATH
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  FULL_PATH
        else:
            FULL_PATH = '"' + os.getcwd() + '/' + PATH +'"'
            os.system['GOOGLE_APPLICATION_CREDENTIALS'] = FULL_PATH

        self.client = language.LanguageServiceClient()


    def _add_state(self, name=None, value=None, next_states: List[dict] = []):
        self.states[name] = State(value=value, next_states=[])
        for next_state in next_states:
            self.states[name].add_next_state(
                name=next_state['name'],
                conditions=next_state['conditions']
            )

    @property
    def current_state(self)->State:
        return self.states[self._current_state]

    def _get_next_state(self, inputs: dict={}):
        next_state = self.current_state.get_next_state(inputs)
        if next_state:
            self._current_state = next_state

    def _get_sentiment(self, text):
        document = types.Document(
            content=text,
            language='es',
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment = self.client.analyze_sentiment(document=document).document_sentiment
        return sentiment.score

    def _get_entities(self, text):
        document = types.Document(
            content=text,
            language='es',
            type=enums.Document.Type.PLAIN_TEXT)

        response = self.client.analyze_entities(
            document=document,
            encoding_type='UTF8'
        )
        return [entity.name for entity in response.entities]

    @staticmethod
    def penalize(input, probability):
        return input * (1 - probability*random())

    @staticmethod
    def randomize(input, probability):
        return input * (1 + probability * (random() - random()))