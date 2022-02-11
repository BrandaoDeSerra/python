# -*- coding: utf-8 -*-
import pyautogui  # https://pyautogui.readthedocs.io/en/latest/quickstart.html
import time
from pandas import read_excel
import pyperclip

# COmo gerar o executavel
# pyinstaller --noconsole --onefile rpaContatoTeams.py
# Feeback
#
pyautogui.PAUSE = 0.5
base = read_excel("eid_teams.xlsx")


def writeMsg(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')


def tempoNow():
    hora = time.localtime().tm_hour
    saudacao = 'Boa noite'
    if hora >= 0 and hora < 12:
        saudacao = 'Bom dia'
    elif hora >= 12 and hora < 18:
        saudacao = 'Boa tarde'
    return saudacao


pyautogui.alert(title="AR(Autonomous Rochedo)",
                text="Vou começar a trabalhar, por favor não utilize o computador até minha finalização! Aproveite esse tempo para tomar um café.",
                button="Okay guy!")

pyautogui.hotkey('win', 'd')
pyautogui.press('winleft')
pyautogui.write('Teams')
time.sleep(1)
pyautogui.press('enter')
time.sleep(9)
for x in base.index:
    eid = base['EID'][x]
    apelido = base['Nome'][x].split()[0]
    mensagem = base['Mensagem'][x].replace('<APELIDO>', apelido).replace('<SAUDACAO>', tempoNow())
    if eid == 'EID' or eid is None:
        continue
    pyautogui.hotkey('ctrl', 'e')
    pyautogui.write(eid)
    time.sleep(2)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('alt', 'Shift', 'c')
    time.sleep(1)
    writeMsg(mensagem)
    pyautogui.press('enter')
    time.sleep(3)

pyautogui.alert(title="AR(Autonomous Rochedo)",
                text="Trabalho finalizado! Você já pode utilizar o computador!",
                button="Very good! Tks.")
