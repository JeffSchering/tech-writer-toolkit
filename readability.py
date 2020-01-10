#!/usr/bin/env python

from toolkit import Readability
import PySimpleGUI as sg
import re

r = Readability()
results = {}

sg.change_look_and_feel('GreenTan')

layout = [  [sg.Text('Paste your text here',font='verdana')],
            [sg.Multiline(size=(80,20),font='verdana',key='INPUT',enable_events=True)],
            [sg.Multiline(size=(80,8),font='verdana',key='OUTPUT',background_color='#9FB8AD',disabled=True)],
            [sg.Submit(font='verdana'), sg.Text(' '*180), sg.Exit(font='verdana')]]

window = sg.Window('Readability', layout, finalize=True, return_keyboard_events=True)

def submit(text):

    if re.match(r'^\s*$',text): # ignore text that's all whitespace
        return

    s =  'Flesch-Kincaid Grade Level: {:.2f}\n'.format(r.flesch_kincaid_grade_level(text))
    s += 'Flesch Reading Ease Score: {:.2f}\n'.format(r.flesch_reading_ease(text))
    s += 'Total words: {}\n'.format(r.total_words)
    s += 'Total sentences: {}\n'.format(r.total_sentences)
    s += 'Total Syllables: {}\n'.format(r.total_syllables)
    s += 'Avg words/sentence: {:.2f}\n'.format(r.words_per_sentence)
    s += 'Avg syllables/word: {:.2f}'.format(r.syllables_per_word)

    window['OUTPUT'].Update(s, background_color='#9FB8AD') #9FB8AD is green for GreenTan theme

# Main loop. Doesn't exit until user clicks the Exit button, or clicks the
# Window close button, or presses Ctrl-E
while True:

    event, values = window.Read()

    if event == 'Submit' or event == 's:83': # Ctrl-S
        submit(values['INPUT'])
    elif event in ('Exit',None,'e:69'):
        break
    else:
        pass

window.close()
del window

