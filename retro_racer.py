import pygame
import random
import math
import sys
import time
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (Enhanced Neon/Synthwave palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_CYAN = (0, 255, 255)
NEON_PURPLE = (138, 43, 226)
NEON_GREEN = (57, 255, 20)
NEON_ORANGE = (255, 165, 0)
DARK_PURPLE = (25, 25, 112)
GRID_COLOR = (75, 0, 130)

# Gradient colors
PURPLE_DARK = (25, 25, 112)
PURPLE_LIGHT = (138, 43, 226)
PINK_LIGHT = (255, 20, 147)
CYAN_DARK = (0, 139, 139)
BLUE_DARK = (0, 0, 139)
BLUE_LIGHT = (0, 191, 255)

class SynthSounds:
    """Generate retro synth-style sound effects"""
    
    @staticmethod
    def generate_beep(frequency=440, duration=0.1, volume=0.3):
        """Generate a simple beep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create stereo sound array
        arr = np.zeros((frames, 2), dtype=np.int16)
        
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            wave = int(wave * volume)
            arr[i] = [wave, wave]  # Stereo
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    @staticmethod
    def generate_engine_sound(base_freq=80, duration=0.2, volume=0.2):
        """Generate engine-like sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create stereo sound array
        arr = np.zeros((frames, 2), dtype=np.int16)
        
        for i in range(frames):
            # Mix multiple frequencies for engine sound
            wave1 = math.sin(base_freq * 2 * math.pi * i / sample_rate)
            wave2 = math.sin((base_freq * 1.5) * 2 * math.pi * i / sample_rate)
            wave3 = math.sin((base_freq * 2) * 2 * math.pi * i / sample_rate)
            combined = (wave1 + wave2 * 0.5 + wave3 * 0.3) / 2.8
            wave = int(4096 * combined * volume)
            arr[i] = [wave, wave]  # Stereo
        
        sound = pygame.sndarray.make_sound(arr)
        return sound

class RetroButton:
    """Retro-style chunky pixel button with glow effects"""
    
    def __init__(self, x, y, width, height, text, font, base_color, glow_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.glow_color = glow_color
        self.is_hovered = False
        self.flicker_timer = 0
        self.glow_intensity = 0
    
    def update(self, mouse_pos, dt):
        """Update button state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.flicker_timer += dt
        
        # Glow effect
        if self.is_hovered:
            self.glow_intensity = min(self.glow_intensity + dt * 5, 1.0)
        else:
            self.glow_intensity = max(self.glow_intensity - dt * 3, 0.0)
    
    def draw(self, screen):
        """Draw the retro button with effects"""
        # Flickering effect
        flicker = 1.0 if int(self.flicker_timer * 10) % 20 < 18 else 0.7
        
        # Glow effect (multiple layers)
        if self.glow_intensity > 0:
            glow_alpha = int(self.glow_intensity * 100)
            for i in range(3, 0, -1):
                glow_rect = self.rect.inflate(i * 4, i * 4)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height))
                glow_surf.set_alpha(glow_alpha // (i + 1))
                glow_surf.fill(self.glow_color)
                screen.blit(glow_surf, glow_rect)
        
        # Main button (chunky pixel style)
        button_color = tuple(int(c * flicker) for c in self.base_color)
        pygame.draw.rect(screen, button_color, self.rect)
        
        # Button border (chunky)
        border_color = tuple(min(255, int(c * 1.3)) for c in button_color)
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Inner highlight
        highlight_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, 
                                   self.rect.width - 6, self.rect.height - 6)
        highlight_color = tuple(min(255, int(c * 1.5)) for c in button_color)
        pygame.draw.rect(screen, highlight_color, highlight_rect, 1)
        
        # Text with glow
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text glow
        if self.glow_intensity > 0:
            for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                glow_text = self.font.render(self.text, True, self.glow_color)
                glow_rect = text_rect.copy()
                glow_rect.x += offset[0]
                glow_rect.y += offset[1]
                screen.blit(glow_text, glow_rect)
        
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked
class RetroRacer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RETRO RACER - 80s Style")
        self.clock = pygame.time.Clock()
        
        # Game states
        self.game_state = "START"  # START, PLAYING, GAME_OVER
        self.score = 0
        self.distance = 0
        self.speed = 5
        self.time_elapsed = 0
        self.dt = 0
        
        # Player car
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - 100
        self.player_speed = 8
        
        # Road and simple elements
        self.road_lines = []
        
        # Obstacles
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        
        # Sound effects (with fallback)
        self.sounds = {}
        try:
            self.sounds = {
                'beep': SynthSounds.generate_beep(880, 0.1, 0.3),
                'select': SynthSounds.generate_beep(1200, 0.15, 0.4),
                'crash': SynthSounds.generate_engine_sound(60, 0.5, 0.5),
                'engine': SynthSounds.generate_engine_sound(100, 0.3, 0.2)
            }
            self.sound_enabled = True
        except Exception as e:
            print(f"Warning: Could not initialize sounds: {e}")
            self.sound_enabled = False
            # Create dummy sound objects
            self.sounds = {
                'beep': None,
                'select': None,
                'crash': None,
                'engine': None
            }
        
        # Fonts (pixel-style)
        try:
            self.title_font = pygame.font.Font(None, 72)
            self.ui_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.hud_font = pygame.font.Font(None, 28)
        except:
            self.title_font = pygame.font.SysFont('Times New Roman', 72, bold=True)
            self.ui_font = pygame.font.SysFont('Times New Roman', 36, bold=True)
            self.small_font = pygame.font.SysFont('courier', 24, bold=True)
            self.hud_font = pygame.font.SysFont('courier', 28, bold=True)
        
        # Retro buttons
        self.start_button = RetroButton(SCREEN_WIDTH//2 - 100, 400, 200, 50, 
                                      "START GAME", self.ui_font, NEON_PINK, PINK_LIGHT)
        self.restart_button = RetroButton(SCREEN_WIDTH//2 - 100, 400, 200, 50, 
                                        "PLAY AGAIN", self.ui_font, NEON_CYAN, BLUE_LIGHT)
        self.quit_button = RetroButton(SCREEN_WIDTH//2 - 100, 470, 200, 50, 
                                     "QUIT GAME", self.ui_font, NEON_PURPLE, PURPLE_LIGHT)
        
        # Initialize elements
        self.init_road_lines()
    
    def init_road_lines(self):
        """Initialize road center lines"""
        for i in range(0, SCREEN_HEIGHT + 50, 50):
            self.road_lines.append(i)
    
    def init_stars(self):
        """Initialize background stars"""
        for _ in range(50):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT // 2),
                'brightness': random.uniform(0.3, 1.0),
                'twinkle': random.uniform(0, 2 * math.pi)
            }
            self.stars.append(star)
    
    def play_sound(self, sound_name):
        """Play a sound with error handling"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Silently ignore sound errors
    
    def init_mountains(self):
        """Initialize parallax mountain layers"""
        # Far mountains
        for i in range(0, SCREEN_WIDTH + 100, 80):
            self.far_mountains.append({
                'x': i,
                'height': random.randint(50, 100)
            })
        
        # Near mountains
        for i in range(0, SCREEN_WIDTH + 60, 60):
            self.near_mountains.append({
                'x': i,
                'height': random.randint(80, 150)
            })
    
    def draw_gradient_background(self):
        """Draw gradient background from purple to pink"""
        for y in range(SCREEN_HEIGHT):
            # Calculate gradient ratio
            ratio = y / SCREEN_HEIGHT
            
            # Interpolate between purple and pink
            r = int(PURPLE_DARK[0] + (PINK_LIGHT[0] - PURPLE_DARK[0]) * ratio)
            g = int(PURPLE_DARK[1] + (PINK_LIGHT[1] - PURPLE_DARK[1]) * ratio)
            b = int(PURPLE_DARK[2] + (PINK_LIGHT[2] - PURPLE_DARK[2]) * ratio)
            
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_stars(self):
        """Draw twinkling stars"""
        for star in self.stars:
            star['twinkle'] += 0.1
            brightness = star['brightness'] * (0.5 + 0.5 * math.sin(star['twinkle']))
            color = tuple(int(255 * brightness) for _ in range(3))
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), 1)
    
    def draw_parallax_mountains(self):
        """Draw parallax scrolling mountains"""
        # Far mountains (slower parallax)
        for mountain in self.far_mountains:
            mountain_x = (mountain['x'] - self.horizon_offset * 0.2) % (SCREEN_WIDTH + 100)
            points = [
                (mountain_x - 40, SCREEN_HEIGHT // 3),
                (mountain_x, SCREEN_HEIGHT // 3 - mountain['height']),
                (mountain_x + 40, SCREEN_HEIGHT // 3)
            ]
            pygame.draw.polygon(self.screen, PURPLE_LIGHT, points)
        
        # Near mountains (faster parallax)
        for mountain in self.near_mountains:
            mountain_x = (mountain['x'] - self.horizon_offset * 0.5) % (SCREEN_WIDTH + 60)
            points = [
                (mountain_x - 30, SCREEN_HEIGHT // 2),
                (mountain_x, SCREEN_HEIGHT // 2 - mountain['height']),
                (mountain_x + 30, SCREEN_HEIGHT // 2)
            ]
            pygame.draw.polygon(self.screen, DARK_PURPLE, points)
    
    def draw_animated_grid(self):
        """Draw animated grid overlay"""
        grid_size = 40
        
        # Vertical lines
        for x in range(0, SCREEN_WIDTH, grid_size):
            for y in range(int(self.grid_offset), SCREEN_HEIGHT, grid_size):
                if y < SCREEN_HEIGHT // 2:  # Only in upper portion
                    alpha = int(100 * (1 - y / (SCREEN_HEIGHT // 2)))
                    color = (*GRID_COLOR, alpha)
                    pygame.draw.line(self.screen, GRID_COLOR, (x, y), (x, y + 20), 1)
        
        # Horizontal lines
        for y in range(int(self.grid_offset), SCREEN_HEIGHT // 2, grid_size):
            alpha = int(100 * (1 - y / (SCREEN_HEIGHT // 2)))
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        self.grid_offset += 1
        if self.grid_offset >= grid_size:
            self.grid_offset = 0
    
    def draw_simple_road(self):
        """Draw simple road without complex perspective"""
        road_width = 300
        road_left = SCREEN_WIDTH // 2 - road_width // 2
        road_right = SCREEN_WIDTH // 2 + road_width // 2
        
        # Road surface
        road_rect = pygame.Rect(road_left, 0, road_width, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 40), road_rect)
        
        # Road edges
        pygame.draw.line(self.screen, NEON_CYAN, (road_left, 0), (road_left, SCREEN_HEIGHT), 4)
        pygame.draw.line(self.screen, NEON_CYAN, (road_right, 0), (road_right, SCREEN_HEIGHT), 4)
        
        # Center line stripes
        for i, line_y in enumerate(self.road_lines):
            if 0 <= line_y <= SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, NEON_PINK, 
                               (SCREEN_WIDTH // 2 - 3, line_y, 6, 40))
        
        # Move road lines
        for i in range(len(self.road_lines)):
            self.road_lines[i] += self.speed
            if self.road_lines[i] > SCREEN_HEIGHT:
                self.road_lines[i] = -50
    def draw_simple_obstacles(self):
        """Draw realistic obstacles with proper car shapes and wheels"""
        for obstacle in self.obstacles:
            if obstacle['type'] == 'car':
                # Enemy car with realistic design
                car_width = obstacle['width']
                car_height = obstacle['height']
                
                # Car body (main rectangle)
                car_rect = pygame.Rect(obstacle['x'] - car_width//2, 
                                     obstacle['y'] - car_height//2,
                                     car_width, car_height)
                pygame.draw.rect(self.screen, NEON_PURPLE, car_rect)
                
                # Car roof (smaller rectangle)
                roof_width = car_width - 6
                roof_height = car_height // 3
                roof_rect = pygame.Rect(obstacle['x'] - roof_width//2, 
                                       obstacle['y'] - car_height//2 + 6, 
                                       roof_width, roof_height)
                pygame.draw.rect(self.screen, (100, 30, 150), roof_rect)  # Darker purple
                
                # Windows
                if car_width > 20:  # Only draw details if car is large enough
                    # Front windshield
                    windshield_rect = pygame.Rect(obstacle['x'] - (roof_width-3)//2, 
                                                obstacle['y'] - car_height//2 + 8, 
                                                roof_width - 3, 6)
                    pygame.draw.rect(self.screen, NEON_PINK, windshield_rect)
                    
                    # Rear window
                    rear_window_rect = pygame.Rect(obstacle['x'] - (roof_width-3)//2, 
                                                 obstacle['y'] - car_height//2 + roof_height - 1, 
                                                 roof_width - 3, 4)
                    pygame.draw.rect(self.screen, NEON_PINK, rear_window_rect)
                
                # Car outline
                pygame.draw.rect(self.screen, WHITE, car_rect, 2)
                if car_width > 15:
                    pygame.draw.rect(self.screen, WHITE, roof_rect, 1)
                
                # Headlights (if car is large enough)
                if car_width > 20:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (obstacle['x'] - 6, obstacle['y'] - car_height//2 + 3), 2)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (obstacle['x'] + 6, obstacle['y'] - car_height//2 + 3), 2)
                
                # Wheels (4 wheels positioned correctly)
                wheel_color = (60, 60, 60)  # Dark gray
                wheel_rim_color = (150, 150, 150)  # Light gray
                wheel_size = max(3, car_width // 8)
                rim_size = max(2, wheel_size - 1)
                
                # Front wheels
                front_wheel_y = obstacle['y'] - car_height//2 + 8
                pygame.draw.circle(self.screen, wheel_color, 
                                 (obstacle['x'] - car_width//2 - 1, front_wheel_y), wheel_size)
                pygame.draw.circle(self.screen, wheel_rim_color, 
                                 (obstacle['x'] - car_width//2 - 1, front_wheel_y), rim_size)
                pygame.draw.circle(self.screen, wheel_color, 
                                 (obstacle['x'] + car_width//2 + 1, front_wheel_y), wheel_size)
                pygame.draw.circle(self.screen, wheel_rim_color, 
                                 (obstacle['x'] + car_width//2 + 1, front_wheel_y), rim_size)
                
                # Rear wheels
                rear_wheel_y = obstacle['y'] + car_height//2 - 8
                pygame.draw.circle(self.screen, wheel_color, 
                                 (obstacle['x'] - car_width//2 - 1, rear_wheel_y), wheel_size)
                pygame.draw.circle(self.screen, wheel_rim_color, 
                                 (obstacle['x'] - car_width//2 - 1, rear_wheel_y), rim_size)
                pygame.draw.circle(self.screen, wheel_color, 
                                 (obstacle['x'] + car_width//2 + 1, rear_wheel_y), wheel_size)
                pygame.draw.circle(self.screen, wheel_rim_color, 
                                 (obstacle['x'] + car_width//2 + 1, rear_wheel_y), rim_size)
                
            else:  # barrier
                # Keep barriers simple
                barrier_rect = pygame.Rect(obstacle['x'] - obstacle['width']//2, 
                                         obstacle['y'] - obstacle['height']//2,
                                         obstacle['width'], obstacle['height'])
                pygame.draw.rect(self.screen, NEON_GREEN, barrier_rect)
                
                # Barrier stripes
                for i in range(0, obstacle['width'], 8):
                    stripe_rect = pygame.Rect(obstacle['x'] - obstacle['width']//2 + i, 
                                            obstacle['y'] - obstacle['height']//2,
                                            4, obstacle['height'])
                    pygame.draw.rect(self.screen, WHITE, stripe_rect)
    
    def draw_glowing_hud(self):
        """Draw glowing HUD with pixel fonts"""
        self.hud_glow_timer += self.dt
        self.speed_flicker += self.dt
        
        # Base glow intensity
        glow_base = 0.7 + 0.3 * math.sin(self.hud_glow_timer * 2)
        
        # HUD background panel
        hud_rect = pygame.Rect(10, 10, 250, 120)
        hud_surf = pygame.Surface((hud_rect.width, hud_rect.height))
        hud_surf.set_alpha(100)
        hud_surf.fill(DARK_PURPLE)
        self.screen.blit(hud_surf, hud_rect)
        
        # HUD border glow
        for i in range(3):
            border_rect = hud_rect.inflate(i * 2, i * 2)
            pygame.draw.rect(self.screen, NEON_CYAN, border_rect, 1)
        
        # Score with glow
        score_text = f"SCORE: {self.score:06d}"
        self.draw_glowing_text(score_text, self.hud_font, 20, 20, NEON_CYAN, glow_base)
        
        # Speed with flicker effect
        speed_flicker = 1.0 if int(self.speed_flicker * 8) % 10 < 8 else 0.6
        speed_color = tuple(int(c * speed_flicker) for c in NEON_PINK)
        speed_text = f"SPEED: {int(self.speed * 20):03d} KM/H"
        self.draw_glowing_text(speed_text, self.hud_font, 20, 45, speed_color, glow_base)
        
        # Distance
        distance_text = f"DIST:  {int(self.distance/10):05d}M"
        self.draw_glowing_text(distance_text, self.hud_font, 20, 70, NEON_GREEN, glow_base)
        
        # Time
        time_text = f"TIME:  {int(self.time_elapsed):03d}S"
        self.draw_glowing_text(time_text, self.hud_font, 20, 95, NEON_ORANGE, glow_base)
        
        # Right side HUD
        right_hud_rect = pygame.Rect(SCREEN_WIDTH - 200, 10, 180, 80)
        right_hud_surf = pygame.Surface((right_hud_rect.width, right_hud_rect.height))
        right_hud_surf.set_alpha(100)
        right_hud_surf.fill(DARK_PURPLE)
        self.screen.blit(right_hud_surf, right_hud_rect)
        
        # Right HUD border
        for i in range(3):
            border_rect = right_hud_rect.inflate(i * 2, i * 2)
            pygame.draw.rect(self.screen, NEON_PURPLE, border_rect, 1)
        
        # Level indicator
        level = int(self.speed - 4)
        level_text = f"LEVEL: {level:02d}"
        self.draw_glowing_text(level_text, self.hud_font, SCREEN_WIDTH - 190, 20, NEON_PURPLE, glow_base)
        
        # Danger indicator
        if len(self.obstacles) > 3:
            danger_text = "DANGER!"
            danger_color = tuple(int(c * (0.5 + 0.5 * math.sin(self.hud_glow_timer * 10))) for c in (255, 0, 0))
            self.draw_glowing_text(danger_text, self.hud_font, SCREEN_WIDTH - 190, 45, danger_color, 1.0)
    
    def draw_glowing_text(self, text, font, x, y, color, glow_intensity=1.0):
        """Draw text with glow effect"""
        # Glow layers
        glow_offsets = [(2, 2), (-2, -2), (2, -2), (-2, 2), (0, 2), (0, -2), (2, 0), (-2, 0)]
        glow_color = tuple(int(c * 0.5 * glow_intensity) for c in color)
        
        for offset in glow_offsets:
            glow_surface = font.render(text, True, glow_color)
            self.screen.blit(glow_surface, (x + offset[0], y + offset[1]))
        
        # Main text
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    def draw_simple_player_car(self):
        """Draw realistic player car with proper car shape and wheels"""
        car_width = 32
        car_height = 56
        
        # Car body (main rectangle)
        car_rect = pygame.Rect(self.player_x - car_width//2, self.player_y - car_height//2, 
                              car_width, car_height)
        pygame.draw.rect(self.screen, NEON_ORANGE, car_rect)
        
        # Car roof (smaller rectangle on top)
        roof_width = car_width - 8
        roof_height = car_height // 3
        roof_rect = pygame.Rect(self.player_x - roof_width//2, 
                               self.player_y - car_height//2 + 8, 
                               roof_width, roof_height)
        pygame.draw.rect(self.screen, (255, 140, 0), roof_rect)  # Darker orange
        
        # Windshield (front window)
        windshield_rect = pygame.Rect(self.player_x - (roof_width-4)//2, 
                                    self.player_y - car_height//2 + 10, 
                                    roof_width - 4, 8)
        pygame.draw.rect(self.screen, NEON_CYAN, windshield_rect)
        
        # Rear window
        rear_window_rect = pygame.Rect(self.player_x - (roof_width-4)//2, 
                                     self.player_y - car_height//2 + roof_height - 2, 
                                     roof_width - 4, 6)
        pygame.draw.rect(self.screen, NEON_CYAN, rear_window_rect)
        
        # Car outline
        pygame.draw.rect(self.screen, WHITE, car_rect, 2)
        pygame.draw.rect(self.screen, WHITE, roof_rect, 1)
        
        # Headlights
        pygame.draw.circle(self.screen, WHITE, (self.player_x - 8, self.player_y - car_height//2 + 4), 3)
        pygame.draw.circle(self.screen, WHITE, (self.player_x + 8, self.player_y - car_height//2 + 4), 3)
        
        # Wheels (4 wheels positioned correctly)
        wheel_color = (60, 60, 60)  # Dark gray
        wheel_rim_color = (200, 200, 200)  # Light gray
        
        # Front wheels
        front_wheel_y = self.player_y - car_height//2 + 12
        pygame.draw.circle(self.screen, wheel_color, (self.player_x - car_width//2 - 2, front_wheel_y), 6)
        pygame.draw.circle(self.screen, wheel_rim_color, (self.player_x - car_width//2 - 2, front_wheel_y), 4)
        pygame.draw.circle(self.screen, wheel_color, (self.player_x + car_width//2 + 2, front_wheel_y), 6)
        pygame.draw.circle(self.screen, wheel_rim_color, (self.player_x + car_width//2 + 2, front_wheel_y), 4)
        
        # Rear wheels
        rear_wheel_y = self.player_y + car_height//2 - 12
        pygame.draw.circle(self.screen, wheel_color, (self.player_x - car_width//2 - 2, rear_wheel_y), 6)
        pygame.draw.circle(self.screen, wheel_rim_color, (self.player_x - car_width//2 - 2, rear_wheel_y), 4)
        pygame.draw.circle(self.screen, wheel_color, (self.player_x + car_width//2 + 2, rear_wheel_y), 6)
        pygame.draw.circle(self.screen, wheel_rim_color, (self.player_x + car_width//2 + 2, rear_wheel_y), 4)
    def draw_simple_background(self):
        """Draw simple gradient background"""
        # Simple gradient from dark purple to pink
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(PURPLE_DARK[0] + (PINK_LIGHT[0] - PURPLE_DARK[0]) * ratio * 0.3)
            g = int(PURPLE_DARK[1] + (PINK_LIGHT[1] - PURPLE_DARK[1]) * ratio * 0.3)
            b = int(PURPLE_DARK[2] + (PINK_LIGHT[2] - PURPLE_DARK[2]) * ratio * 0.3)
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_simple_hud(self):
        """Draw simple HUD without complex effects"""
        # Score
        score_text = self.ui_font.render(f"SCORE: {self.score:06d}", True, NEON_CYAN)
        self.screen.blit(score_text, (10, 10))
        
        # Speed
        speed_text = self.ui_font.render(f"SPEED: {int(self.speed * 20):03d} KM/H", True, NEON_PINK)
        self.screen.blit(speed_text, (10, 45))
        
        # Distance
        distance_text = self.ui_font.render(f"DISTANCE: {int(self.distance/10):05d}M", True, NEON_GREEN)
        self.screen.blit(distance_text, (10, 80))
        
        # Time
        time_text = self.ui_font.render(f"TIME: {int(self.time_elapsed):03d}S", True, NEON_ORANGE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 200, 10))
        
        # Level
        level = int(self.speed - 4)
        level_text = self.ui_font.render(f"LEVEL: {level:02d}", True, NEON_PURPLE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 45))
    def handle_input(self):
        """Handle player input with updated car boundaries"""
        keys = pygame.key.get_pressed()
        
        if self.game_state == "PLAYING":
            road_width = 300
            road_left = SCREEN_WIDTH // 2 - road_width // 2
            road_right = SCREEN_WIDTH // 2 + road_width // 2
            
            # Account for new car width (32 pixels) plus wheel overhang
            car_half_width = 18  # 16 for car + 2 for wheel overhang
            
            if keys[pygame.K_LEFT] and self.player_x > road_left + car_half_width:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < road_right - car_half_width:
                self.player_x += self.player_speed
    
    def draw_enhanced_start_screen(self):
        """Draw enhanced start screen with retro effects"""
        # Animated title with glow
        title_glow = 0.8 + 0.2 * math.sin(time.time() * 3)
        
        # Title shadow/glow layers
        for i in range(5, 0, -1):
            shadow_color = tuple(int(c * 0.3 * title_glow) for c in NEON_PINK)
            title_shadow = self.title_font.render("RETRO RACER", True, shadow_color)
            shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + i, 150 + i))
            self.screen.blit(title_shadow, shadow_rect)
        
        # Main title
        title_text = self.title_font.render("RETRO RACER", True, NEON_PINK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle with flicker
        flicker = 1.0 if int(time.time() * 6) % 8 < 7 else 0.6
        subtitle_color = tuple(int(c * flicker) for c in NEON_CYAN)
        subtitle_text = self.ui_font.render("ARCADE STYLE", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Animated instructions
        instructions = [
            "USE LEFT/RIGHT ARROWS TO STEER",
            "AVOID OBSTACLES AND CARS", 
            "SURVIVE AS LONG AS POSSIBLE"
        ]
        
        for i, instruction in enumerate(instructions):
            wave_offset = math.sin(time.time() * 2 + i * 0.5) * 3
            color_intensity = 0.7 + 0.3 * math.sin(time.time() * 1.5 + i * 0.8)
            color = tuple(int(c * color_intensity) for c in NEON_GREEN)
            
            text = self.small_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 280 + i * 25 + wave_offset))
            self.screen.blit(text, text_rect)
    
    def draw_enhanced_game_over_screen(self):
        """Draw enhanced game over screen"""
        # Game Over title with dramatic effect
        game_over_glow = 0.6 + 0.4 * math.sin(time.time() * 4)
        
        # Multiple glow layers
        for i in range(8, 0, -1):
            glow_color = tuple(int(c * 0.2 * game_over_glow) for c in NEON_PINK)
            game_over_shadow = self.title_font.render("GAME OVER", True, glow_color)
            shadow_rect = game_over_shadow.get_rect(center=(SCREEN_WIDTH//2 + i//2, 150 + i//2))
            self.screen.blit(game_over_shadow, shadow_rect)
        
        # Main text
        game_over_text = self.title_font.render("GAME OVER", True, NEON_PINK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Stats with glow
        stats = [
            (f"FINAL SCORE: {self.score:06d}", NEON_CYAN, 250),
            (f"DISTANCE: {int(self.distance/10):05d}M", NEON_GREEN, 290),
            (f"TIME: {int(self.time_elapsed):03d}S", NEON_ORANGE, 330),
            (f"TOP SPEED: {int(self.speed * 20):03d} KM/H", NEON_PURPLE, 370)
        ]
        
        for text, color, y_pos in stats:
            self.draw_glowing_text(text, self.ui_font, SCREEN_WIDTH//2 - 150, y_pos, color, 0.8)
    def update_game(self):
        """Update game logic with sound effects"""
        if self.game_state == "PLAYING":
            # Update distance and time
            self.distance += self.speed
            self.time_elapsed += self.dt
            
            # Increase difficulty over time
            old_speed = int(self.speed)
            if self.distance > 0 and self.distance % 1000 == 0:
                self.speed = min(self.speed + 0.5, 12)
                if int(self.speed) > old_speed:
                    self.play_sound('beep')  # Level up sound
            
            # Update score based on distance
            self.score += 1
            
            # Play engine sound occasionally
            if random.randint(1, 120) == 1:
                self.play_sound('engine')
            
            # Check for collisions
            if self.check_collisions():
                self.play_sound('crash')
                self.game_state = "GAME_OVER"
    
    def handle_input(self):
        """Handle player input with improved road boundaries"""
        keys = pygame.key.get_pressed()
        
        if self.game_state == "PLAYING":
            # Calculate road boundaries at player position
            player_perspective = (self.player_y - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2)
            player_perspective = max(player_perspective, 0.8)  # Player is near bottom, so high perspective
            
            road_width = int(300 * player_perspective)
            road_left = SCREEN_WIDTH // 2 - road_width // 2
            road_right = SCREEN_WIDTH // 2 + road_width // 2
            
            if keys[pygame.K_LEFT] and self.player_x > road_left + 25:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < road_right - 25:
                self.player_x += self.player_speed
    
    def run(self):
        """Enhanced main game loop"""
        running = True
        mouse_pos = (0, 0)
        mouse_clicked = False
        
        while running:
            self.dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            mouse_clicked = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == "START":
                            self.play_sound('select')
                            self.game_state = "PLAYING"
                            self.reset_game()
                        elif self.game_state == "GAME_OVER":
                            self.play_sound('select')
                            self.game_state = "START"
                    
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == "GAME_OVER":
                            running = False
            
            # Update buttons
            if self.game_state == "START":
                self.start_button.update(mouse_pos, self.dt)
                if self.start_button.is_clicked(mouse_pos, mouse_clicked):
                    self.play_sound('select')
                    self.game_state = "PLAYING"
                    self.reset_game()
            
            elif self.game_state == "GAME_OVER":
                self.restart_button.update(mouse_pos, self.dt)
                self.quit_button.update(mouse_pos, self.dt)
                
                if self.restart_button.is_clicked(mouse_pos, mouse_clicked):
                    self.play_sound('select')
                    self.game_state = "START"
                elif self.quit_button.is_clicked(mouse_pos, mouse_clicked):
                    running = False
            
            # Handle continuous input
            self.handle_input()
            
            # Update game
            self.update_game()
            if self.game_state == "PLAYING":
                self.update_obstacles()
            
            # Draw everything with simple graphics
            self.draw_simple_background()
            
            if self.game_state == "START":
                self.draw_enhanced_start_screen()
                self.start_button.draw(self.screen)
                
            elif self.game_state == "PLAYING":
                self.draw_simple_road()
                self.draw_simple_obstacles()
                self.draw_simple_player_car()
                self.draw_simple_hud()
                
            elif self.game_state == "GAME_OVER":
                self.draw_simple_road()
                self.draw_simple_obstacles()
                self.draw_simple_player_car()
                self.draw_enhanced_game_over_screen()
                self.restart_button.draw(self.screen)
                self.quit_button.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def create_obstacle(self):
        """Create a simple obstacle"""
        road_width = 300
        road_left = SCREEN_WIDTH // 2 - road_width // 2
        road_right = SCREEN_WIDTH // 2 + road_width // 2
        
        obstacle_x = random.randint(road_left + 30, road_right - 30)
        obstacle_type = random.choice(['car', 'barrier'])
        
        obstacle = {
            'x': obstacle_x,
            'y': -50,  # Start from top of screen
            'type': obstacle_type,
            'width': 30 if obstacle_type == 'car' else 40,
            'height': 40 if obstacle_type == 'car' else 20
        }
        
        self.obstacles.append(obstacle)
    
    def update_obstacles(self):
        """Update obstacle positions - simple movement"""
        # Move obstacles down
        for obstacle in self.obstacles[:]:
            obstacle['y'] += self.speed + 2
            
            # Remove obstacles that are off screen
            if obstacle['y'] > SCREEN_HEIGHT + 50:
                self.obstacles.remove(obstacle)
                self.score += 10  # Points for passing obstacles
        
        # Spawn new obstacles
        self.obstacle_spawn_timer += 1
        spawn_rate = max(40 - (self.speed - 5) * 4, 20)
        
        if self.obstacle_spawn_timer >= spawn_rate:
            self.create_obstacle()
            self.obstacle_spawn_timer = 0
    
    def check_collisions(self):
        """Simple collision detection with updated car dimensions"""
        # Updated player car collision box to match new design
        player_rect = pygame.Rect(self.player_x - 16, self.player_y - 28, 32, 56)
        
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle['x'] - obstacle['width']//2,
                                      obstacle['y'] - obstacle['height']//2,
                                      obstacle['width'], obstacle['height'])
            
            if player_rect.colliderect(obstacle_rect):
                return True
        return False
    
    def reset_game(self):
        """Reset game to initial state"""
        self.score = 0
        self.distance = 0
        self.speed = 5
        self.time_elapsed = 0
        self.player_x = SCREEN_WIDTH // 2
        self.obstacles.clear()
        self.obstacle_spawn_timer = 0

if __name__ == "__main__":
    game = RetroRacer()
    game.run()
