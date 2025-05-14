import pygame
import sys
import random
import math
import os
from enum import Enum

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация звукового движка

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Binding of Bin Laden")
clock = pygame.time.Clock()

# Пути к ресурсам
IMG_DIR = "images"
SOUND_DIR = "sounds"

# Создаем папки для ресурсов, если их нет
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(SOUND_DIR, exist_ok=True)

# Класс для игровых состояний
class GameState(Enum):
    TITLE = 1
    CHARACTER_SELECT = 2
    GAME = 3
    GAME_OVER = 4
    VICTORY = 5

# Класс для хранения ассетов
class Assets:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        self.backgrounds = {}
        self.load_assets()
    
    def load_assets(self):
        # Загрузка шрифтов
        self.fonts["title"] = pygame.font.SysFont("Arial", 48)
        self.fonts["medium"] = pygame.font.SysFont("Arial", 36)
        self.fonts["small"] = pygame.font.SysFont("Arial", 24)
        
        # Загружаем изображения персонажей
        self.images["player_1"] = self.create_image("player_1.png", (60, 60), RED)  # Osama Bin Laden
        self.images["player_2"] = self.create_image("player_2.png", (60, 60), GREEN)  # Saddam Hussein
        self.images["player_3"] = self.create_image("player_3.png", (60, 60), BLUE)  # Aiman AL-Zawahiri
        
        # Загружаем изображения врагов
        self.images["enemy_1"] = self.create_image("enemy_1.png", (60, 60), YELLOW)  # Враг-преследователь
        self.images["enemy_2"] = self.create_image("enemy_2.png", (60, 60), BROWN)   # Враг-стрелок
        self.images["enemy_3"] = self.create_image("enemy_3.png", (60, 60), GRAY)    # Враг-охранник
        
        # Загружаем изображение босса
        self.images["boss"] = self.create_image("boss.png", (100, 100), RED)
        
        # Загружаем изображения снарядов
        self.images["bullet_player"] = self.create_image("bullet_player.png", (30, 30), WHITE)
        self.images["bullet_enemy"] = self.create_image("bullet_enemy.png", (40, 40), RED)
        
        # Загружаем фоны уровней
        self.backgrounds[1] = self.create_image("background_3.png", (SCREEN_WIDTH, SCREEN_HEIGHT), DARK_GRAY)
        self.backgrounds[2] = self.create_image("background_2.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (70, 70, 100))
        self.backgrounds[3] = self.create_image("background_1.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (100, 70, 70))
        self.backgrounds[4] = self.create_image("background_4.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (70, 100, 70))
        self.backgrounds[5] = self.create_image("background_5.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (100, 100, 50))
        
        # Загружаем изображение сердца
        self.images["heart"] = self.create_image("heart.png", (80, 50), RED)
        
        # Загружаем музыку
        self.music["menu"] = self.create_sound("menu_music.mp3", is_music=True)
        self.music["game"] = self.create_sound("game_music.mp3", is_music=True)
        self.music["boss"] = self.create_sound("boss_music.mp3", is_music=True)
        
        # Загружаем звуковые эффекты
        self.sounds["hit"] = self.create_sound("hit.wav")
        self.sounds["enemy_death"] = self.create_sound("enemy_death.wav")
        self.sounds["player_hurt"] = self.create_sound("player_hurt.wav")
        self.sounds["victory"] = self.create_sound("victory.wav")
        
    def create_image(self, name, size, default_color):
        """Создает изображение, если файл существует, или заглушку с указанным цветом"""
        try:
            # Пытаемся загрузить изображение
            fullname = os.path.join(IMG_DIR, name)
            if os.path.exists(fullname):
                image = pygame.image.load(fullname)
                image = pygame.transform.scale(image, size)
                return image
            else:
                # Если файл не существует, создаем заглушку
                surf = pygame.Surface(size, pygame.SRCALPHA)
                surf.fill(default_color)
                # Добавим рамку для заглушки
                pygame.draw.rect(surf, WHITE, surf.get_rect(), 1)
                return surf
        except Exception as e:
            print(f"Ошибка при загрузке изображения {name}: {e}")
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(default_color)
            return surf
    
    def create_sound(self, name, is_music=False):
        """Создает объект звука или музыки, возвращает None, если файл не существует"""
        try:
            fullname = os.path.join(SOUND_DIR, name)
            if os.path.exists(fullname):
                if is_music:
                    return fullname  # Для музыки возвращаем путь
                else:
                    return pygame.mixer.Sound(fullname)
            return None
        except Exception as e:
            print(f"Ошибка при загрузке звука {name}: {e}")
            return None
    
    def get_image(self, name):
        """Возвращает изображение по имени или заглушку, если не найдено"""
        return self.images.get(name, pygame.Surface((30, 30)))
    
    def get_background(self, level):
        """Возвращает фон для указанного уровня"""
        return self.backgrounds.get(level, self.backgrounds.get(1))
    
    def play_sound(self, name):
        """Воспроизводит звуковой эффект"""
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
    
    def play_music(self, name):
        """Воспроизводит музыку"""
        if name in self.music and self.music[name]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music[name])
            pygame.mixer.music.play(-1)  # Зацикливаем музыку
    
    def stop_music(self):
        """Останавливает музыку"""
        pygame.mixer.music.stop()

# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type):
        super().__init__()
        self.player_type = player_type
        self.image_name = f"player_{player_type}"
        self.image = assets.get_image(self.image_name)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.health = 6
        self.max_health = 6
        self.damage = 1
        self.fire_rate = 10
        self.fire_delay = 0
        self.bullets = pygame.sprite.Group()
        self.invincible = False
        self.invincible_timer = 0
        
        # Статистика в зависимости от типа персонажа
        if player_type == 1:  # Осама бин Ладен - средний персонаж
            pass  # Стандартные настройки
        elif player_type == 2:  # Саддам Хусейн - быстрый персонаж с меньшим здоровьем
            self.speed = 7
            self.health = 4
            self.max_health = 4
            self.fire_rate = 8
        elif player_type == 3:  # Аиман аль-Завахири - сильный медленный персонаж
            self.speed = 3
            self.health = 8
            self.max_health = 8
            self.damage = 2
            self.fire_rate = 15
    
    def update(self):
        # Обработка движения
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # Ограничение движения по экрану
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
        # Обработка выстрелов
        if self.fire_delay > 0:
            self.fire_delay -= 1
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and self.fire_delay == 0:
            self.shoot(keys)
            self.fire_delay = self.fire_rate
        
        # Обновление пуль
        self.bullets.update()
        
        # Обработка неуязвимости после получения урона
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
    
    def shoot(self, keys):
        direction = [0, 0]
        if keys[pygame.K_UP]:
            direction[1] = -1
        elif keys[pygame.K_DOWN]:
            direction[1] = 1
        if keys[pygame.K_LEFT]:
            direction[0] = -1
        elif keys[pygame.K_RIGHT]:
            direction[0] = 1
        
        if direction != [0, 0]:
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, True, self.damage)
            self.bullets.add(bullet)
            assets.play_sound("shoot")
    
    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            self.invincible = True
            self.invincible_timer = 60  # Неуязвимость на 1 секунду
            assets.play_sound("player_hurt")
            return True
        return False
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
    
    def draw_health(self, surface):
        heart_width = 20
        heart_spacing = 5
        heart_img = assets.get_image("heart")
        
        for i in range(self.max_health // 2):
            heart_x = 10 + i * (heart_width + heart_spacing)
            heart_y = 10
            
            # Полное сердце (2 хп)
            if self.health >= (i + 1) * 2:
                surface.blit(heart_img, (heart_x, heart_y))
            # Половина сердца (1 хп)
            elif self.health >= i * 2 + 1:
                half_heart = pygame.Surface((heart_width // 2, heart_width))
                half_heart.blit(heart_img, (0, 0))
                surface.blit(half_heart, (heart_x, heart_y))
            # Пустое сердце (0 хп)
            else:
                empty_heart = pygame.Surface((heart_width, heart_width), pygame.SRCALPHA)
                empty_heart.blit(heart_img, (0, 0))
                empty_heart.fill((100, 100, 100, 150), None, pygame.BLEND_RGBA_MULT)
                surface.blit(empty_heart, (heart_x, heart_y))

# Класс для пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_player_bullet, damage=1):
        super().__init__()
        self.is_player_bullet = is_player_bullet
        self.image = assets.get_image("bullet_player" if is_player_bullet else "bullet_enemy")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 if is_player_bullet else 5
        
        # Нормализация вектора направления
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        if length > 0:
            self.direction = [direction[0]/length, direction[1]/length]
        else:
            self.direction = [0, 0]
        
        self.damage = damage
    
    def update(self):
        # Движение пули
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Удаление пуль, вышедших за пределы экрана
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

# Базовый класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, x, y):
        super().__init__()
        self.enemy_type = enemy_type
        self.image_name = f"enemy_{enemy_type}"
        self.image = assets.get_image(self.image_name)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullets = pygame.sprite.Group()
        self.fire_delay = 0
        
        # Характеристики врага в зависимости от типа
        if enemy_type == 1:  # Враг-преследователь
            self.health = 3
            self.speed = 2
            self.damage = 1
            self.fire_rate = 0  # Не стреляет
        elif enemy_type == 2:  # Враг-стрелок
            self.health = 2
            self.speed = 1
            self.damage = 1
            self.fire_rate = 60  # Стреляет раз в секунду
        elif enemy_type == 3:  # Враг-охранник (перемещается по заданному маршруту)
            self.health = 4
            self.speed = 1.5
            self.damage = 1
            self.fire_rate = 90  # Стреляет раз в 1.5 секунды
            self.patrol_points = []
            self.current_point = 0
            self.set_patrol_points()
    
    def set_patrol_points(self):
        # Создаем случайные точки патрулирования для врага типа 3
        center_x, center_y = self.rect.center
        radius = random.randint(50, 150)
        
        # Добавляем несколько точек вокруг центра
        for i in range(4):
            angle = i * math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.patrol_points.append((x, y))
    
    def update(self, player):
        # Обновление пуль
        self.bullets.update()
        
        # Логика движения и стрельбы в зависимости от типа врага
        if self.enemy_type == 1:  # Враг-преследователь
            # Движение к игроку
            self.move_towards_player(player)
        elif self.enemy_type == 2:  # Враг-стрелок
            # Сохранение дистанции от игрока и стрельба
            dist_to_player = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + 
                                       (player.rect.centery - self.rect.centery)**2)
            
            if dist_to_player < 200:
                # Отходим от игрока
                self.move_away_from_player(player)
            elif dist_to_player > 300:
                # Приближаемся к игроку
                self.move_towards_player(player)
            
            # Стрельба
            if self.fire_delay > 0:
                self.fire_delay -= 1
            else:
                self.shoot_at_player(player)
                self.fire_delay = self.fire_rate
                
        elif self.enemy_type == 3:  # Враг-охранник
            # Движение по маршруту
            if self.patrol_points:
                target = self.patrol_points[self.current_point]
                
                # Движение к текущей точке
                dx = target[0] - self.rect.centerx
                dy = target[1] - self.rect.centery
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist > 5:  # Если не достигли точки
                    self.rect.x += (dx / dist) * self.speed
                    self.rect.y += (dy / dist) * self.speed
                else:
                    # Переход к следующей точке
                    self.current_point = (self.current_point + 1) % len(self.patrol_points)
            
            # Стрельба
            if self.fire_delay > 0:
                self.fire_delay -= 1
            else:
                self.shoot_at_player(player)
                self.fire_delay = self.fire_rate
    
    def move_towards_player(self, player):
        # Вычисление направления к игроку
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            # Нормализация и движение
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
    
    def move_away_from_player(self, player):
        # Вычисление направления от игрока
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            # Нормализация и движение
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
    
    def shoot_at_player(self, player):
        # Вычисление направления к игроку
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        # Создание пули
        bullet = Bullet(self.rect.centerx, self.rect.centery, [dx, dy], False, self.damage)
        self.bullets.add(bullet)
        assets.play_sound("shoot")
    
    def take_damage(self, damage):
        self.health -= damage
        assets.play_sound("hit")
        if self.health <= 0:
            assets.play_sound("enemy_death")
            return True
        return False

# Класс для босса
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = assets.get_image("boss")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 30
        self.max_health = 30
        self.speed = 1.5
        self.damage = 2
        self.bullets = pygame.sprite.Group()
        self.fire_delay = 0
        self.fire_rate = 30  # Стреляет каждые 0.5 секунды
        self.phase = 1  # Фаза босса
        self.attack_pattern = 0  # Текущий паттерн атаки
        self.attack_timer = 0  # Таймер для смены паттернов
    
    def update(self, player):
        # Обновление пуль
        self.bullets.update()
        
        # Смена фазы в зависимости от здоровья
        if self.health <= self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.speed += 0.5
        
        # Обновление таймера атаки
        self.attack_timer += 1
        if self.attack_timer >= 180:  # Смена паттерна каждые 3 секунды
            self.attack_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 3
        
        # Движение и атака в зависимости от паттерна
        if self.attack_pattern == 0:
            # Паттерн 1: Преследование игрока
            self.move_towards_player(player)
        elif self.attack_pattern == 1:
            # Паттерн 2: Случайное движение
            if self.attack_timer % 60 == 0:
                self.random_move()
        elif self.attack_pattern == 2:
            # Паттерн 3: Оставаться на месте и интенсивно стрелять
            pass
        
        # Стрельба
        if self.fire_delay > 0:
            self.fire_delay -= 1
        else:
            self.shoot(player)
            self.fire_delay = self.fire_rate if self.attack_pattern != 2 else self.fire_rate // 2
    
    def move_towards_player(self, player):
        # Вычисление направления к игроку
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            # Нормализация и движение
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
    
    def random_move(self):
        # Случайное движение в пределах экрана
        self.rect.x += random.randint(-20, 20)
        self.rect.y += random.randint(-20, 20)
        
        # Ограничение в пределах экрана
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
    
    def shoot(self, player):
        if self.attack_pattern == 0 or self.attack_pattern == 1:
            # Одиночный выстрел в игрока
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            bullet = Bullet(self.rect.centerx, self.rect.centery, [dx, dy], False, self.damage)
            self.bullets.add(bullet)
            assets.play_sound("shoot")
        elif self.attack_pattern == 2:
            # Круговой выстрел
            for angle in range(0, 360, 45):
                dx = math.cos(math.radians(angle))
                dy = math.sin(math.radians(angle))
                bullet = Bullet(self.rect.centerx, self.rect.centery, [dx, dy], False, self.damage)
                self.bullets.add(bullet)
            assets.play_sound("shoot")
    
    def take_damage(self, damage):
        self.health -= damage
        assets.play_sound("hit")
        return self.health <= 0
    
    def draw_health_bar(self, surface):
        # Рисуем полоску здоровья босса
        health_ratio = self.health / self.max_health
        bar_width = 200
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT - bar_height - 10
        
        # Фон полоски
        pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Полоска здоровья
        pygame.draw.rect(surface, RED, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
        # Контур
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

# Класс для игры
class Game:
    def __init__(self):
        self.state = GameState.TITLE
        self.reset_game()
    
    def reset_game(self):
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.boss = None
        self.room_count = 0
        self.max_rooms = 5  # Количество комнат до появления босса
        self.selected_character = 1
        
        # Установка начальной музыки
        assets.play_music("menu")
    
    def spawn_enemies(self):
        # Очистка существующих врагов
        self.enemies.empty()
        
        # Увеличение счетчика комнат
        self.room_count += 1
        
        # Если достигли максимального количества комнат, создаем босса
        if self.room_count >= self.max_rooms:
            self.boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            assets.play_music("boss")  # Включаем музыку для боя с боссом
            return
        
        # Иначе создаем обычных врагов
        enemy_count = random.randint(3, 5)
        for _ in range(enemy_count):
            enemy_type = random.randint(1, 3)
            
            # Случайное расположение врага
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Проверка, чтобы враг не появился слишком близко к игроку
            if self.player:
                while (abs(x - self.player.rect.centerx) < 150 and 
                       abs(y - self.player.rect.centery) < 150):
                    x = random.randint(50, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
            
            enemy = Enemy(enemy_type, x, y)
            self.enemies.add(enemy)
    
    def start_game(self):
        self.state = GameState.GAME
        self.player = Player(self.selected_character)
        self.room_count = 0
        self.spawn_enemies()
        assets.play_music("game")  # Включаем музыку для игры
    
    def update(self):
        if self.state == GameState.GAME:
            # Обновление игрока
            self.player.update()
            
            # Обновление врагов или босса
            if self.boss:
                self.boss.update(self.player)
                
                # Проверка коллизий пуль игрока с боссом
                hits = pygame.sprite.spritecollide(self.boss, self.player.bullets, True)
                for hit in hits:
                    if self.boss.take_damage(hit.damage):
                        self.state = GameState.VICTORY
                        assets.play_sound("victory")
                        assets.play_music("menu")
                
                # Проверка коллизий пуль босса с игроком
                hits = pygame.sprite.spritecollide(self.player, self.boss.bullets, True)
                for hit in hits:
                    if self.player.take_damage(hit.damage):
                        if self.player.health <= 0:
                            self.state = GameState.GAME_OVER
                            assets.stop_music()
                
                # Проверка коллизий игрока с боссом (получение урона при касании)
                if pygame.sprite.collide_rect(self.player, self.boss):
                    if self.player.take_damage(1):
                        if self.player.health <= 0:
                            self.state = GameState.GAME_OVER
                            assets.stop_music()
            else:
                # Обновление обычных врагов
                for enemy in self.enemies:
                    enemy.update(self.player)
                    
                    # Проверка коллизий пуль игрока с врагами
                    hits = pygame.sprite.spritecollide(enemy, self.player.bullets, True)
                    for hit in hits:
                        if enemy.take_damage(hit.damage):
                            enemy.kill()
                    
                    # Проверка коллизий пуль врагов с игроком
                    hits = pygame.sprite.spritecollide(self.player, enemy.bullets, True)
                    for hit in hits:
                        if self.player.take_damage(hit.damage):
                            if self.player.health <= 0:
                                self.state = GameState.GAME_OVER
                                assets.stop_music()
                    
                    # Проверка коллизий игрока с врагами (получение урона при касании)
                    if pygame.sprite.collide_rect(self.player, enemy):
                        if self.player.take_damage(1):
                            if self.player.health <= 0:
                                self.state = GameState.GAME_OVER
                                assets.stop_music()
                
                # Проверка, все ли враги побеждены
                if len(self.enemies) == 0:
                    self.spawn_enemies()
    
    def draw(self):
        # Отрисовка в зависимости от состояния игры
        if self.state == GameState.TITLE:
            # Отрисовка титульного экрана
            screen.fill(BLACK)
            title_text = assets.fonts["title"].render("The Binding of Bin Laden", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(title_text, title_rect)
            
            # Отрисовка инструкции
            start_text = assets.fonts["medium"].render("Press ENTER to start", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(start_text, start_rect)
            
            # Отрисовка кредитов
            credits_text = assets.fonts["small"].render("Created by: Agatu_LLL", True, GRAY)
            credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(credits_text, credits_rect)
            
        elif self.state == GameState.CHARACTER_SELECT:
            # Отрисовка экрана выбора персонажа
            screen.fill(BLACK)
            title_text = assets.fonts["medium"].render("Select Your Muslim", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_text, title_rect)
            
            # Отрисовка персонажей
            char_spacing = 200
            char_y = SCREEN_HEIGHT // 2
            
            for i in range(1, 4):
                char_x = SCREEN_WIDTH // 2 + (i - 2) * char_spacing
                char_img = assets.get_image(f"player_{i}")
                char_rect = char_img.get_rect(center=(char_x, char_y))
                screen.blit(char_img, char_rect)
                
                # Выделение выбранного персонажа
                if i == self.selected_character:
                    pygame.draw.rect(screen, YELLOW, char_rect.inflate(20, 20), 3)
                
                # Отрисовка имени персонажа
                if i == 1:
                    name = "Osama Bin Laden"
                elif i == 2:
                    name = "Saddam Hussein"
                else:
                    name = "Aiman AL-Zawahiri"
                
                name_text = assets.fonts["small"].render(name, True, WHITE)
                name_rect = name_text.get_rect(center=(char_x, char_y + 50))
                screen.blit(name_text, name_rect)
            
            # Отрисовка инструкции
            select_text = assets.fonts["small"].render("Use LEFT/RIGHT arrows to select, ENTER to confirm", True, WHITE)
            select_rect = select_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(select_text, select_rect)
            
        elif self.state == GameState.GAME:
            # Отрисовка игрового экрана
            # Фон уровня
            screen.blit(assets.get_background(self.room_count), (0, 0))
            
            # Отрисовка игрока
            screen.blit(self.player.image, self.player.rect)
            
            # Отрисовка здоровья игрока
            self.player.draw_health(screen)
            
            # Отрисовка пуль игрока
            for bullet in self.player.bullets:
                screen.blit(bullet.image, bullet.rect)
            
            # Отрисовка врагов или босса
            if self.boss:
                screen.blit(self.boss.image, self.boss.rect)
                self.boss.draw_health_bar(screen)
                
                # Отрисовка пуль босса
                for bullet in self.boss.bullets:
                    screen.blit(bullet.image, bullet.rect)
            else:
                for enemy in self.enemies:
                    screen.blit(enemy.image, enemy.rect)
                    
                    # Отрисовка пуль врагов
                    for bullet in enemy.bullets:
                        screen.blit(bullet.image, bullet.rect)
            
            # Отрисовка информации о текущем уровне
            level_text = assets.fonts["small"].render(f"Room: {self.room_count} / {self.max_rooms}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
            
        elif self.state == GameState.GAME_OVER:
            # Отрисовка экрана Game Over
            screen.fill(BLACK)
            
            game_over_text = assets.fonts["title"].render("HAHAHAHHA SUCKER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = assets.fonts["medium"].render(f"Rooms completed: {self.room_count}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
            
            retry_text = assets.fonts["small"].render("Press R to retry or ESC to return to menu", True, WHITE)
            retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(retry_text, retry_rect)
            
        elif self.state == GameState.VICTORY:
            # Отрисовка экрана победы
            screen.fill(BLACK)
            
            victory_text = assets.fonts["title"].render("Perfect", True, GREEN)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(victory_text, victory_rect)
            
            congrats_text = assets.fonts["medium"].render("You have become a true leader of taliban!", True, WHITE)
            congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(congrats_text, congrats_rect)
            
            retry_text = assets.fonts["small"].render("Press R to kick georges ass again or ESC to return to menu", True, WHITE)
            retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(retry_text, retry_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.TITLE:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.CHARACTER_SELECT
                
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == pygame.K_LEFT:
                        self.selected_character = max(1, self.selected_character - 1)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_character = min(3, self.selected_character + 1)
                    elif event.key == pygame.K_RETURN:
                        self.start_game()
                
                elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
                    if event.key == pygame.K_r:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.TITLE
                        self.reset_game()
        
        return True

# Главный игровой цикл
def main():
    assets = Assets()  # Загрузка ассетов
    game = Game()  # Создание игры
    running = True
    
    while running:
        # Обработка событий
        running = game.handle_events()
        
        # Обновление игры
        game.update()
        
        # Отрисовка
        game.draw()
        
        # Обновление экрана
        pygame.display.flip()
        
        # Фреймрейт
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

# Глобальный экземпляр Assets для доступа из всех классов
assets = Assets()

if __name__ == "__main__":
    main()