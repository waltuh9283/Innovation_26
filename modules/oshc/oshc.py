"""VishGuard - Cybersecurity Awareness Simulator."""
#CLONE OF PHISHGUARD - CHANGE ACCORDINGLY
from tkinter import font

# ---- IMPORTS  ----
#import streamlit as st
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
font_title = pygame.font.Font(os.path.join(FONTS_DIR, 'blocky.ttf'), 16)

# ── Draw helpers ──────────────────────────────────────────────────────────────
def draw_text(text, font, colour, x, y):
    """Draw text with its top-left corner at (x, y). Returns the rect."""
    surf = font.render(text, True, colour)
    rect = surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)
    return rect

def draw_text_center(text, font, colour, y):
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