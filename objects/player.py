from modules.modules import * 
from globalvars.globalvars import *  
from functions.sprite_functions import *  
from functions.window_display_functions import * 

class Player(pygame.sprite.Sprite): 
    """  
    Name: Player
    Location: .../finding-el-dorado/objects/player 
    Purpose: Playable character used by the user
    Return: N/a
    """   
    player_animation_delay = 3
    player_gravity = GRAVITY

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x,y, width, height)
        self.x_vel = 0
        self.y_vel = 0 
        self.mask = None 
        self.direction = "left" 
        self.animation_count = 0   
        self.fall_count = 0 
        self.jump_count = 0  
        self.hit = False 
        self.hit_count = 0  
        
        user_settings = []   
        user_settings = get_user_settings(user_settings)
        self.player_sprite = load_sprite_sheets("MainCharacters", user_settings[3][11:], 32, 32, True)

    def update(self): 
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y)) 
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y): 
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

    def move(self, dx, dy):
        self.rect.x += dx 
        self.rect.y += dy  

    def move_left(self, vel): 
        self.x_vel = -vel 
        if self.direction != "left":
            self.direction = "left" 
            self.animation_count = 0  
            
    def move_right(self, vel): 
        self.x_vel = vel 
        if self.direction != "right":
            self.direction = "right" 
            self.animation_count = 0   

    def jump(self):  
        self.y_vel = -self.player_gravity * 8 
        self.animation_count = 0 
        self.jump_count +=1
        if self.jump_count == 1: 
            self.fall_count = 0  

    def landed(self): 
        self.fall_count = 0 
        self.y_vel = 0 
        self.jump_count = 0 

    def hit_head(self): 
        self.count = 0 
        self.y_vel *= -1

    def make_hit(self): 
        self.hit = True 
        self.hit_count = 0

    def loop(self, fps):  
        self.y_vel += min(1, (self.fall_count / fps) * self.player_gravity) 
        self.move(self.x_vel, self.y_vel)  

        if self.hit: 
            self.hit_count += 1 
        if self.hit_count > fps *2: 
            self.hit = False 
            self.hit_count = 0

        self.fall_count += 1  
        self.update_sprite()
    
    def update_sprite(self): 
        sprite_sheet = "idle"  
        if self.hit:
            sprite_sheet = "hit" 
        elif self.y_vel < 0: 
            if self.jump_count == 1: 
                sprite_sheet = "jump" 
            elif self.jump_count == 2: 
                sprite_sheet = "double_jump" 
        elif self.y_vel > self.player_gravity * 2: 
            sprite_sheet = "fall"        
        elif self.x_vel != 0: 
            sprite_sheet = "run" 

        sprite_sheet_name = sprite_sheet + "_" + self.direction 
        sprites = self.player_sprite[sprite_sheet_name] 
        sprite_index = (self.animation_count // self.player_animation_delay) % len(sprites)
        self.sprite = sprites[sprite_index] 
        self.animation_count += 1  
        self.update()
