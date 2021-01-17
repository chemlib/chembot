# Chembot

Chembot is a chemistry discord bot built on the Python package [chemlib](https://github.com/chemlib/chemlib) that provides easy access to element data and quickly performs calculations.

## Commands

**Command Prefix: ``-``**

### help

Displays help message.

Usage: ``-help``

[help](https://user-images.githubusercontent.com/58019082/104853716-7f201300-58b7-11eb-9e6e-c697b32e18e0.jpg)

### elem 

Displays properties of requested element by symbol.

Usage: ``-elem <symbol>``

[elements](https://user-images.githubusercontent.com/58019082/104853737-ad9dee00-58b7-11eb-86a0-b734113fcf2f.jpg)

### cmpd

Gets the molar mass of a compound, and performs optional calculations.

Usage: ``-cmpd <formula>``

Additional Parameters (accepts abbreviations): 
- ``--amount <number and units>``
- ``--composition <elem symbol>``

[cmpd](https://user-images.githubusercontent.com/58019082/104853774-e5a53100-58b7-11eb-881a-bd04ad914020.jpg)