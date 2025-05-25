


''' CREDITS, PERMISSION AND REFERENCES:


THIS PROJECT WAS INSPIRED FROM THE "THE BIG BOOK OF SMALL PYTHON PROJECT" BY AL SWEIGART
    .... PROJECT 4, BLACKJACK

    Sweigart, A. (2021). The big book of small Python projects: 81 easy practice programs. No Starch Press.
    https://inventwithpython.com/bigbookpython/project4.html




https://inventwithpython.com/bigbookpython/appendixb.html -- For the Unicode

Pygame Community. (2024). Pygame v2.6.0 documentation. https://www.pygame.org/docs/ -- PyGame Documentation


freeCodeCamp.org. (2019, October 23). Pygame tutorial for beginners - Python game development course [Video]. YouTube.
 https://www.youtube.com/watch?v=FfWpgLFMI7w -- Helped me familiarise with pygame


python basic. (2018, May 24). python basic random shuffle [Video]. YouTube. 
https://www.youtube.com/watch?v=Jiv9zVeIRBY


Python Basics. (2019, February 9). Python Basics Pygame Mouse Get Pos Method [Video]. YouTube. 
https://www.youtube.com/watch?v=3Zl1vE-D5h0


Code Coach. (2021, June 29). Create Blackjack in Python | Beginner Friendly Tutorial [Video]. YouTube.
https://www.youtube.com/watch?v=mpL0Y01v6tY&t=318s


Totaka, K. (2006). Shop Channel Title [Audio file]. Internet Archive. 
https://archive.org/details/wii-shop-channel-soundtrack/Kazumi+Totaka+-+Shop+Channel+Title.mp3
SONG USED - 
LICENSE: CREATIVE COMMON ATTRIBUTION AUSTRALIA

CREATIVE CODING (IDEA9103) taught by Somanwita Sarkar at The University of Sydney helped me complete this project as I was able to apply the logic
taught in that course here.

'''



import pygame 
import random


pygame.init() #initalises pygame

pygame.mixer.init() #initialises music
pygame.mixer.music.load('Wii Shop Channel - Menu Banner Theme.mp3')
pygame.mixer.music.play(-1) #-1 

'''GLOBALS'''
width = 1000
height = 600
card_w = 90
card_h = 135
white = (255, 255, 255)
casino_green = (0, 110, 0)
black = (0, 0, 0)
card_colour = (237, 225, 192)
red = (220, 5, 5)
diamond = chr(9830) #(Sweigart, 2021.)
heart = chr(9829) #(Sweigart, 2021.)
club = chr(9827) #(Sweigart, 2021.)
spade = chr(9824) #(Sweigart, 2021.)
chars = (diamond, heart, club, spade) #they don't matter in a game of blackjack and are here to display 
numbers = ('2','3','4','5','6','7','8','9','10','J','Q','K','A') #decided to go with a tuple for better error prevention inspired from (COAD COACH, 2021.)
in_play = True
message = ""
round_count = 0
max_rounds = 5
armin_wins = 0
karlos_wins = 0
round_results = []
font_fam = pygame.font.SysFont('times new roman', 24)
bold_font = pygame.font.SysFont('times new roman bold', 40)
button_font = pygame.font.SysFont('roboto', 34)
yellow = (237, 227, 31)
different_red = (240, 68, 53)
orange = (201, 63, 8)

'''setting the canvas'''
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Armin vs Karlos')







class Button:
    def __init__(self, x, y, w, h, text, font,color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
    def draw(self):
        pygame.draw.rect(screen,self.color, self.rect) #.draw.rect will inherit the colour 
        pygame.draw.rect(screen,black, self.rect, 2)
        text = self.font.render(self.text, True, black) #This creates a new Surface with the specified text rendered on it. Pygame Community. (2024)
        screen.blit(text, text.get_rect(center=self.rect.center))#blit draws the surface, this is the only method to draw something on canvas
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) #checks if pos is in the rect to or not, basically detecting the mouse click
    
hit = Button(370, 520, 120, 50, 'Hit', button_font,yellow)
stand = Button(530, 520, 120, 50, 'Stand', button_font,different_red)
    

def total_of_a_card(card_var): #diffrenitating the value of the cards
    if card_var == 'J' or card_var == 'Q' or card_var == 'K':
        new_card_var = 10
    elif card_var == 'A':
        new_card_var = 11
    else:
        new_card_var = int(card_var)
    return int(new_card_var) #will simply return the number from 2 to 10

def game_logic_basic(player_cards):#Derived logic from Al Sweigart's def gethandvalue(cards) Blackjack project (Sweigart, 2021, line 169)
    ace = 0
    points = 0   
    for j in player_cards:
        x = j[0]                
        card_value = total_of_a_card(x)#checks what the card shows J,K,2,4,5, ETC.
        points += card_value           
        if x == 'A':
            ace += 1
#if total is above 21 then Ace is counted as 1 and not 11
    while points > 21 and ace > 0:
        points -= 10
        ace -= 1
    return points

def draw_card(numbers, chars, x, y):

    #the following argument takes (canvas, color, xpos, ypos, w, h)

    pygame.draw.rect(screen, card_colour, (x, y, card_w, card_h))
    pygame.draw.rect(screen, black, (x, y, card_w, card_h), 3) #3 here is for the thickness of boundary

    text = font_fam.render(f"{numbers}{chars}", True, black) #printing the numbers inside card
    text_in_rect = text.get_rect(center=(x + card_w // 2, y + card_h // 2)) #aligning the text in the card
    screen.blit(text, text_in_rect)

def game_setup():
    screen.fill(casino_green)

    karlos_xpos = width - (len(karlos_hand) * (card_w + 10)) - 50 #
    j = 0
    for card in karlos_hand:
        x = karlos_xpos + j * (card_w + 10)#deriving x pos and 10 is the gap
        draw_card(card[0], card[1], x, 100)#
        j += 1

    i = 0
    for card in armin_hand:
        x = 50 + i * (card_w + 10)
        draw_card(card[0], card[1], x, 400) 
        i += 1

    armin_text = font_fam.render('Armin: ' + str(game_logic_basic(armin_hand)), True, white) #true is to make the font smooth
    #false would have made the text pixelated kind of like minecraft blocks haha
    screen.blit(armin_text, (50, 370))
    if in_play:
        karlos_text = 'Classified'
    else:
        karlos_text = str(game_logic_basic(karlos_hand))
    karlos_text = font_fam.render('Karlos: ' + karlos_text, True, black)#same logic as above
    screen.blit(karlos_text, (width - 250, 70))#these numbers are here the coordinates of xpos and ypos

    '''Round counting'''
    round_text = font_fam.render('Round ' + str(round_count + 1) + " of " + str(max_rounds), True, white) 
    screen.blit(round_text, (width // 2 - 80, 20))



    if message != "":
        message_text = bold_font.render(message, True, white)
        screen.blit(message_text, message_text.get_rect(center=(width // 2, height // 2)))






    if in_play:
        hit.draw()
        stand.draw()
        instruction_text = font_fam.render('Hit: Draw card     Stand: Play cards', True, white)
        screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, 570))

    elif not in_play and len(round_results) > 0:
        last_result = round_results[-1]#round result was a global list I declared above
        result_text = font_fam.render(last_result, True, white)
        screen.blit(result_text, (width // 2 - result_text.get_width() // 2, height // 2 + 50))

    pygame.display.update()



deck = []
for j in numbers:#loop will go through the tuple numbers and put them in a deck     
    for i in chars:#this gets the useless special character  
        deck.append((j, i))#this will create normal cards with speical symbols



random.shuffle(deck)#random.shuffle will remove the duplicates (python basic, 2018)
#giving them both their cards from the deck 
armin_hand = [deck.pop(), deck.pop()]
karlos_hand = [deck.pop(), deck.pop()]




run = True
while run:
    game_setup()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False









        elif in_play and event.type == pygame.MOUSEBUTTONDOWN: #(Python Bascs,2019.)

            if hit.is_clicked(event.pos):
                armin_hand.append(deck.pop())

                if game_logic_basic(armin_hand) > 21:
                    message = 'Armin drew > 21.'
                    karlos_wins += 1
                    round_results.append(f'Round {round_count + 1}: Karlos won!')
                    in_play = False








            elif stand.is_clicked(event.pos):
                while game_logic_basic(karlos_hand) < 17:
                    karlos_hand.append(deck.pop())

                armin_game = game_logic_basic(armin_hand)
                karlos_game = game_logic_basic(karlos_hand)


                if karlos_game > 21 or armin_game > karlos_game:
                    message = 'Armin wins!'
                    armin_wins += 1
                    round_results.append(f'Round {round_count + 1}: Armin won!')
                elif karlos_game > armin_game:
                    message = 'Karlos wins.'
                    karlos_wins += 1
                    round_results.append(f'Round {round_count + 1}: Karlos won!')
                else:
                    message = 'Tie game.'
                    round_results.append(f'Round {round_count + 1}: boooo!!! (tied)')
                in_play = False








    
    if not in_play:
        game_setup()  
        pygame.time.delay(2000)#will delay the next gameplay 
        round_count += 1
        if round_count >= max_rounds:
            final_message = 'CHAMPION --> '
            if armin_wins > karlos_wins:
                final_message += 'Armin wins SEM 2 2025'
                screen.fill(casino_green)
            elif karlos_wins > armin_wins:
                final_message += 'Karlos wins SEM 2 2025'
                screen.fill(red)
            else:
                final_message += 'No one wins :('
                screen.fill(orange) #orange

            screen.blit(bold_font.render(final_message, True, white), (width // 2 - 250, 30))
            y_pos = 100
            for result in round_results:
                line = font_fam.render(result, True, white)
                screen.blit(line, (width // 2 - 150, y_pos))
                y_pos += 30
            pygame.display.update()

            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        run = False






        else:
            deck = []
            for j in numbers:   
                for i in chars:
                    deck.append((j, i))
            random.shuffle(deck)
            armin_hand = [deck.pop(), deck.pop()]
            karlos_hand = [deck.pop(), deck.pop()]
            message = ""
            in_play = True

pygame.quit()

