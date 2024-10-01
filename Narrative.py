from asyncio.windows_events import NULL
from enum import Enum
import tkinter

class Narrative:
    
    def __init__(self):
        self.p1NarrativeSections: list[NarrativeSection] = []
        self.p2NarrativeSections: list[NarrativeSection] = []



class NarrativeSection:

    def __init__(self):
        self.narrativeText = ""
        self.choices: list[NarrativeChoice] = []
        #self.narrativeImage

class NarrativeChoice:
    
    def __init__(self):
        self.choiceText
        self.choiceType = ChoiceType.neutral
        #self.nextNarrativeSection: NarrativeSection = NULL

class ChoiceType(Enum):
    neutral = 0
    positive = 1
    negative = 2
    positiveHarmful = 3
    negativehelpful = 4
class Narrative:
    def __init__(self, narrativeText: str):
        self.story = narrativeText
        self.choices = []
        
    def getStory(self):
        
        return self.story
    
    def getChoices(self):
        return self.choices
    
    def addChoice(self, playerDecision: 'Decision'):
        from Decision import Decision
        self.choices.append(playerDecision)
        
    def removeChoice(self, playerDecision: 'Decision'):
        if playerDecision in self.choices:
            self.choices.remove(playerDecision)
        else:
            raise ValueError("This decision is not found in the list of choices")
        
        