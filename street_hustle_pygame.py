"""
╔══════════════════════════════════════════╗
║       STREET HUSTLE - PYGAME EDITION     ║
║       Built for: CSE Beginner            ║
║       Learn: Game Loop, Events, Drawing  ║
╚══════════════════════════════════════════╝

KEY CONCEPTS IN THIS FILE:
- pygame.init()         → starts pygame engine
- screen.fill()         → paints background every frame
- pygame.draw.rect()    → draws rectangles (buttons, bars)
- font.render()         → turns text into a drawable surface
- screen.blit()         → pastes anything onto the screen
- pygame.event.get()    → checks what user is doing
- clock.tick(60)        → limits game to 60 frames/second
"""

import pygame
import sys
import random
import time

# ============================================
# STEP 1: INITIALIZE PYGAME
# ============================================
pygame.init()

# ============================================
# STEP 2: CONSTANTS (values that never change)
# ============================================
SCREEN_W = 900
SCREEN_H = 600

# Color palette — RGB format (Red, Green, Blue) each 0-255
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
DARK_BG     = (15, 15, 25)          # main background
CARD_BG     = (25, 25, 40)          # card/panel background
ACCENT      = (255, 200, 0)         # gold accent
ACCENT2     = (255, 100, 50)        # orange accent
GREEN       = (50, 220, 100)
RED         = (220, 60, 60)
BLUE        = (80, 140, 255)
GRAY        = (80, 80, 100)
LIGHT_GRAY  = (160, 160, 180)
PURPLE      = (150, 80, 255)

# ============================================
# STEP 3: SCREEN + CLOCK SETUP
# ============================================
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("🔥 Street Hustle - Survive the Week")
clock = pygame.time.Clock()  # controls FPS

# ============================================
# STEP 4: FONTS
# ============================================
pygame.font.init()
font_big    = pygame.font.SysFont("Arial", 42, bold=True)
font_med    = pygame.font.SysFont("Arial", 24, bold=True)
font_small  = pygame.font.SysFont("Arial", 18)
font_tiny   = pygame.font.SysFont("Arial", 14)

# ============================================
# STEP 5: HELPER DRAWING FUNCTIONS
# ============================================

def draw_text(surface, text, font, color, x, y, center=False):
    """Renders text and draws it on the screen."""
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))

def draw_rounded_rect(surface, color, rect, radius=12):
    """Draws a rectangle with rounded corners."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_stat_bar(surface, label, value, max_val, x, y, color):
    """Draws a labeled progress bar for player stats."""
    bar_w = 200
    bar_h = 18
    fill_w = int((value / max_val) * bar_w)

    # Background bar
    draw_rounded_rect(surface, GRAY, (x, y, bar_w, bar_h), 6)
    # Filled portion
    if fill_w > 0:
        draw_rounded_rect(surface, color, (x, y, fill_w, bar_h), 6)
    # Label
    draw_text(surface, f"{label}: {value}", font_tiny, WHITE, x, y - 18)

def draw_button(surface, text, x, y, w, h, color, hover_color, mouse_pos):
    """
    Draws a clickable button.
    Returns True if mouse is hovering over it (so we can detect clicks).
    """
    rect = pygame.Rect(x, y, w, h)
    is_hovered = rect.collidepoint(mouse_pos)  # is mouse inside the button?
    
    # Change color on hover
    current_color = hover_color if is_hovered else color
    draw_rounded_rect(surface, current_color, rect, 10)
    
    # Button border
    pygame.draw.rect(surface, ACCENT, rect, 2, border_radius=10)
    
    # Button text
    draw_text(surface, text, font_small, WHITE, x + w // 2, y + h // 2, center=True)
    
    return is_hovered

# ============================================
# STEP 6: GAME SCREENS
# ============================================

def screen_intro():
    """
    The opening screen where player enters their name.
    Returns the player's name as a string.
    """
    name = ""
    active = True

    while active:
        mouse_pos = pygame.mouse.get_pos()

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    active = False  # move to next screen
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # delete last character
                else:
                    if len(name) < 16:
                        name += event.unicode  # add typed character

        # --- DRAWING ---
        screen.fill(DARK_BG)

        # Background grid effect
        for i in range(0, SCREEN_W, 60):
            pygame.draw.line(screen, (25, 25, 45), (i, 0), (i, SCREEN_H))
        for j in range(0, SCREEN_H, 60):
            pygame.draw.line(screen, (25, 25, 45), (0, j), (SCREEN_W, j))

        # Title
        draw_text(screen, "STREET HUSTLE", font_big, ACCENT, SCREEN_W // 2, 140, center=True)
        draw_text(screen, "Survive the Week", font_med, ACCENT2, SCREEN_W // 2, 195, center=True)
        draw_text(screen, "You're broke. You're hungry. Make it work.", font_small, LIGHT_GRAY, SCREEN_W // 2, 240, center=True)

        # Name input box
        draw_text(screen, "Enter your name:", font_med, WHITE, SCREEN_W // 2, 310, center=True)
        input_rect = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 50)
        draw_rounded_rect(screen, CARD_BG, input_rect, 10)
        pygame.draw.rect(screen, ACCENT, input_rect, 2, border_radius=10)
        draw_text(screen, name + "|", font_med, ACCENT, SCREEN_W // 2, 355, center=True)

        # Start hint
        if name.strip():
            draw_text(screen, "Press ENTER to start", font_small, GREEN, SCREEN_W // 2, 420, center=True)
        else:
            draw_text(screen, "Type your name above", font_small, GRAY, SCREEN_W // 2, 420, center=True)

        draw_text(screen, "Built with Python + Pygame 🐍", font_tiny, GRAY, SCREEN_W // 2, SCREEN_H - 30, center=True)

        pygame.display.flip()  # UPDATE THE SCREEN (very important!)
        clock.tick(60)

    return name.strip()


def screen_story(player, day_num, story_text, options):
    """
    Generic story screen with choices.
    Shows: story text + 3 clickable buttons
    Returns: which option was clicked (1, 2, or 3)
    """
    chosen = None

    # Button layout
    btn_w, btn_h = 700, 55
    btn_x = SCREEN_W // 2 - btn_w // 2
    btn_positions = [
        (btn_x, 340),
        (btn_x, 410),
        (btn_x, 480),
    ]
    btn_colors = [
        (50, 100, 200),   # blue
        (180, 80, 30),    # orange
        (60, 160, 80),    # green
    ]
    btn_hover_colors = [
        (80, 130, 255),
        (220, 110, 50),
        (80, 200, 100),
    ]

    while chosen is None:
        mouse_pos = pygame.mouse.get_pos()

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (bx, by) in enumerate(btn_positions):
                    if i < len(options):
                        btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
                        if btn_rect.collidepoint(mouse_pos):
                            chosen = i + 1  # 1, 2, or 3

        # --- DRAWING ---
        screen.fill(DARK_BG)

        # Top banner
        draw_rounded_rect(screen, CARD_BG, (0, 0, SCREEN_W, 80))
        draw_text(screen, f"DAY {day_num}", font_big, ACCENT, 40, 20)
        draw_text(screen, f"{player['name']}  💰Rs.{player['money']}  ⚡{player['energy']}%  🔥{player['reputation']}", font_small, LIGHT_GRAY, 220, 35)

        # Stat bars
        draw_stat_bar(screen, "Money", min(player['money'], 2000), 2000, SCREEN_W - 260, 15, GREEN)
        draw_stat_bar(screen, "Energy", player['energy'], 100, SCREEN_W - 260, 55, BLUE)

        # Story card
        draw_rounded_rect(screen, CARD_BG, (50, 100, SCREEN_W - 100, 220), 14)
        pygame.draw.rect(screen, ACCENT2, (50, 100, SCREEN_W - 100, 220), 2, border_radius=14)

        # Word wrap story text
        words = story_text.split()
        lines = []
        current_line = ""
        for word in words:
            test = current_line + word + " "
            if font_small.size(test)[0] < SCREEN_W - 160:
                current_line = test
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines[:6]):  # max 6 lines
            draw_text(screen, line.strip(), font_small, WHITE, 80, 120 + i * 30)

        # Choice label
        draw_text(screen, "WHAT DO YOU DO?", font_med, ACCENT, SCREEN_W // 2, 315, center=True)

        # Buttons
        for i, (bx, by) in enumerate(btn_positions):
            if i < len(options):
                draw_button(screen, options[i], bx, by, btn_w, btn_h,
                           btn_colors[i], btn_hover_colors[i], mouse_pos)

        pygame.display.flip()
        clock.tick(60)

    return chosen


def screen_result(player, result_text, color=WHITE):
    """
    Shows the outcome of a player's choice.
    Waits for a click to continue.
    """
    waiting = True
    alpha = 0  # for fade-in effect

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(DARK_BG)

        # Result card
        draw_rounded_rect(screen, CARD_BG, (100, 150, SCREEN_W - 200, 280), 16)
        pygame.draw.rect(screen, color, (100, 150, SCREEN_W - 200, 280), 3, border_radius=16)

        draw_text(screen, "RESULT", font_big, color, SCREEN_W // 2, 185, center=True)

        # Word wrap result text
        words = result_text.split()
        lines = []
        current_line = ""
        for word in words:
            test = current_line + word + " "
            if font_med.size(test)[0] < SCREEN_W - 260:
                current_line = test
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines[:5]):
            draw_text(screen, line.strip(), font_med, WHITE, SCREEN_W // 2, 240 + i * 35, center=True)

        draw_text(screen, "Click or press any key to continue...", font_small, GRAY, SCREEN_W // 2, SCREEN_H - 60, center=True)

        pygame.display.flip()
        clock.tick(60)


def screen_status(player, message=""):
    """Shows current player stats. Waits for click to continue."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(DARK_BG)

        draw_text(screen, "STATUS UPDATE", font_big, ACCENT, SCREEN_W // 2, 60, center=True)
        if message:
            draw_text(screen, message, font_med, LIGHT_GRAY, SCREEN_W // 2, 110, center=True)

        # Stat cards
        stats = [
            ("💰 Money",      f"Rs.{player['money']}",      GREEN),
            ("⚡ Energy",      f"{player['energy']}%",       BLUE),
            ("🔥 Reputation", f"{player['reputation']}/100", PURPLE),
            ("📅 Day",        f"{player['day']} of 3",      ACCENT),
        ]

        for i, (label, val, color) in enumerate(stats):
            cx = 150 + (i % 2) * 420
            cy = 200 + (i // 2) * 140
            draw_rounded_rect(screen, CARD_BG, (cx - 130, cy - 40, 280, 100), 14)
            pygame.draw.rect(screen, color, (cx - 130, cy - 40, 280, 100), 2, border_radius=14)
            draw_text(screen, label, font_small, LIGHT_GRAY, cx, cy - 15, center=True)
            draw_text(screen, val, font_big, color, cx, cy + 20, center=True)

        draw_text(screen, "Click or press any key to continue...", font_small, GRAY, SCREEN_W // 2, SCREEN_H - 40, center=True)

        pygame.display.flip()
        clock.tick(60)


def screen_final(player):
    """Final results screen with ending."""
    waiting = True

    # Determine ending
    if player["money"] >= 1500 and player["reputation"] >= 70:
        ending = "THE LEGEND 🏆"
        desc = "You survived AND built your name. People respect you. This is just the beginning."
        color = ACCENT
    elif player["money"] >= 800:
        ending = "SURVIVOR ✅"
        desc = "You made it. Not flashy, but you handled business. Solid. Keep grinding."
        color = GREEN
    elif player["reputation"] >= 70:
        ending = "THE SCHOLAR 🎓"
        desc = "Broke but respected. Your reputation will pay off later. Stay consistent."
        color = BLUE
    else:
        ending = "BACK TO ZERO 😤"
        desc = "Rough week bro. But you learned something. Every L is a lesson. Run it again."
        color = RED

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(DARK_BG)

        # Background effect
        for i in range(0, SCREEN_W, 40):
            pygame.draw.line(screen, (20, 20, 35), (i, 0), (i, SCREEN_H))

        draw_text(screen, "WEEK COMPLETE", font_big, ACCENT, SCREEN_W // 2, 70, center=True)

        draw_rounded_rect(screen, CARD_BG, (80, 120, SCREEN_W - 160, 200), 16)
        pygame.draw.rect(screen, color, (80, 120, SCREEN_W - 160, 200), 3, border_radius=16)

        draw_text(screen, f"ENDING: {ending}", font_big, color, SCREEN_W // 2, 160, center=True)

        # Word wrap desc
        words = desc.split()
        lines, current_line = [], ""
        for word in words:
            test = current_line + word + " "
            if font_small.size(test)[0] < SCREEN_W - 220:
                current_line = test
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        for i, line in enumerate(lines):
            draw_text(screen, line.strip(), font_small, WHITE, SCREEN_W // 2, 215 + i * 28, center=True)

        # Final stats
        draw_text(screen, f"Final Money: Rs.{player['money']}    Energy: {player['energy']}%    Rep: {player['reputation']}/100",
                  font_med, LIGHT_GRAY, SCREEN_W // 2, 360, center=True)

        draw_text(screen, f"GG {player['name']}. Built with Python 🐍 + Pygame", font_small, GRAY, SCREEN_W // 2, 440, center=True)
        draw_text(screen, "Press any key to exit", font_small, GRAY, SCREEN_W // 2, SCREEN_H - 40, center=True)

        pygame.display.flip()
        clock.tick(60)


# ============================================
# STEP 7: GAME LOGIC (same as before, now with screens)
# ============================================

def day_one(player):
    player["day"] = 1
    story = (
        f"You wake up in your room. Rs.{player['money']} in your pocket. "
        "You check your phone. Two messages waiting. Your friend wants help "
        "selling phone cases near the bus stop. Your lecturer posted about an "
        "extra class with attendance marked. Or you could just rest at home."
    )
    options = [
        "1. Help friend sell phone cases (hustle 💰)",
        "2. Attend the extra class (education 📚)",
        "3. Stay home and rest (recovery ⚡)",
    ]
    choice = screen_story(player, 1, story, options)

    if choice == 1:
        earned = random.randint(300, 700)
        player["money"] += earned
        player["energy"] -= 30
        player["reputation"] += 10
        screen_result(player, f"You hustled hard at the bus stop. Made Rs.{earned}! Rep up. But you're tired now.", GREEN)

    elif choice == 2:
        player["energy"] -= 20
        player["reputation"] += 15
        screen_result(player, "3 hours of lectures. Brain fried. But the lecturer noticed you and mentioned an IT internship opportunity.", BLUE)

    elif choice == 3:
        player["energy"] = min(100, player["energy"] + 20)
        screen_result(player, "You stayed home. Ate noodles. Watched YouTube. Energy restored. Nothing gained though. That's life.", LIGHT_GRAY)

    return player


def day_two(player):
    player["day"] = 2
    story = (
        f"Your classmate slides up to you. 'Bro, I need Rs.200. "
        f"I'll pay you back tomorrow. Promise.' You have Rs.{player['money']} right now. "
        "Do you trust him? Or do you protect your bag?"
    )
    options = [
        "1. Lend full Rs.200 (trust 🤝)",
        "2. Refuse — you're broke too (protect 🛡️)",
        "3. Give Rs.100 only (compromise ⚖️)",
    ]
    choice = screen_story(player, 2, story, options)

    if choice == 1:
        if random.random() < 0.6:
            player["money"] += 200
            player["reputation"] += 5
            screen_result(player, "He actually paid you back! Rare W. Friendship and money both intact.", GREEN)
        else:
            player["money"] -= 200
            player["reputation"] -= 5
            screen_result(player, "He went ghost. Doesn't pick up calls. Classic. You lost Rs.200 and some trust.", RED)

    elif choice == 2:
        player["reputation"] -= 5
        screen_result(player, "You said no. He looked upset. People talk. Reputation dropped a bit, but your money is safe.", ACCENT2)

    elif choice == 3:
        player["money"] -= 100
        player["reputation"] += 3
        screen_result(player, "You gave Rs.100. Fair compromise. He appreciated it. You kept some dignity and some cash.", BLUE)

    return player


def day_three(player):
    player["day"] = 3
    story = (
        f"Last day before money comes from home. You have Rs.{player['money']} and "
        f"{player['energy']}% energy. A local startup needs a student to help set up "
        "their event for Rs.1000 for 5 hours. But you also have an assignment due tonight. "
        "What's your move?"
    )
    options = [
        "1. Take the startup job (money 💰)",
        "2. Finish the assignment (grades 📝)",
        "3. Try to do BOTH (risky ⚠️)",
    ]
    choice = screen_story(player, 3, story, options)

    if choice == 1:
        player["money"] += 1000
        player["energy"] -= 40
        player["reputation"] += 20
        screen_result(player, "You crushed it at the event. Rs.1000 secured. The startup founder remembered your name. That's a real connection.", GREEN)

    elif choice == 2:
        player["reputation"] += 10
        player["energy"] -= 10
        screen_result(player, "Submitted on time. Lecturer was impressed. No money gained, but your academic rep is solid.", BLUE)

    elif choice == 3:
        if player["energy"] >= 60:
            player["money"] += 1000
            player["energy"] -= 60
            player["reputation"] += 25
            screen_result(player, "You somehow pulled it off! Job done. Assignment submitted. You're built different. Absolute W.", ACCENT)
        else:
            player["reputation"] -= 10
            player["energy"] -= 50
            screen_result(player, "Bro you were already running on empty. Messed up both. Assignment incomplete. Left the job early. Big L.", RED)

    return player


# ============================================
# STEP 8: MAIN GAME LOOP
# ============================================

def main():
    # Get player name from intro screen
    name = screen_intro()

    # Initialize player stats
    player = {
        "name": name,
        "money": 500,
        "energy": 100,
        "reputation": 50,
        "day": 1,
    }

    # Show starting status
    screen_status(player, "Your journey begins. Rs.500. 3 days. Survive.")

    # Run each day
    player = day_one(player)
    screen_status(player, "End of Day 1")

    player = day_two(player)
    screen_status(player, "End of Day 2")

    player = day_three(player)

    # Show final results
    screen_final(player)

    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    main()