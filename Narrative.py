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