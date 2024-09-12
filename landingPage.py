import tkinter as tk
from tkinter import filedialog
import os
import shutil
import subprocess
import sys
import pandas as pd


currentDir = os.path.dirname(__file__)
enemyDir = os.path.join(currentDir, "EnemyTables")
playerDir = os.path.join(currentDir, "PlayerTables")
activeDir = os.path.join(currentDir, "ActiveTables")
combatDir = os.path.join(currentDir, "SavedCombatFiles")
programsDir = os.path.join(currentDir, "SubProcesses")
playerBuilder = os.path.join(programsDir, "playerCollect.py")
enemyBuilder = os.path.join(programsDir, "enemyCollect.py")
diceRoller = os.path.join(programsDir, "combineAndDice.py")
combat = os.path.join(programsDir, "combatWindow.py")


playersLoaded = "N"
enemiesLoaded ="N"

def rollDice():
    subprocess.Popen(["python", diceRoller])
    sys.exit()

def buildPlayerTable():
    scriptsDir = os.path.join(os.path.dirname(__file__), "SubProcesses")
    playerBuilder = os.path.join(scriptsDir, "playerCollect.py")
    subprocess.Popen(['python', playerBuilder])
    
def buildEnemyTable():
    scriptsDir = os.path.join(os.path.dirname(__file__), "SubProcesses")
    enemyBuilder = os.path.join(scriptsDir, "enemyCollect.py")
    subprocess.Popen(['python', enemyBuilder])

def openCombat():
    combatTable = filedialog.askopenfilename(
        title="Select an existing combat file",
        initialdir=combatDir,
        filetypes=(("Combat File", ".cbf"),("All Files", "*.*"))
    )
    if combatTable:

        copiedInitList = shutil.copy(combatTable, activeDir)
        renamedFile = os.path.join(activeDir, "initiativeList.pkl")

        if os.path.exists(renamedFile):
            os.remove(renamedFile)

        os.rename(copiedInitList, renamedFile)
        subprocess.Popen([sys.executable, combat, "Y"])
        sys.exit()
    else:
        return
    


def loadEnemyTable():
    global enemiesLoaded
    global enemyFileName
    enemyTable = filedialog.askopenfilename(
        title="Select an existing enemy file",
        initialdir=enemyDir,
        filetypes=(("Enemy Data Table", ".edt"),("All Files", "*.*"))
    )

    if enemyTable:
        copiedFile = shutil.copy(enemyTable, activeDir)
        renamedFile = os.path.join(activeDir, "enemyData.pkl")

        if os.path.exists(renamedFile):
            os.remove(renamedFile)

        os.rename(copiedFile, renamedFile)
        enemiesLoaded = "Y"
        enemyFileName = os.path.basename(enemyTable)
    else:
        enemiesLoaded = "N"

    updateScreen()

def loadPlayerTable():
    global playersLoaded
    global playerFileName
    playerTable = filedialog.askopenfilename(
        title="Select an existing player file",
        initialdir=playerDir,
        filetypes=(("Player Data Table", ".pdt"),("All Files", "*.*"))
    )

    if playerTable:
        copiedFile = shutil.copy(playerTable, activeDir)
        renamedFile = os.path.join(activeDir, "playerData.pkl")

        if os.path.exists(renamedFile):
            os.remove(renamedFile)

        os.rename(copiedFile, renamedFile)
        playersLoaded = "Y"
        playerFileName = os.path.basename(playerTable)
    else:
        playersLoaded = "N"

    updateScreen()


def updateScreen():
    global playersLoaded
    global enemiesLoaded

    if playersLoaded == "Y":
        playerText = tk.Label(landingPage)
        playerText.config(text=f"Player table loaded!", bg="light gray", font="Helvetica 12 bold")
        playerText.place(x=10, y=270, width=180, height=20)

        playerFileText = tk.Label(landingPage)
        playerFileText.config(text=f"{playerFileName}", bg="light gray", font="Helvetica 10")
        playerFileText.place(x=10, y=290, width=180, height=20)
    else:
        playerText = tk.Label(landingPage)
        playerText.config(text="No player table loaded", bg="light gray", font="Helvetica 12 bold")
        playerText.place(x=10, y=270, width=180, height=20)

    if enemiesLoaded == "Y":
        enemyText = tk.Label(landingPage)
        enemyText.config(text=f"Enemy table loaded!", bg="light gray", font="Helvetica 12 bold")
        enemyText.place(x=210, y=270, width=180, height=20)
        
        enemyFileText = tk.Label(landingPage)
        enemyFileText.config(text=f"{enemyFileName}", bg="light gray", font="Helvetica 10")
        enemyFileText.place(x=210, y=290, width=180, height=20)
    else:
        enemyText = tk.Label(landingPage)
        enemyText.config(text="No enemy table loaded", bg="light gray", font="Helvetica 12 bold")
        enemyText.place(x=210, y=270, width=180, height=20)

    if enemiesLoaded == "Y" and playersLoaded == "Y":
        fightButton = tk.Button(landingPage)
        fightButton.config(text="Roll some dice and fight!", wraplength = 360, font="Helvetica 12 bold")
        fightButton.config(command = lambda: rollDice())
        fightButton.place(x=10, y=410, height = 80, width = 380)

landingPage = tk.Tk()
landingPage.title("Initiative Tracker Landing Page")
landingPage.geometry("400x500")
landingPage.config(bg="light gray")    





mainText = tk.Label(landingPage)
mainText.config(text="What would you like to do?", bg="light gray", font="Helvetica 12 bold")
mainText.place(x=10, y=10, width=400, height=30)

createPlayers = tk.Button(landingPage)
createPlayers.config(text="Create a roster of players", wraplength =170, font="Helvetica 10 bold")
createPlayers.config(command= lambda: buildPlayerTable())
createPlayers.place(x=10, y=50, height = 100, width = 180)

loadPlayers = tk.Button(landingPage)
loadPlayers.config(text="Load an existing roster of players", wraplength = 170, font="Helvetica 10 bold")
loadPlayers.config(command= lambda: loadPlayerTable())
loadPlayers.place(x=10, y=160, height = 100, width = 180)

createEnemies = tk.Button(landingPage)
createEnemies.config(text="Create a roster of enemies", wraplength = 170, font="Helvetica 10 bold")
createEnemies.config(command= lambda: buildEnemyTable())
createEnemies.place(x=210, y=50, height = 100, width = 180)

loadEnemies = tk.Button(landingPage)
loadEnemies.config(text="Load an existing roster of enemies", wraplength = 170, font="Helvetica 10 bold")
loadEnemies.config(command= lambda: loadEnemyTable())
loadEnemies.place(x=210, y=160, height = 100, width = 180)


loadButton = tk.Button(landingPage)
loadButton.config(text="Load saved combat", wraplength =370, font="Helvetica 12 bold")
loadButton.config(command= lambda: openCombat())
loadButton.place(x=10, y=320, height = 80, width = 380)


playerText = tk.Label(landingPage)
playerText.config(text="No player table loaded", bg="light gray", font="Helvetica 12 bold")
playerText.place(x=10, y=270, width=180, height=20)

enemyText = tk.Label(landingPage)
enemyText.config(text="No enemy table loaded", bg="light gray", font="Helvetica 12 bold")
enemyText.place(x=210, y=270, width=180, height=20)

landingPage.mainloop()