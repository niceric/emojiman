# importerar pygame-biblioteket
import pygame
# importerar "constants"
from settings import *
# importerar klasser som används i main.py
from emojienemy import EmojiEnemy
from emojiman import EmojiMan, FlyingEmoji, FlyingClouds
from gamemap import GameMap, BACKGROUND
from scores import Watermelon, Apples, Scores, DrawScore, Life
# startar igång pygamemodulerna
pygame.init()

# laddar in musiken och sätter på reapet med -1
pygame.mixer.music.load("assets/emoji_man_song3.mp3")
pygame.mixer.music.play(loops = -1)
# sätter fönstrets namn samt visningsikon
pygame.display.set_caption("EmojiMan in Rectland")
pygame.display.set_icon(pygame.image.load(EMOJI_SURFACE))

# variabel för huvudloopen
running = True


# skapar en ett clock-objekt för att använda i spelloopen med dess uppdateringsfrekvens
clock = pygame.time.Clock() 
# skapar objektinstanser från inbyggd .sprite.Group där sprites kan förvaras i listor med 
# ytterligare metoder för t.ex collision
sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()
start_sprites = pygame.sprite.Group() 

# sakapar instanser av fienderna med startposition, steg och hastighet
# som key word arguments/kwargs
enemy_1 = EmojiEnemy(start_x= 870, start_y= 120, steps= 90, speed = 5)
enemy_2 = EmojiEnemy(start_x= 1270, start_y= 480, steps= 17, speed = 6)
enemy_3 = EmojiEnemy(start_x= 1000, start_y= 800, steps = 80, speed = 10)
enemy_4 = EmojiEnemy(start_x= 1800, start_y= 300, steps = 40, speed = 5)
enemy_5 = EmojiEnemy(start_x= 1070, start_y= 480, steps = 65, speed = 3)
# lägger till fienderna i fiendespritegruppen
enemies.add(enemy_1, enemy_2, enemy_3, enemy_4, enemy_5)

# skapar instans av spelaren
player_1 = EmojiMan()
# lägger till spelaren i spelarspritegruppen
player.add(player_1)

# skapar instanser av dom flygande emojisarna vid startfönstret samt molnen
#flying_emoji = FlyingEmoji() 
#clouds = FlyingClouds()

# skapar instanser av frukterna
water_melon01 = Watermelon()
apple_01 = Apples()
# använder en lista för att lägga till frukterna
all_fruits = [water_melon01, apple_01]
# använder listan för att lägga till i fruktspritegruppen
#fruits.add(all_fruits)
# skapar instans av scores klassen för att kunna beräkna poängen från frukterna
scores = Scores(fruits)
# sakapar instans för att kunna rendera score samt antal poäng
score = DrawScore()
# skapar instans som hanterar livräknaren
hearts = Life()


# skapar instans av spelets bana
level = GameMap()
# kallar på metoden för att kolla kollision mot spelaren och rendering av alla tiles
level.draw_map([collision_sprites, sprites])

# skapar variabler som är förändras under spelets gång ----------------------------------------------------

started = False
taken_damage = False
current_time = 0
damaged_time = 0
current_score = 0
invincible = False


# kör igång huvudloopen
while running: 
    # kollar igenom alla events/eventloopen
    for event in pygame.event.get():

        # kollar om eventet ovan är av typen KEYDOWN
        if event.type == pygame.KEYDOWN:
            # avslutar spelet
            if event.key == ESC:
                running = False
            # startar spelets gång 
            if event.key == ENTER and started == False:
                    # lägger till alla sprites som ska renderas 
                    sprites.add(player_1, enemy_1, enemy_2, enemy_3, enemy_4, enemy_5, water_melon01, apple_01)
                    # lägger till frukterna för att kunna beräkna collision och därmed poängökning
                    fruits.add(all_fruits)
                    # sätter spelarns startposition
                    player_1.rect.center = (100, 200)
                    # sätter till True för att hoppa över denna loop
                    started = True
        # om event är SPAWN_CLOUD så skapas molnen som flyger 
        elif event.type == SPAWN_CLOUD:
                flying_cloud = FlyingClouds()
                start_sprites.add(flying_cloud)
        # om spelet är vid startfönstret    
        if started == False:
            # skapar dom fallande emojisarna
            if event.type == SPAWN_EMOJI:
                flying_emoji = FlyingEmoji()
                start_sprites.add(flying_emoji)      
    # går in i spelloopen
    if running:
        # skickar bakgrundsbilden till skärminstansen
        SCREEN.blit(BACKGROUND, (0, 0))
        # skapar en variabel för alla tangenter som trycks ner
        key = pygame.key.get_pressed()
        # skickar in alla tangenttryckningar för att kunna förflytta spelaren
        # med .update metoden
        player.update(key)
        # får fiendera att förflytta sig
        enemies.update()
        # kallar på metoden för att poängräkning
        scores.get_scores(player_1)
        # kallar på .collision metoden som tar spelaren och tilesspriten som kwargs(för att förtydliga)
        player_1.collision(player = player_1, collision_sprites = collision_sprites)

        # går igenom sprites i enemiesgruppen
        for enemy in enemies:
            # kollar om spelarens .rect har kollision med en fiende .rect
            if pygame.Rect.colliderect(player_1.rect, enemy.rect):
                # om ovan True 
                taken_damage = True 
        # om spelaren har kollision med en fiende .rect
        if taken_damage:
            # ändra på spelarens visningssprite
            player_1.surface = EMOJI_DAMAGED
            # beräkngar en offset för pratbubblan
            offset_x = 10 + player_1.rect.topright[0]
            offset_y = player_1.rect.topright[1]
            offset = (offset_x, offset_y)
            # renderar pratbubblan med offset ovan
            SCREEN.blit(OUCH, offset)
            # kollisionen är gjorde och går in i is_damaged fasen
            is_damaged = True
            if is_damaged == True:
                # tar tid för att använda för fasen som spelaren ska vara odödlig 
                # och ha en annan surface
                current_time = pygame.time.get_ticks()

                damaged_time = current_time + 400
                # ser till att inte loopen fortsätter
                taken_damage = False
                # går in och tar bort ett hjärta samt sätter som odödlig
                if invincible == False and len(hearts.current_hearts) != 0:
                    invincible = True
                    hearts.current_hearts.remove(1)
        # tar tiden varje spelloop för att använda mot damaged_time
        new_time = pygame.time.get_ticks()

        # om tiden för att vara skadad har gått 
        if new_time >= damaged_time:
            # spelaren får tillbaka sin ursprungs surface
            player_1.surface = pygame.image.load(EMOJI_SURFACE).convert()
            # nollställer så looparna ovan kan gå igenom igen
            is_damaged = False
            invincible = False

        # renderar molnen som flyger i bakgrunden
        for sprite in start_sprites:   
            sprite.fly(started)
            SCREEN.blit(sprite.surface, sprite.rect)
        # renderar spritesen som rör på sig samt har kollision
        for sprite in sprites:
            SCREEN.blit(sprite.surface, sprite.rect)
        # uppdaterar poängen så dom renderas samt hjärtan
        score.display_score(scores.current_score)
        hearts.draw_hearts()
    
    # går in här när spelet sätts på först som en startskärm med instruktioner
    if started == False:
        score.draw_text() 
        # renderar molnen/fallande emojis
        for sprite in start_sprites:   
            sprite.fly(started)
            SCREEN.blit(sprite.surface, sprite.rect)
        # förhindrar en bugg då spelaren kunde röra på sig och ta skada innan spelet startat
        invincible = True   
    # avslutar spelets gång och ger ett fönster med lose eller win
    if scores.current_score == 2 or len(hearts.current_hearts) == 0 or player_1.rect.bottom > 2000:        
        score.game_over(scores.current_score)
        print(scores.current_score)
        # renderar molnen
        for sprite in start_sprites:   
            sprite.fly(started)
            SCREEN.blit(sprite.surface, sprite.rect)
        # startar om spelet vid enter-tangent och nollställer poäng/frukter/hjärtan/spelar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                scores.current_score = score.score_reset()
                hearts.reset_hearts()
                sprites.add(player_1, enemy_1, enemy_2, enemy_3, enemy_4, enemy_5, water_melon01, apple_01)
                fruits.add(all_fruits)
                player_1.rect.center = (100, 200)
    
    # uppdaterar skärmen med alla renderingar
    pygame.display.flip()
    # .tick metoden med antal bilder per sekund som spelloopen körs med
    clock.tick(FPS)
                
# stänger ner alla pygame moduler som initierats
pygame.quit()



