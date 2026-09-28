"""VishGuard - Cybersecurity Awareness Simulator."""
#CLONE OF PHISHGUARD - CHANGE ACCORDINGLY
from tkinter import font

# ---- IMPORTS  ----
import streamlit as st
#import content
#import ui
import pygame, sys, json, random, os  
pygame.init()

"""
oshc.py - Medibank OSHC Awareness module
==========================================
Owns: plain-language OSHC explainer sections, each followed by a
short comprehension question (FR05).

Reference: Report section 1.1.3 (Accessibility) and 1.1.1,
Table 3.4.2 (oshc.py row).
"""

#DIRECTORY DEFINITIONS for assets (images, fonts, audio etc.)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio") #Not sure if audio required for this module, added for now
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
# ── Window & colours ──────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1000, 700  # fixed window size for the game display
MIN_WIDTH, MIN_HEIGHT = 640, 480   # smallest size the window can be dragged to
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create the main game window
pygame.display.set_caption("What is OSHC?")  # set the window title shown by the OS
#COLOURS TAKEN FROM PHISHGUARD AND CHANGED ACCORDINGLY
WHITE  = (255, 255, 255)  # white used for text and button borders
BLACK  = (15,  15,  15)   # dark background color for the game screens
MEDI_BLUE = (5, 125, 194)  # blue from Medibank logo, used for buttons and highlights
GREEN  = (50,  200, 90)   # green for safe actions and success feedback
RED    = (217, 4,   50)   # Red taken from Medibank website, used for Medibank logo and error feedback
GREY   = (180, 180, 180)  # gray for secondary text and borders
YELLOW = (255, 210, 50)   # yellow for warnings and educational tips
DARK   = (50,  50,  70)   # darker tone 

FPS = 60  # frames per second for the game loop

# ── Fonts ─────────────────────────────────────────────────────────────────────
HEADING_FONT_SIZE = 36
BODY_FONT_SIZE = 20
SMALL_FONT_SIZE = 14

generic_font = pygame.font.SysFont("Arial", HEADING_FONT_SIZE)  # create a font
HEADING_FONT_PATH = os.path.join(FONTS_DIR, "blocky.ttf")
font_title = pygame.font.Font(HEADING_FONT_PATH, 16)


# ── Draw helpers ──────────────────────────────────────────────────────────────
def draw_text(text, font, colour, x, y):
    """Draw text with its top-left corner at (x, y). Returns the rect."""
    surf = font.render(text, True, colour)
    rect = surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)
    return rect

def draw_text_centre(text, font, colour, y):
    """Render text horizontally centred at the given y-coordinate."""
    surf = font.render(text, True, colour)
    screen.blit(surf, surf.get_rect(center=(screen.get_width() // 2, y)))

#BUTTON FOR TESTING PURPOSES
def draw_button(label, font, rect, fill, text_colour=WHITE, hover=False):
    """Draw a rounded button. Hover lightens the fill slightly."""
    colour = tuple(min(255, c + 25) for c in fill) if hover else fill
    pygame.draw.rect(screen, colour, rect, border_radius=10)
    surf = font.render(label, True, text_colour)
    screen.blit(surf, surf.get_rect(center=rect.center))


def wrap_text(text, font, max_width):
    """Split text into lines that fit within max_width pixels."""
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if font.size(test)[0] <= max_width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

CUSTOM_FONT_PATH = os.path.join(FONTS_DIR, "font.ttf")
FONT_CHOICES = ["Arial", "Verdana", "Calibri", "Segoe UI", "Tahoma"]
if os.path.exists(CUSTOM_FONT_PATH):
    FONT_CHOICES.insert(0, CUSTOM_FONT_PATH)   # custom font is first choice if present
 

_font_cache = {}

def get_font(name, size, bold=False):
    """Return a cached pygame Font. Falls back to a system font if the
    custom font file is missing or can't be loaded."""
    key = (name, size, bold)
    if key not in _font_cache:
        try:
            if name.lower().endswith((".ttf", ".otf")):
                f = pygame.font.Font(name, size)
                f.set_bold(bold)
            else:
                f = pygame.font.SysFont(name, size, bold=bold)
        except (FileNotFoundError, pygame.error):
            f = pygame.font.SysFont("Arial", size, bold=bold)
        _font_cache[key] = f
    return _font_cache[key]


def draw_paragraph(text, font, colour, x, y, max_width, line_gap=6):
    """Draw wrapped text. Returns the y-coordinate below the last line."""
    for line in wrap_text(text, font, max_width):
        draw_text(line, font, colour, x, y)
        y += font.get_linesize() + line_gap
    return y



TITLE = "What is OSHC?"
BODY = (
    "OSHC stands for Overseas Student Health Cover. It is health insurance "
    "that international students must have while studying in Australia. "
    "It helps pay for visits to the doctor, some hospital care and "
    "emergency ambulance services."
)

SAMPLE_QUESTION = "Why do international students need OSHC?"
SAMPLE_OPTIONS = [
    "A. It is a student visa requirement",
    "B. It is only needed for sports",
    "C. It is optional",
    "D. It replaces a student ID",
]

# ---------------------------------------------------------------
# FUNCTION: render()
# PURPOSE: Main entry point, called by app.py's router when
#          st.session_state.page == "oshc".
# ---------------------------------------------------------------


def render():
    # items = content.load_oshc()
    # total = LENGTH of items
    # index = st.session_state.question_index
    #
    # IF index >= total:
    #     CALL ui.results_screen(st.session_state.score, total, "Medibank OSHC Awareness")
    #     RETURN
    #
    # current_item = items[index]
    #
    # CALL ui.progress_bar(index + 1, total)
    # CALL show_section(current_item)
    # CALL comprehension_check(current_item)
    #
    # CALL ui.return_button()
    pass


# ---------------------------------------------------------------
# FUNCTION: show_section(item)
# PURPOSE: Display a short, plain-language explainer of one OSHC
#          concept (e.g. "What is OSHC?", "How do I make a claim?").
# ---------------------------------------------------------------
def show_section(item):
    # DISPLAY item["section_text"]
    # (keep language simple - target users have varied English
    #  proficiency, per report section 3.2.2)
    pass


# ---------------------------------------------------------------
# FUNCTION: comprehension_check(item)
# PURPOSE: Ask a short question testing understanding of the
#          section just shown, using st.radio (report 3.3.3).
# ---------------------------------------------------------------
def comprehension_check(item):
    # DISPLAY item["question"]
    # choice = st.radio(options = item["options"])
    #
    # IF student submits an answer:
    #     CALL check_answer(choice, item)
    #     CALL ui.next_button()
    pass


# ---------------------------------------------------------------
# FUNCTION: check_answer(choice, item)
# PURPOSE: Compare selection to item["correct_option"], update
#          session score (FR03, FR06), show feedback via ui module.
# ---------------------------------------------------------------
def check_answer(choice, item):
    # is_correct = (choice == item["correct_option"])
    # IF is_correct:
    #     INCREMENT st.session_state.score
    # APPEND is_correct to st.session_state.answered
    # CALL ui.feedback_box(is_correct, item["explanation"])
    # RETURN is_correct
    pass


# ── Style test screen ─────────────────────────────────────────────────────────
def draw_test_screen(font_name, body_size, selected_option):
    w, h = screen.get_size()
    margin = max(24, w // 25)
    content_w = w - 2 * margin

    heading_font = get_font(HEADING_FONT_PATH, int(body_size * 1.8))
    body_font = get_font(font_name, body_size)
    small_font = get_font(font_name, SMALL_FONT_SIZE)

    screen.fill(DARK)

    # Header bar
    header_h = heading_font.get_linesize() + 40
    pygame.draw.rect(screen, MEDI_BLUE, (0, 0, w, header_h))
    draw_text(TITLE, heading_font, WHITE, margin, 20)

    # Body text + tip box
    y = header_h + 24
    y = draw_paragraph(BODY, body_font, WHITE, margin, y, content_w)

    # Question + options
    draw_text(SAMPLE_QUESTION, get_font(font_name, body_size, bold=True), YELLOW, margin, y)
    y += body_font.get_linesize() + 14

    mouse = pygame.mouse.get_pos()
    option_rects = []
    opt_h = body_font.get_linesize() + 20
    for i, text in enumerate(SAMPLE_OPTIONS):
        r = pygame.Rect(margin, y, min(content_w, 620), opt_h)
        hover = r.collidepoint(mouse)
        selected = (i == selected_option)
        fill = MEDI_BLUE if selected else WHITE
        pygame.draw.rect(screen, fill, r, border_radius=10)
        pygame.draw.rect(screen, MEDI_BLUE if hover or selected else GREY, r, 2, border_radius=10)
        draw_text(text, body_font, WHITE if selected else BLACK, r.x + 16, r.y + 10)
        option_rects.append(r)
        y += opt_h + 10

    # ... rest of the function (buttons, swatches, footer) stays as before
    return option_rects
 
 
# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    global screen
    clock = pygame.time.Clock()
    font_index = 0
    body_size = BODY_FONT_SIZE
    selected_option = None
    running = True
 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            elif event.type == pygame.VIDEORESIZE:
                # Enforce a minimum window size
                new_w = max(MIN_WIDTH, event.w)
                new_h = max(MIN_HEIGHT, event.h)
                screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    body_size = min(48, body_size + 1)
                elif event.key == pygame.K_DOWN:
                    body_size = max(10, body_size - 1)
                elif event.key == pygame.K_f:
                    font_index = (font_index + 1) % len(FONT_CHOICES)
                elif event.key == pygame.K_r:
                    font_index, body_size = 0, BODY_FONT_SIZE
                elif event.key == pygame.K_LEFTBRACKET:
                    screen = pygame.display.set_mode(
                        (max(MIN_WIDTH, screen.get_width() - 50), screen.get_height()), pygame.RESIZABLE)
                elif event.key == pygame.K_RIGHTBRACKET:
                    screen = pygame.display.set_mode(
                        (screen.get_width() + 50, screen.get_height()), pygame.RESIZABLE)
 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, r in enumerate(option_rects if "option_rects" in locals() else []):
                    if r.collidepoint(event.pos):
                        selected_option = i
 
        option_rects = draw_test_screen(FONT_CHOICES[font_index], body_size, selected_option)
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()
 
