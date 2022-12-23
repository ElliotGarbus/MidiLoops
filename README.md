# MidiLoops
A simple midi controlled audio player designed for playing backing tracks, each track plays as an endless loop

Release builds for Windows10 and Mac on Release Page: 

**Directions:**

Drag the backing track file you would like to play onto one of the loop sections.  The number of the left of 
each of the loops sections corresponds to the MIDI PC# to select that track.  The file name will be displayed 
in the center toggle button.

Select the midi device (or midi device interface) for controlling the player, and the matching midi channel.

Pressing the SongTitle will cause the current loop to stop (if one is playing) and the selected loop to begin.  Pressing 
the select loop a second time will cause play to stop. Pressing the trashcan icon button will remove the 
loop from MidiLoops.

Each loop has an independently adjustable volume level.  


The MidiLoops can be controlled by the buttons on the app or a MIDI controller.

**Configure your MIDI Controller to send PC/CC messages**

**PC Messages**
When a PC message associated with one of the loops is received the selected loop begins to play.  If a different loop is playing when the 
PC message is received it will stop. The BackingTrackPlayer responds to the following MIDI messages:

**CC Messages**

Action | CC# | CC Value | Notes
-------|-----|---------|------------|
Stop | 1 | any | Stop playing
Next | 2 | any | stop the playing, start the next loop
Volume|3| 0-127 | set the volume for the playing loop

The audio loops by default.
Use PC to start a loop.


