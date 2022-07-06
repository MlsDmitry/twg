"""
# scene 1
Main menu with play button. When play button is pressed change scene to scene 2.

# scene 2
Generate map, place player, etc.

# scene 3
When "P"(eng) is pressed pause everything rendered on scene 2 and display "pause menu".
Pause menu consist of two buttons: "save & exit", "Resume".

Notes:
Pausing is tricky thing to implement in panda3d. I guess we will need to do everything in "tasks" (like ticks). Suppose a task that handles keyboard pressing and player movement. That task is executed each frame, as sated in panda3d docs, checking for pressed keys and moving player accordingly. When the pause button is pressed this task is removed and so player will stop moving. 
"""
