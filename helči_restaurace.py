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
RED = (255, 100, 100)
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
flowers = [
    pygame.Rect(0, window_height - 130, 50, 150),  # leva kytka
    pygame.Rect(window_width - 50, window_height - 130, 50, 150)]  # prava kytka

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
        self.rect = self.image.get_rect(center = (280, 160))
        self.speed = 3
        self.carrying_food = None

        self.direction = "right" # aktuální směr pohybu
        self.walking = False # jestli hráč právě chodí
        self.animation_index = 0 # index pro animaci nohou
        self.animation_timer = 0 # časovač animace (pro přepínání snímků)

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

        # kolize s kytkama
        if not any(zone.colliderect(new_rect) for zone in flowers):
            self.rect = new_rect  # pohyb jen pokud není kolize

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

    def reset_customer(self):
        self.customer_waiting = True
        self.requested_food = random.randint(0, 4)

# třída koše
class TrashBin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("trash_bin.png")
        self.image = pygame.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect(center = pos)

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

# HERNÍ SMYČKA
while running:
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    # zavření okna
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pohyb
    player.update(keys)
    counter.update(current_time)

    # PODMÍNKY
    # POKUD je hráč u jídla na pultu a nic nenese TAK vezme jídlo
    if player.carrying_food is None and keys[pygame.K_SPACE]:
        for i, pos in enumerate(counter.positions):
            rect = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
            if rect.colliderect(player.rect) and counter.food_available[i]:
                player.carrying_food = i
                counter.food_available[i] = False
                counter.last_spawn[i] = current_time
                break

    # POKUD je hráč u nějakého stolu, nese jídlo, zákazník čeká a stiskne SPACE TAK ho obslouží
    for table in tables:
        if player.rect.colliderect(table.rect) and player.carrying_food is not None and table.customer_waiting:
            if player.carrying_food == table.requested_food:
                # Kontrola, zda hráč stiskl klávesu ENTER
                if keys[pygame.K_SPACE]:  # pokud je stisknutý Enter
                    score += 1
                    table.customer_waiting = False
                    table.served_time = current_time
                    player.carrying_food = None  # obslouženo, když nese správné jídlo

    # Po 3 sekundách se zákazník znovu objeví a jídlo se obnoví na pultu
    for table in tables:
        if not table.customer_waiting:
            if current_time - table.served_time > 3000:
                table.reset_customer()

    # POKUD je hráč u koše a stiskne SPACE TAK zahodí jídlo
    if player.carrying_food is not None:
        for bin in trash_bins:
            if player.rect.colliderect(bin.rect) and keys[pygame.K_SPACE]:
                player.carrying_food = None

    # VYKRESLOVÁNÍ
    screen.blit(background_image, (0, 0)) # pozadí
    counter.draw(screen) # pult a jídla
    all_sprites.draw(screen) # všechny objekty

    # obrázek nad stolem když je objednávka
    for table in tables:
        if table.customer_waiting:
            # Vykreslení bubliny
            bubble_img = pygame.transform.scale(bubble_img, (120, 100))
            bubble_rect = bubble_img.get_rect(center = (table.rect.centerx + 50, table.rect.top + 10))
            screen.blit(bubble_img, bubble_rect)

            # Vykreslení jídla uvnitř bubliny
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
# dodělat zákazníky
# zbarvování zákazníka do červena podle délky čekání - rudý zákazník odchází a snižuje skore
# nelze chodit skrz stoly a jiné objekty