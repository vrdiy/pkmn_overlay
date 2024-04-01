
import os
import random

from PIL import Image 
import pygame 

ASPECT_RATIO = 474/280
RESOLUTION = (1280,720)
#LEFT = 0.126
#UPPER = 0.133
#RIGHT = 0.916
#LOWER = 0.472
LEFT = 0.10
UPPER = 0.111
RIGHT = 0.9
LOWER = 0.472

STANDARD_SIZE = (734,1024)
IMG_SIZE = (int(RESOLUTION[0]/6),int((RESOLUTION[0]/6)/ASPECT_RATIO))
CROP_RATIOS = (int(STANDARD_SIZE[0]*LEFT),int(STANDARD_SIZE[1]*UPPER),int(STANDARD_SIZE[0]*RIGHT),int(STANDARD_SIZE[1]*LOWER))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RSC_DIR = os.path.abspath(os.path.join(PROJECT_ROOT,"rsc/"))
CARDS_DIR = os.path.abspath(os.path.join(RSC_DIR,"cards/"))
SAVE_FILE = os.path.abspath(os.path.join(PROJECT_ROOT,"party.txt"))


def pilImageToSurface(pilImage : Image.Image):
    return pygame.image.frombytes(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

def get_card_image_by_pokemon(pokemon_name : str, card_index = None):
    pokemon_name = pokemon_name.lower()
    pkmn : pygame.Surface = pygame.Surface(IMG_SIZE)
    if card_index is None:
        card_index = random.randrange(6)
    if card_index is not None:
        try:
            img = Image.open(os.path.abspath(os.path.join(CARDS_DIR,f"{pokemon_name}_{card_index}.png")))
            img = img.resize(STANDARD_SIZE)
            cropped = img.crop(CROP_RATIOS)
            img = cropped.resize(IMG_SIZE)
            pkmn = pilImageToSurface(img)
            return pkmn, card_index, pokemon_name
        except FileNotFoundError:
            print("No Images Found")
    index = 0
    for i in range(5):
        try:
            img = Image.open(os.path.abspath(os.path.join(CARDS_DIR,f"{pokemon_name}_{i}.png")))
        except FileNotFoundError:
            print("No Images Found")
            return None
        img = img.resize(STANDARD_SIZE)
        cropped = img.crop(CROP_RATIOS)
        img = cropped.resize(IMG_SIZE)
        pkmn = pilImageToSurface(img)
        index = i
        break
    return pkmn, index, pokemon_name

def get_pokemon_slot_and_name(text : str)-> str:
    choices = text.split(' ',1)
    if len(choices) != 2:
        print("Not enough parameters")
        return None
    try:
        slot = int(choices[0])
    except:
        slot = -1
    pkmn_name = choices[1]
    if slot not in range(1,7):
        print("Something is not right.")
        return None
    return (slot,pkmn_name)

def get_random_team()->list[pygame.surface.Surface,int,str]:
    team = [None]*6
    with open(os.path.abspath(os.path.join(RSC_DIR,'pokemon_names.txt')),'r') as file:
        pokemon_names = file.readlines()
        
        for i in range(6):
            temp = get_card_image_by_pokemon(pokemon_names[random.randrange(len(pokemon_names))][:-1])
            while temp is None:
                temp = get_card_image_by_pokemon(pokemon_names[random.randrange(len(pokemon_names))][:-1]) 
            team[i] = temp
    return team

def clear_empty_slots_on_team(team : list[pygame.surface.Surface,int,str])->list[pygame.surface.Surface,int,str]:
    compact_team = [None] * 6
    counter = 0
    for pkmn in team:
        if pkmn is not None:
            compact_team[counter] = pkmn
            counter+=1
    return compact_team

def load_save() -> list[pygame.surface.Surface,int,str]:
    team = [None] * 6
    if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE,'r+') as sav:
                for i in range(6):
                    try:
                        pkmn_name, card_index = sav.readline().split(',',1)
                        pkmn = get_card_image_by_pokemon(pkmn_name,card_index[:-1])
                        if pkmn == None:
                            pass
                        else:
                            team[i] = pkmn
                    except Exception as e:
                        pass
                team = clear_empty_slots_on_team(team) 
                return team
    else:
        return [None] * 6 
    
def save_team(team : list[pygame.surface.Surface,int,str]):
    with open(SAVE_FILE,'w+') as sav:
        for pkmn in team:
            if pkmn is not None:
                sav.write(f"{pkmn[2]},{pkmn[1]}\n")
        sav.close()

def main():
    pygame.init()
    pygame.display.init()
    icon = pygame.image.load(os.path.abspath(os.path.join(RSC_DIR,'pokeball.ico')))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Pokémon Overlay')
    screen = pygame.display.set_mode((RESOLUTION[0], IMG_SIZE[1]))
    fuchsia = (255, 0, 128)  # Transparency color
    clock = pygame.time.Clock()
    font = pygame.font.Font(size=24)

    pkmns = load_save()
    temp_text = ""
    backspace_counter = 0
    layout = 6,1
    done = False
    update = True
    while not done:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                save_team(pkmns)
            if event.type == pygame.MOUSEBUTTONDOWN:
                update = True
            if event.type == pygame.KEYDOWN:
                update = True
                if event.key == pygame.K_BACKSPACE:
                    if backspace_counter > 2:
                        temp_text = ""
                        backspace_counter = 0
                    else:
                        temp_text = temp_text[:-1]
                        backspace_counter +=1
                elif event.key == pygame.K_RETURN:
                    if temp_text.lower() == "clear":
                        pkmns = [None] * 6
                    else:
                        selection = get_pokemon_slot_and_name(temp_text)
                        if selection is not None:
                            if selection[1].lower() == 'x':
                                pkmns[selection[0]-1] = None
                            elif selection[1].lower() == 'r':
                                if pkmns[selection[0]-1] is not None:
                                    pkmns[selection[0]-1] = get_card_image_by_pokemon(pkmns[selection[0]-1][2],int(pkmns[selection[0]-1][1])+1)
                            else:
                                pkmns[selection[0]-1] = get_card_image_by_pokemon(selection[1])
                    temp_text = ""
                elif event.key == pygame.K_F1: # 2x3
                    screen = pygame.display.set_mode(((IMG_SIZE[0]*2),IMG_SIZE[1]*3))
                    update = True
                    layout = 2,3
                elif event.key == pygame.K_F2: # 3x2
                    screen = pygame.display.set_mode(((IMG_SIZE[0]*3),IMG_SIZE[1]*2))
                    update = True
                    layout = 3,2
                elif event.key == pygame.K_F3: # 6x1
                    screen = pygame.display.set_mode(((IMG_SIZE[0]*6),IMG_SIZE[1]*1))
                    update = True
                    layout = 6,1
                elif event.key == pygame.K_F4: # 1x6
                    screen = pygame.display.set_mode(((IMG_SIZE[0]*1),IMG_SIZE[1]*6))
                    update = True
                    layout = 1,6
                elif event.key == pygame.K_TAB:
                    pkmns = clear_empty_slots_on_team(pkmns)
                elif event.key == pygame.K_ESCAPE:
                    done = True
                    save_team(pkmns)
                else:
                    backspace_counter = 0
                    temp_text += str(event.unicode)
        if update: # Draw screen only when needed
            screen.fill(fuchsia)  # Transparent background
            counter = 0
            for i in range(layout[0]):
                for j in range(layout[1]):
                    if pkmns[counter] is not None:
                        screen.blit(pkmns[counter][0],(pkmns[counter][0].get_width()*i,pkmns[counter][0].get_height()*j))
                    counter += 1

            text_surf = font.render(temp_text, True, (0,0,0))
            text_rect = text_surf.get_rect()
            text_rect.x = 10
            text_rect.y = 10
            pygame.draw.rect(screen,(255,255,255),text_rect)
            screen.blit(text_surf,(10,10))
            pygame.display.update()
        update = False

if __name__ == "__main__":
    main()