# http://tomashg.com
# ghz.tomash@gmail.com
# Color clips script for MIDI Fighter 3D from DJ TECH TOOLS
from Constants import *

TRACK_OFFSET = 0 #offset from the left of linked session origin
SCENE_OFFSET = 0 #offset from the top of linked session origin (no auto-join)

# Session Navigation (aka "red box")
# Possible buttons: LEFTSIDE_BTN1,LEFTSIDE_BTN2, LEFTSIDE_BTN3, 
# RIGHTSIDE_BTN1, RIGHTSIDE_BTN2, RIGHTSIDE_BTN3,
# BANK_BTN1, BANK_BTN2, BANK_BTN3, BANK_BTN4

SESSIONLEFT = LEFTSIDE_BTN1 #Session left
SESSIONRIGHT = RIGHTSIDE_BTN1 #Session right
SESSIONUP = BANK_BTN3 #Session up
SESSIONDOWN = BANK_BTN4 #Session down
ZOOMUP = -1 #Session Zoom up
ZOOMDOWN = -1 #Session Zoom down
ZOOMLEFT = -1 #Session Zoom left
ZOOMRIGHT = -1 #Session Zoom right


# Button Color Values
# All the possible colors: RED, LOWRED, WHITE, CYAN, LOWCYAN, PURPLE, LOWPURPLE
# BLUE, LOWBLUE, YELLOW, LOWYELLOW, GREEN, LOWGREEN, PINK, LOWPINK, CHARTREUSSE
# LOWCHARTREUSSE, ORANGE, LOWORANGE, REDCYCLE, GREENCYCLE, BLUECYCLE, RGBCYCLE
PLAYTRIG_COL = BLUECYCLE # Clip Triggered to play
TRIGD_COL = GREENCYCLE # Clip Playing
RECTRIG_COL = REDCYCLE # Clip Trigered to record
RECD_COL = RED # Clip recording

# Buttons / Pads
# -------------
# Valid Note/CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments are permitted

BUTTONCHANNEL = 2 # Channel assignment for all mapped buttons/pads; valid range is 0 to 15
MESSAGETYPE = 0 # Message type for buttons/pads; set to 0 for MIDI Notes, 1 for CCs. 
PAGE = 0 # On which Page of the MF3D to map the clip launch buttons


# 4x4 Matrix note assignments
# DONT CHANGE THIS, if you want to assign the clip launcher to another page edit the PAGE variable
# Track no.:     1               2           3           4
CLIPNOTEMAP = ((48+16*PAGE, 49+16*PAGE, 50+16*PAGE, 51+16*PAGE), #Row 1
               (44+16*PAGE, 45+16*PAGE, 46+16*PAGE, 47+16*PAGE), #Row 2
               (40+16*PAGE, 41+16*PAGE, 42+16*PAGE, 43+16*PAGE), #Row 3
               (36+16*PAGE, 37+16*PAGE, 38+16*PAGE, 39+16*PAGE), #Row 4
               )
