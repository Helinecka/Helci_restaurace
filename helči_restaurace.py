import pygame
import random

pygame.init()

# vytvoření herního okna
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Helči restaurace")  # název okna

# vytvoření proměnných pro barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
GREY = (200, 200, 200)

# obrázky jídel místo puvodnich koleček
FOOD_IMAGES = [
    pygame.transform.scale(pygame.image.load("coca_cola.png"), (30, 55)),
    pygame.transform.scale(pygame.image.load("meat.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("cake.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("melon.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("sushi.png"), (50, 40))]

# pozadí
background_image = pygame.image.load("floor.png")
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# font
font = pygame.font.SysFont(None, 36)

# kytky
#flowers = [
    #pygame.Rect(0, window_height - 130, 50, 150),  # leva kytka
    #pygame.Rect(window_width - 50, window_height - 130, 50, 150)]  # prava kytka

# instrukce ke hře
information_background = pygame.image.load("information_background.png")
information_background = pygame.transform.scale(information_background, (700, 700))

def show_instructions():
    showing = True
    while showing:
        screen.blit(background_image, (0, 0))
        screen.blit(information_background, (50, -80))

        title = font.render("HELČI RESTAURACE", True, BLACK)
        instruction1 = font.render("Pohyb: šipkami", True, BLACK)
        instruction2 = font.render("Interakce: mezerníkem", True, BLACK)
        instruction3_1 = font.render("Obsluž zákazníky dřív, než", True, BLACK)
        instruction3_2 = font.render("se naštvou!", True, BLACK)
        instruction4_1 = font.render("Zahoď jídlo u koše, pokud", True, BLACK)
        instruction4_2 = font.render("neseš nesprávné.", True, BLACK)
        start_text_1 = font.render("Stiskni ENTER pro", True, RED)
        start_text_2 = font.render("spuštění hry.", True, RED)

        screen.blit(title, (window_width//2 - title.get_width()//2, 130))
        screen.blit(instruction1, (window_width//2 - instruction1.get_width()//2, 170))
        screen.blit(instruction2, (window_width//2 - instruction2.get_width()//2, 210))
        screen.blit(instruction3_1, (window_width//2 - instruction3_1.get_width()//2, 250))
        screen.blit(instruction3_2, (window_width//2 - instruction3_2.get_width()//2, 275))
        screen.blit(instruction4_1, (window_width//2 - instruction4_1.get_width()//2, 315))
        screen.blit(instruction4_2, (window_width//2 - instruction4_2.get_width()//2, 340))
        screen.blit(start_text_1, (window_width//2 - start_text_1.get_width()//2, 380))
        screen.blit(start_text_2, (window_width//2 - start_text_2.get_width()//2, 405))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showing = False

# TŘÍDY
# třída číšníka = hráče
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # obrazky pro animaci
        self.images_right = [
            pygame.transform.scale(pygame.image.load("player_standing_right.png"), (50, 150)), # stoji a kouka do prava
            pygame.transform.scale(pygame.image.load("player_walking_right1.png"), (50, 150)), # jde do prava 1
            pygame.transform.scale(pygame.image.load("player_walking_right2.png"), (50, 150))] # jde do prava 2
        self.images_left = [
            pygame.transform.scale(pygame.image.load("player_standing_left.png"), (50, 150)), # stoji a kouka do leva
            pygame.transform.scale(pygame.image.load("player_walking_left1.png"), (50, 150)),# jde do leva 1
            pygame.transform.scale(pygame.image.load("player_walking_left2.png"), (50, 150))] # jde do leva 2

        self.image = self.images_right[0]  # výchozí obrázek - stojící doprava
        self.rect = self.image.get_rect(center = (280, 150)) # výchozí pozice hráče
        self.speed = 5
        self.carrying_food = None

        self.direction = "right" # aktuální směr pohybu
        self.walking = False # jestli hráč právě chodí
        self.animation_index = 0 # index pro animaci nohou
        self.animation_timer = 0 # časovač animace

    def update(self, keys):
        self.walking = False
        new_rect = self.rect.copy()

        if keys[pygame.K_LEFT]:
            new_rect.x = max(0, new_rect.x - self.speed)
            self.direction = "left"
            self.walking = True

        elif keys[pygame.K_RIGHT]:
            new_rect.x = min(window_width - new_rect.width, new_rect.x + self.speed)
            self.direction = "right"
            self.walking = True

        if keys[pygame.K_UP]:
            new_rect.y = max(0, new_rect.y - self.speed)
            self.walking = True

        if keys[pygame.K_DOWN]:
            new_rect.y = min(window_height - new_rect.height, new_rect.y + self.speed)
            self.walking = True

        self.rect = new_rect  # pohyb bez kontroly kolizí ------ PO VYRESENI KOLIZI SMAZAT

        # kolize s překážkami           ------- NEFUNGUJE
        #feet_rect = self.get_feet_rect()
        #if not any(obstacle.colliderect(feet_rect) for obstacle in obstacle_rects):
            #self.rect = new_rect
            
        # animace nohou
        if self.walking:
            self.animation_timer += clock.get_time()
            if self.animation_timer > 150:
                self.animation_timer = 0
                self.animation_index = 1 if self.animation_index == 2 else 2
        else:
            self.animation_index = 0

        if self.direction == "right":
            self.image = self.images_right[self.animation_index]

        else:
            self.image = self.images_left[self.animation_index]

    def get_feet_rect(self):
        # obdélník představující nohy hráče
        return pygame.Rect(
            self.rect.left + 20,
            self.rect.bottom - 10,
            self.rect.width - 40, 10)

# třída pultu s jídly
class Counter:
    def __init__(self):
        self.positions = [(180 + i * 100, 50) for i in range(5)]  # pevná místa pro jídla na pultu
        self.food_available = [True] * 5  # dostupnost jídla (lze vzít např. prostřední jídlo)
        self.last_spawn = [pygame.time.get_ticks()] * 5  # čas posledního obnovení jídla

    def update(self, current_time):
        for i in range(5):
            if not self.food_available[i] and current_time - self.last_spawn[i] > 5000:
                self.food_available[i] = True
                self.last_spawn[i] = current_time

    def draw(self, surface):
        # Načteme obrázek pultu
        self.image = pygame.image.load("counter.png")
        self.image = pygame.transform.scale(self.image, (600, 100))
        self.rect = self.image.get_rect(center = (400, 105))
        surface.blit(self.image, self.rect)
        # Vykreslíme jídla na pultu
        for i, pos in enumerate(self.positions):
            if self.food_available[i]:
                # zajistí, že máme správný obrázek pro dané jídlo
                img = FOOD_IMAGES[i]
                rect = img.get_rect(center = pos)  # nastaví pozici pro každé jídlo
                surface.blit(img, rect)  # vykreslí jídlo na pult

# třída stolu
class Table(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("table.png")
        self.image = pygame.transform.scale(self.image, (240, 180))
        self.rect = self.image.get_rect(center = pos)
        self.customer_waiting = True
        self.served_time = 0
        self.requested_food = random.randint(0, 4)

        self.customer = Customer()
        self.customer.rect.midbottom = self.rect.midtop

    def reset_customer(self):
        self.customer_waiting = True
        self.requested_food = random.randint(0, 4)
        self.customer = Customer()
        self.customer.rect.midbottom = (self.rect.centerx, self.rect.top + 180)

# třída koše
class TrashBin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("trash_bin.png")
        self.image = pygame.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect(center = pos)

# třída zákazníka
class Customer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load("customer1.png"), (70, 120)),
            pygame.transform.scale(pygame.image.load("customer2.png"), (70, 120)),
            pygame.transform.scale(pygame.image.load("customer3.png"), (70, 120)),
            pygame.transform.scale(pygame.image.load("customer_angry.png"), (70, 120))]
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.stage = 0
        self.spawn_time = pygame.time.get_ticks()
        self.angry = False

    def update(self, current_time, table_rect):
        elapsed = current_time - self.spawn_time
        if elapsed > 32000:
            self.stage = 3
            self.angry = True
        elif elapsed > 24000:
            self.stage = 3
        elif elapsed > 16000:
            self.stage = 2
        elif elapsed > 8000:
            self.stage = 1
        else:
            self.stage = 0

        self.image = self.images[self.stage]
        self.rect.midbottom = (table_rect.centerx, table_rect.top + 180)

player = Player()
counter = Counter()

# vytvoření více stolů
tables = pygame.sprite.Group()
table_positions = [
    (150, 440),
    (150, 280),
    (400, 440),
    (400, 280),
    (650, 440),
    (650, 280)]

for pos in table_positions:
    table = Table(pos)
    tables.add(table)

# vytvoření košů
trash_bins = pygame.sprite.Group()
trash_bins.add(TrashBin((50, 100)), TrashBin((750, 100)))

# vytvoření bublin
bubble_img = pygame.image.load("dream_bubble.png")

# skupina všech objektů
all_sprites = pygame.sprite.Group()
all_sprites.add(trash_bins)
all_sprites.add(tables)
all_sprites.add(player)

# proměnné
score = 0
clock = pygame.time.Clock()
running = True

#      PŘEKÁŽKY             ------- NEFUNGUJE
#obstacle_rects = []
#      přidání stolů
#for table in tables:
    #obstacle_rects.append(table.rect)
#      přidání pultu
#counter_rect = pygame.Rect(100, 55, 600, 100)  # vyhrazeni pultu
#obstacle_rects.append(counter_rect)
#      přidání košů
#for bin in trash_bins:
    #obstacle_rects.append(bin.rect)
#      přidání květin
#for flower in flowers:
    #obstacle_rects.append(flower)

# zavolani funkce instrukci
show_instructions()

# proměnné pro klávesy
space_pressed = False
space_was_pressed_last_frame = False

# HERNÍ SMYČKA
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Jednorázový stisk mezerníku
    if keys[pygame.K_SPACE] and not space_was_pressed_last_frame:
        space_pressed = True
    else:
        space_pressed = False

    # Ulož stav pro další snímek
    space_was_pressed_last_frame = keys[pygame.K_SPACE]

    # pohyb hráče
    player.update(keys)
    counter.update(current_time)

    # PODMÍNKY
    # POKUD je hráč u jídla na pultu a nic nenese TAK vezme jídlo
    if player.carrying_food is None and space_pressed:
        space_pressed = False
        for i, pos in enumerate(counter.positions):
            rect = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
            if rect.colliderect(player.rect) and counter.food_available[i]:
                player.carrying_food = i
                counter.food_available[i] = False
                counter.last_spawn[i] = current_time
                break

    # POKUD je hráč u nějakého stolu, nese jídlo, zákazník čeká a stiskne SPACE TAK ho obslouží
    for table in tables:
        if table.customer_waiting:
            table.customer.update(current_time, table.rect)

            if table.customer.angry:
                table.customer_waiting = False
                table.served_time = current_time
                score = max(0, score - 1)

            elif player.carrying_food == table.requested_food and player.rect.colliderect(table.rect) and space_pressed:
                score += 1
                player.carrying_food = None
                table.customer_waiting = False
                table.served_time = current_time

    # Po 3 sekundách se zákazník znovu objeví a jídlo se obnoví na pultu
    for table in tables:
        if not table.customer_waiting:
            if current_time - table.served_time > 3000:
                table.reset_customer()

    # POKUD je hráč u koše a stiskne SPACE TAK zahodí jídlo
    if player.carrying_food is not None:
        for bin in trash_bins:
            if player.rect.colliderect(bin.rect) and space_pressed:
                player.carrying_food = None

    # VYKRESLOVÁNÍ
    screen.blit(background_image, (0, 0)) # pozadí
    counter.draw(screen) # pult a jídla

    # zákaznik
    for table in tables:
        if table.customer_waiting:
            screen.blit(table.customer.image, table.customer.rect)

    # vyreseni vrstev obrazku podle osy Y
    sprites_to_draw = []

    for table in tables:
        sprites_to_draw.append(table)
        if table.customer_waiting:
            sprites_to_draw.append(table.customer)

    sprites_to_draw += [player] + list(trash_bins)

    sprites_to_draw.sort(key = lambda sprite: sprite.rect.bottom) # seradi objekty podle spodni hrany

    for sprite in sprites_to_draw:
        screen.blit(sprite.image, sprite.rect)

    # obrázek nad stolem když je objednávka
    for table in tables:
        if table.customer_waiting:
            # vykreslení bubliny
            bubble_img = pygame.transform.scale(bubble_img, (120, 100))
            bubble_rect = bubble_img.get_rect(center = (table.rect.centerx + 50, table.rect.top + 10))
            screen.blit(bubble_img, bubble_rect)

            # vykreslení jídla uvnitř bubliny
            img = FOOD_IMAGES[table.requested_food]
            rect = img.get_rect(center = (table.rect.centerx + 50, table.rect.top))
            screen.blit(img, rect)

    # obrázek nad hráčem když nese jídlo
    if player.carrying_food is not None:
        img = FOOD_IMAGES[player.carrying_food]
        rect = img.get_rect(center = (player.rect.centerx, player.rect.top - 15))
        screen.blit(img, rect)

    # zobrazení skóre
    score_text = font.render(f"Skóre: {score}", True, BLACK)
    screen.blit(score_text, (window_width - 450, 550))

    # aktualizace obrazovky
    pygame.display.update()
    clock.tick(90)  # počet snímků za sekundu

# prostě konec
pygame.quit()

# TO DO LIST: 
# nelze chodit skrz stoly a jiné objekty - uz fakt nevim jak