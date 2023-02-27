import pygame
from time import sleep
from random import shuffle


class Game:

    def __init__(self):

        self.title = pygame.display.set_caption("War")
        self.size = (400, 2*144)
        self.surface = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.running = True
        self.giving_cards = False
        self.removing_cards = False

        self.cards = []
        self.card_size = (100, 144)
        self.cards_sprite = pygame.image.load("CuteCards.png")
        
        self.black_pile = []
        self.black_deck_pos = (0, 0)
        self.black_pile_pos = (self.size[0]//2-self.card_size[0]//2,
                               self.size[1]//2-self.card_size[1])

        self.red_pile = []
        self.red_deck_pos = (self.size[0]-self.card_size[0],
                             self.size[1]-self.card_size[1])
        self.red_pile_pos = (self.size[0]//2-self.card_size[0]//2,
                             self.size[1]//2)
        
        self.sprites = []  # [pos, end, color]

    class Card:

        def __init__(self, value, image):

            self.value = value
            self.image = image

    def prepare_deck(self):

        # extract value and image for each card
        for row in range(4):
            for col in range(13):

                value = col+1
                image = (col*self.card_size[0], row*self.card_size[1],
                         self.card_size[0], self.card_size[1])

                self.cards.append(self.Card(value, image))

        shuffle(self.cards)

        self.black_deck = self.cards[:len(self.cards)//2]
        self.red_deck = self.cards[len(self.cards)//2:]

    def animate_card(self):

        if self.giving_cards and self.sprites == []:
            self.giving_cards = False
        elif self.removing_cards and self.sprites == []:
            self.removing_cards = False

        speed = 4

        for sprite in self.sprites:

            x, y = sprite[0]
            x1, y1 = sprite[1]

            # if arrive delete
            if x1-speed <= x <= x1+speed and y1-speed <= y <= y1+speed:
                self.sprites.remove(sprite)
            # right
            if sprite[0][0] < sprite[1][0]:
                sprite[0] = (sprite[0][0]+speed, sprite[0][1])
            # down
            if sprite[0][1] < sprite[1][1]:
                sprite[0] = (sprite[0][0], sprite[0][1]+speed)
            # left
            if sprite[0][0] > sprite[1][0]:
                sprite[0] = (sprite[0][0]-speed, sprite[0][1])
            # up
            if sprite[0][1] > sprite[1][1]:
                sprite[0] = (sprite[0][0], sprite[0][1]-speed)

            color = [2, 3][sprite[2] == "red"]

            self.surface.blit(self.cards_sprite, sprite[0],
                              (14*self.card_size[0], color*self.card_size[1],
                               self.card_size[0], self.card_size[1]))

    def draw_decks(self):

        for pos, color in [[self.black_deck_pos, 2], [self.red_deck_pos, 3]]:

            self.surface.blit(self.cards_sprite, pos,
                              (14*self.card_size[0], color*self.card_size[1],
                               self.card_size[0], self.card_size[1]))

    def draw_piles(self):

        for pile, pos, color in [[self.black_pile, self.black_pile_pos, 2],
                                 [self.red_pile, self.red_pile_pos, 3]]:

            if self.giving_cards:
                pile = pile[:-1]

            for x, card in enumerate(pile):

                image = [card.image, (14*self.card_size[0],
                                      color*self.card_size[1],
                                      self.card_size[0],
                                      self.card_size[1])][x % 2]

                self.surface.blit(self.cards_sprite,
                                  ((pos[0]+20*x)-10*x, pos[1]),
                                  image)


# initialise
game = Game()
game.prepare_deck()

# main loop
while game.running:

    game.surface.fill("lightpink")

    if game.giving_cards or game.removing_cards:

        game.animate_card()
        game.draw_piles()

    else:

        # check if the piles are empty or with even numbers of cards
        if (len(game.black_pile) % 2 == 0 and len(game.red_pile) % 2 == 0) or game.black_pile[-1].value == game.red_pile[-1].value:

            game.sprites.append([game.black_deck_pos, game.black_pile_pos,
                                 "black"])

            game.sprites.append([game.red_deck_pos, game.red_pile_pos,
                                 "red"])

            game.black_pile.append(game.black_deck.pop(0))
            game.red_pile.append(game.red_deck.pop(0))
            game.giving_cards = True

        # if the piles have an odd number of cards
        elif len(game.black_pile) % 2 == 1 and len(game.red_pile) % 2 == 1:

            if game.black_pile[-1].value < game.red_pile[-1].value:

                for card in game.black_pile:
                    game.red_deck.append(card)
                for card in game.red_pile:
                    game.red_deck.append(card)
                game.black_pile, game.red_pile = [], []

                game.sprites.append([game.black_pile_pos,
                                     game.red_deck_pos,
                                     "black"])

                game.sprites.append([game.red_pile_pos,
                                     game.red_deck_pos,
                                     "red"])

                game.removing_cards = True

            elif game.black_pile[-1].value > game.red_pile[-1].value:

                for card in game.black_pile:
                    game.black_deck.append(card)
                for card in game.red_pile:
                    game.black_deck.append(card)
                game.black_pile, game.red_pile = [], []

                game.sprites.append([game.red_pile_pos,
                                     game.black_deck_pos,
                                     "red"])

                game.sprites.append([game.black_pile_pos,
                                     game.black_deck_pos,
                                     "black"])

                game.removing_cards = True

    game.draw_decks()
    pygame.display.update()

    # pause the programm to show the cards
    # i need to find a better way to do it
    if not game.giving_cards and not game.removing_cards and not (len(game.black_pile) == 0 and len(game.red_pile) == 0):
        sleep(0.5)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            pygame.quit()

    game.clock.tick(60)
