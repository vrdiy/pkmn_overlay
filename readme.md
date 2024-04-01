# Pokémon Overlay

This app lets you showcase your party Pokémon with art from the TCG for use in broadcasting software.
![](readme/banner.png)
    
## Controls

### Adding Pokémon
Type the slot number (1-6), followed by a space, and the name of the Pokémon:

`1 beldum`

![](readme/add_pokemon.png)

### Removing Pokémon
Type the slot of the Pokémon you'd like to remove, followed by a space, and then the letter 'x':

`1 x`

![](readme/rmv_pokemon.png)

#### Removing All
You can also remove all Pokémon from the layout by entering 'clear':

`clear`

### Change Card Image
[!WARNING]
This does nothing on the minimal version as you only have one card per Pokémon

Sometimes the card doesn't look the best for a particular Pokémon, to get the next available card, type the slot of the Pokémon, followed by a space, and then the letter 'r':

`1 r`

### Layout Controls
- F1 - **2x3**
- F2 - **3x2**
- F3 - **6x1**
- F4 - **1x6**
- TAB - **Removes gaps in layout**

## Streaming Setup
- Add a window capture of Pokémon Overlay to your sources. Use `#ff0080`/`rgb(255,0,128)` for your chroma key color.

![](readme/chroma_key.png)


## Manual Setup
[!TIP]
If you are just looking for a ready-to-go application, just go to <a href="https://github.com/vrdiy/pkmn_overlay/releases/">releases</a> and you can find bundled distributions of the app. The following section is primarily for those who would prefer to 
You will need Python, and I recommend creating a virtual environment just for this application, for info on setting up a virtual environment see this: https://docs.python.org/3/library/venv.html
 
1. Download the card art here: https://drive.google.com/file/d/12OxKjOa3NmDUt2yFM7HZ28E7sQ7uEecP/view?usp=drive_link
2. Extract and place the `rsc/` folder you just downloaded into the root directory of this project.
3. Create and activate a virtual environment in the root directory of this project
4. `pip install -r requirements.txt`
5. `python pkmn_overlay.py`

# Building Exe Nuitka

To build the exes using Nuitka first install it:

`pip install nuitka`

Minimal (1 of each card):

`python -m nuitka --standalone --include-data-dir=rsc/minimal_cards=rsc/cards --include-data-files=rsc/pokeball_minimal.ico=rsc/pokeball.ico --include-data-files=rsc/pokemon_names.txt=rsc/ --standalone --windows-icon-from-ico=rsc/pokeball_minimal.ico --disable-console --output-dir=pkmn_overlay_minimal --output-filename="Pkmn Overlay - Minimal.exe" pkmn_overlay.py`

Full (Up to 5 of each card):

`python -m nuitka --standalone --include-data-dir=rsc/cards=rsc/cards --include-data-files=rsc/pokeball.ico=rsc/ --include-data-files=rsc/pokemon_names.txt=rsc/ --standalone --windows-icon-from-ico=rsc/pokeball.ico --disable-console --output-dir=pkmn_overlay --output-filename="Pkmn Overlay.exe" pkmn_overlay.py`

# Special Mentions
Card images sourced from https://pkmncards.com/ <3
