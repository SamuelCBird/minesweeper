# Minesweeper

This is a recreation of the classic game found on most Windows machines. I embarked upon this project whilst learning Python as a challenge and a way to improve my knowledge and skill. 

The official Minesweeper went through many versions and I've tried to recreate the version I remember playing. I'm not sure exactly which version that was, but I would have been playing on a Windows 95 or 98 machine. 

## Build Status

This game runs and works as expected. 

## Known Bugs or Inconsistencies

- The smiley button is there, and the face changes in response to various actions as it should, but the click to start a new game function is not implemented yet. So to start a new game you have to quit and rerun the script. I'm intending to add this in due course.

- On some of the official Minesweepers I know that right clicking on the numbers automatically cleared some of the squares with no mine underneath; I didn't include this feature.

- Currently this recreation only has one game size available; 40x40 which was the intermediate level. In the future I may add the easy and hard level too, and possibly the custom level.

- If you have lost the game (clicked on a mine), the unclicked mines still open.

## Language

This was built in **Python 3** with the **Pygame** library.

## Dependencies

**Pygame1.9.2**

## Screenshots

![screenshot](/images/screenshot.png)
