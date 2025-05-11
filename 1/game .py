import pygame
import sys
import os
import random

pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()
small_font = pygame.font.SysFont("comicsansms", 24)

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("comicsansms", 36)
big_font = pygame.font.SysFont("comicsansms", 48, bold=True)

# File paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
get_path = lambda f: os.path.join(BASE_PATH, f)
HIGHSCORE_FILE = get_path("highscore.txt")
HIGHAIRSTREAK_FILE = get_path("highairstreak.txt")

# Load images
bg_img = pygame.transform.scale(pygame.image.load(get_path("background.png")), (WIDTH, HEIGHT))
mario_img = pygame.transform.scale(pygame.image.load(get_path("mario.png")), (40, 60))
goomba_img = pygame.transform.scale(pygame.image.load(get_path("goomba.png")), (40, 40))
heart_img = pygame.transform.scale(pygame.image.load(get_path("heart.png")), (30, 30))

# Load sounds
jump_sound = pygame.mixer.Sound(get_path("jump.wav"))
game_over_sound = pygame.mixer.Sound(get_path("game_over.wav"))
pygame.mixer.music.load(get_path("start.wav"))

# Game floor
floor_y = HEIGHT - 50

# Helper functions
def draw_text(text, x, y, font=font, color=(0, 0, 0)):
    # Draw text on the screen
    screen.blit(font.render(text, True, color), (x, y))

def wait_screen(title, subtitle, play_music=False, is_muted=False):
    # Display a waiting screen with a title and subtitle
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Super Mario - Start Screen")
    if play_music and not is_muted and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("segoeui", 60, bold=True)
    subtitle_font = pygame.font.SysFont("segoeui", 20)

    while True:
        screen.fill((30, 30, 30))
        title_surf = title_font.render(title, True, (255, 215, 0))
        subtitle_surf = subtitle_font.render(subtitle, True, (255, 255, 255))
        screen_rect = screen.get_rect()
        title_rect = title_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery - 100))
        subtitle_rect = subtitle_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery + 50))
        screen.blit(title_surf, title_rect)
        screen.blit(subtitle_surf, subtitle_rect)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

def wait_for_key():
    # Wait for a key press to continue
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def load_high_airstreak():
    # Load the highest air streak from a file
    try:
        with open(HIGHAIRSTREAK_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_airstreak(streak):
    # Save the highest air streak to a file
    with open(HIGHAIRSTREAK_FILE, "w") as f:
        f.write(str(streak))

def load_highscore():
    # Load the high score from a file
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    # Save the high score to a file
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def screen_flash():
    # Flash the screen red for a short duration
    for _ in range(3):
        screen.fill((255, 0, 0))
        pygame.display.update()
        pygame.time.delay(60)
        screen.blit(bg_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(60)

def flash_mario(player_x, player_y, bg_x, enemy_x):
    # Flash Mario to indicate damage
    for i in range(3):
        clock.tick(60)
        screen.blit(bg_img, (bg_x - WIDTH, 0))
        screen.blit(bg_img, (bg_x, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))
        screen.blit(goomba_img, (enemy_x, floor_y - 40))
        white_mario = mario_img.copy()
        white_mario.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(white_mario, (player_x, player_y))
        pygame.display.update()
        pygame.time.delay(80)

        screen.blit(bg_img, (bg_x - WIDTH, 0))
        screen.blit(bg_img, (bg_x, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))
        screen.blit(goomba_img, (enemy_x, floor_y - 40))
        screen.blit(mario_img, (player_x, player_y))
        pygame.display.update()
        pygame.time.delay(80)

def short_fall_animation(x, y, enemy_x):
    # Animate a short fall
    screen_flash()
    fall_speed = 3
    for _ in range(15):
        clock.tick(60)
        y += fall_speed
        fall_speed += 0.3
        bg_x = pygame.time.get_ticks() // 5 % WIDTH
        screen.blit(bg_img, (bg_x - WIDTH, 0))
        screen.blit(bg_img, (bg_x, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))
        screen.blit(goomba_img, (enemy_x, floor_y - 40))
        screen.blit(mario_img, (x, y))
        pygame.display.update()
    flash_mario(x, y, bg_x, enemy_x)

def fall_animation(x, y):
    # Animate a long fall
    fall_speed = 5
    while y < HEIGHT:
        clock.tick(60)
        y += fall_speed
        fall_speed += 0.5
        bg_x = pygame.time.get_ticks() // 5 % WIDTH
        screen.blit(bg_img, (bg_x - WIDTH, 0))
        screen.blit(bg_img, (bg_x, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))
        screen.blit(mario_img, (x, y))
        pygame.display.update()

new_game = False
def toggle_mute(is_muted, restart=False):
    # Toggle mute/unmute for the game
    global new_game
    if is_muted:
        if restart or new_game:
            pygame.mixer.music.play(-1)
            new_game = False
        else:
            pygame.mixer.music.unpause()
        jump_sound.set_volume(1)
        game_over_sound.set_volume(1)
        return False
    else:
        pygame.mixer.music.pause()
        jump_sound.set_volume(0)
        game_over_sound.set_volume(0)
        return True

def toggle_pause(is_paused):
    # Toggle pause/unpause for the game
    return not is_paused

def show_bonus_points(points, mario_x, mario_y, bonus_start_time):
    """Display bonus points above Mario for one second without freezing the game."""
    bonus_font = pygame.font.SysFont("comicsansms", 50, bold=True)
    bonus_text = bonus_font.render(f"+{points}", True, (255, 255, 0))  # Yellow text
    text_x = mario_x - 10  # Slightly offset to center above Mario
    text_y = mario_y - 100  # Position higher above Mario's head

    # Check if one second has passed since the bonus started
    if pygame.time.get_ticks() - bonus_start_time < 500:  # 1000 milliseconds = 1 second
        screen.blit(bonus_text, (text_x, text_y))

def show_muted_status(is_muted):
    """Display 'Muted' in white if the game is muted."""
    if is_muted:
        muted_font = pygame.font.SysFont("comicsansms", 30, bold=True)
        muted_text = muted_font.render("Muted", True, (255, 255, 255))  # White text
        screen.blit(muted_text, (WIDTH - 250, 0))  # Display in the top-right corner

# Main game loop
def main_game(is_muted=False):  
    player_x, player_y = 100, floor_y - 60
    vel_y, gravity, jump_force = 0, 0.8, -15
    on_ground = True
    score, timer = 0, 0
    time_since_last_score = 0  # משתנה לספירת הזמן שחלף מאז העדכון האחרון של הניקוד
    enemy_x = 800
    enemy_speed = 3
    bg_x = 0
    lives = 3
    highscore = load_highscore()
    max_saved_streak = load_high_airstreak()
    game_start_time = pygame.time.get_ticks()  # Start time
    total_paused_time = 0  # Total pause time
    paused_time = None  # Additional time saved during pause
    elapsed_time = 0  # Total elapsed time
    aerial_kill_streak = 0
    highest_aerial_streak = 0  # Highest streak
    total_kills = 0  # Total kills
    is_paused = False  # Pause flag

    while True:
        dt = clock.tick(60)  # Time elapsed since the last frame (in milliseconds)

        if not is_paused:  # Update the score only if the game is not paused
            time_since_last_score += dt  # Add the elapsed time to the variable

            # Update the score if one second has passed
            if time_since_last_score >= 1000:
                score += 1
                if score > highscore:
                    highscore = score
                time_since_last_score = 0  # Reset the elapsed time

        # Update enemy speed based on elapsed time and total kills
        enemy_speed = 3 + elapsed_time * 0.3 + total_kills * 0.1  

        if is_paused:
            if paused_time is None:  # If the pause just started
                paused_time = pygame.time.get_ticks()  # Save the current time
        else:
            if paused_time is not None:  # If the game was paused
                total_paused_time += pygame.time.get_ticks() - paused_time  # Subtract the pause duration
                paused_time = None  # Reset the pause time
            elapsed_time = (pygame.time.get_ticks() - game_start_time - total_paused_time) // 1000  # Calculate total elapsed time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Mute/unmute sound
                    was_muted = is_muted
                    is_muted = toggle_mute(is_muted, restart=False)
                    if not is_muted and was_muted:  # If unmuted after being muted
                        pygame.mixer.music.unpause()  # Resume the music
                        jump_sound.set_volume(1)
                        game_over_sound.set_volume(1)
                if event.key == pygame.K_p:  # Pause/unpause game
                    is_paused = toggle_pause(is_paused)
                if event.key == pygame.K_r:  # Restart game
                    if not is_muted:  # Play sounds only if not muted
                        pygame.mixer.music.play(-1)  # Restart the background music
                    return is_muted  # Return the current mute state

        if is_paused:
            # Display the background
            screen.blit(bg_img, (bg_x - WIDTH, 0))  # Display the background (left part)
            screen.blit(bg_img, (bg_x, 0))  # Display the background (right part)

            # Display the floor
            pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))  # Display the floor

            # Display the player and enemies in their current positions
            screen.blit(mario_img, (player_x, player_y))  # Display the player
            screen.blit(goomba_img, (enemy_x, floor_y - 40))  # Display the enemy

            # Display the score, high score, and other stats
            draw_text(f"Score: {score}", 10, 10, font=small_font)
            draw_text(f"High Score: {highscore}", 10, 50, font=small_font)
            draw_text(f"Air Streak: {highest_aerial_streak}", 10, 90, font=small_font)  # Display the highest streak
            draw_text(f"Best Air Streak: {max_saved_streak}", 10, 130, font=small_font)
            draw_text(f"Time: {elapsed_time}s", 350, 10, font=small_font)
            draw_text(f"Kills: {total_kills}", 350, 50, font=small_font)  # Display the total number of kills

            # Display the player's lives
            for i in range(lives):
                screen.blit(heart_img, (WIDTH - (i + 1) * 40, 10))

            # Display the "Paused" text
            draw_text("Paused", WIDTH // 2 - 100, HEIGHT // 2 - 100, font=big_font, color=(255, 255, 255))

            # Display the mute status if the game is muted
            if is_muted:
                show_muted_status(is_muted)

            # Update the screen
            pygame.display.update()
            continue  # Skip the rest of the game loop to keep the game paused



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_x -= 5
        if keys[pygame.K_RIGHT]: player_x += 5
        if keys[pygame.K_SPACE] and on_ground:
            if not is_muted:
                jump_sound.play()
            vel_y = jump_force
            on_ground = False

        vel_y += gravity
        player_y += vel_y
        if player_y + 60 >= floor_y:
            player_y = floor_y - 60
            vel_y = 0
            on_ground = True
            aerial_kill_streak = 0

        enemy_x -= enemy_speed
        if enemy_x < -40:
            enemy_x = random.randint(800, 1000)

        bg_x = (bg_x - 1) % WIDTH
        screen.blit(bg_img, (bg_x - WIDTH, 0))
        screen.blit(bg_img, (bg_x, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, 50))

        screen.blit(mario_img, (player_x, player_y))
        screen.blit(goomba_img, (enemy_x, floor_y - 40))

        draw_text(f"Score: {score}", 10, 10, font=small_font)
        draw_text(f"High Score: {highscore}", 10, 50, font=small_font)
        draw_text(f"Air Streak: {highest_aerial_streak}", 10, 90, font=small_font)  # Display the highest streak
        draw_text(f"Best Air Streak: {max_saved_streak}", 10, 130, font=small_font) 
        draw_text(f"Time: {elapsed_time}s", 350, 10, font=small_font)
        draw_text(f"Kills: {total_kills}", 350, 50, font=small_font)  # Display the total number of kills

        for i in range(lives):
            screen.blit(heart_img, (WIDTH - (i + 1) * 40, 10))

        player_rect = pygame.Rect(player_x, player_y, 40, 60)
        enemy_rect = pygame.Rect(enemy_x, floor_y - 40, 40, 40)

        if player_rect.colliderect(enemy_rect):
            if vel_y > 0 and player_y + 60 <= floor_y - 20:
                vel_y = jump_force / 1.2
                ##score += 5
                total_kills += 1  # Update total kills
                aerial_kill_streak += 1  # Update aerial kill streak

                # Update the highest streak
                if aerial_kill_streak > highest_aerial_streak:
                    highest_aerial_streak = aerial_kill_streak
                if highest_aerial_streak > max_saved_streak:
                    max_saved_streak = highest_aerial_streak  
                    save_high_airstreak(max_saved_streak)           

                # Calculate bonus points based on the streak
                bonus_points = 5
                if aerial_kill_streak == 2:
                    bonus_points = 50
                elif aerial_kill_streak == 3:
                    bonus_points = 200
                elif aerial_kill_streak == 4:
                    bonus_points = 1000
                elif aerial_kill_streak == 5:
                    bonus_points = 5000
                elif aerial_kill_streak == 6:
                    bonus_points = 10000
                elif aerial_kill_streak == 7:
                    bonus_points = 20000
                elif aerial_kill_streak == 8:
                    bonus_points = 50000
                elif aerial_kill_streak == 9:
                    bonus_points = 100000
                elif aerial_kill_streak == 10:
                    bonus_points = 1000000

                # Add bonus points to the score
                score += bonus_points

                # Start the bonus display timer
                bonus_start_time = pygame.time.get_ticks()

                # Show bonus points above Mario
                show_bonus_points(bonus_points, player_x, player_y, bonus_start_time)

                enemy_x = random.randint(800, 1000)
            else:
                if aerial_kill_streak > highest_aerial_streak:
                    highest_aerial_streak = aerial_kill_streak
                if highest_aerial_streak > max_saved_streak:
                        max_saved_streak = highest_aerial_streak
                        save_high_airstreak(max_saved_streak)   
                aerial_kill_streak = 0
                lives -= 1
                pygame.mixer.music.pause()
                game_over_sound.play()
                short_fall_animation(player_x, player_y, enemy_x)
                if lives <= 0:
                    global new_game  
                    new_game = True  # Set new_game to True to indicate a new game

                    fall_animation(player_x, player_y)
                    if score > highscore:
                        highscore = score
                        save_highscore(score)
                        
                    if highest_aerial_streak > max_saved_streak:
                        max_saved_streak = highest_aerial_streak    
                        save_high_airstreak(max_saved_streak)
                    
                    pygame.mixer.music.stop()  # Stop the music completely

                    # Loop to display the "Game Over" screen for 5 seconds
                    lock_start_time = pygame.time.get_ticks()
                    while pygame.time.get_ticks() - lock_start_time < 3000:  # 5000 milliseconds = 5 seconds
                        screen.fill((30, 30, 30))  # Dark gray background
                        draw_text("Game Over", WIDTH // 2 - 100, HEIGHT // 2 - 150, font=big_font, color=(255, 0, 0))
                        draw_text(f"Score: {score}", WIDTH // 2 - 100, HEIGHT // 2-50, font=font, color=(255, 255, 255))
                        draw_text(f"High Score: {highscore}", WIDTH // 2 - 100, HEIGHT // 2 , font=font, color=(255, 255, 255))
                        draw_text(f"Air Streak: {highest_aerial_streak}", WIDTH // 2 - 100, HEIGHT // 2 + 50, font=font, color=(255, 255, 255))
                        draw_text(f"Best Air Streak: {max_saved_streak}", WIDTH // 2 - 100, HEIGHT // 2 + 100, font=font, color=(255, 255, 255))
                        draw_text(f"Time: {elapsed_time}s", WIDTH // 2 - 100, HEIGHT // 2 + 150, font=font, color=(255, 255, 255))
                        pygame.display.update()

                        # Ignore all keyboard and mouse events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                    # Return to the start screen after 5 seconds
                    wait_screen("Records", f"High Score: {highscore} | Best Air Streak: {max_saved_streak} | Press any key to restart", play_music=False)
                    if not is_muted:  # Play sounds only if not muted
                        pygame.time.delay(500)  # Small delay to separate sounds

                        pygame.mixer.music.play(-1) 
                    return is_muted
                else:
                    pygame.time.delay(2000)
                    enemy_x = random.randint(800, 1000)
                    if not is_muted:  # Only unpause music if not muted
                        pygame.mixer.music.unpause()

        if 'bonus_start_time' in locals() and pygame.time.get_ticks() - bonus_start_time < 1000:
            show_bonus_points(bonus_points, player_x, player_y, bonus_start_time)

        show_muted_status(is_muted)  # Display muted status

        pygame.display.update()



def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    return True

is_muted = False  # Initialize mute state
while True:
    if not is_muted and not pygame.mixer.music.get_busy():  # Play music only if not muted and not already playing
        pygame.mixer.music.play(-1) 
        jump_sound.set_volume(1)
        game_over_sound.set_volume(1)
        
        # Start the background music
    wait_screen("Welcome to Super Mario!", "Press any key to start", play_music=True, is_muted=is_muted)
    
    # Restart the background music if the game is not muted
    is_muted = main_game(is_muted)  # Pass and retrieve the mute state
    if not is_muted:  # Restart music if unmuted after the game restarts
        toggle_mute(is_muted, restart=True)
