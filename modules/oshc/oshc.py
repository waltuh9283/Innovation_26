"""VishGuard - Cybersecurity Awareness Simulator."""
#CLONE OF PHISHGUARD - CHANGE ACCORDINGLY
import pygame, sys, json, random, os  
pygame.init()  
# ── Window & colours ──────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1000, 700  # fixed window size for the game display
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create the main game window
pygame.display.set_caption("PhishGuard")  # set the window title shown by the OS
WHITE  = (255, 255, 255)  # white used for text and button borders
BLACK  = (15,  15,  15)  # dark background color for the game screens
BLUE   = (70,  120, 255)  # blue for positive or action buttons
GREEN  = (50,  200, 90)   # green for safe actions and success feedback
RED    = (220, 60,  60)   # red for danger, errors, and phishing cues
GRAY   = (180, 180, 180)  # gray for secondary text and borders
YELLOW = (255, 210, 50)   # yellow for warnings and educational tips
PANEL  = (35,  35,  55)   # panel background color behind email details
DARK   = (50,  50,  70)   # darker tone used to dim completed rows

# ── Config ────────────────────────────────────────────────────────────────────
FPS, LINE_HEIGHT     = 60, 30  # frame rate cap and vertical line height for wrapped text
GLITCH_DURATION = 700                                    # ms the red glitch flashes after a wrong answer
GLITCH_COUNT    = 18                                     # number of random rects drawn per glitch frame

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_X, PANEL_W    = 80, 840                            # email content panel: left edge and width
SEP_X1,  SEP_X2     = 150, 850                           # feedback separator line start/end x
ROW_X, ROW_W, ROW_H = 100, 800, 55                       # inbox row: left edge, width, height
ROW_START_Y         = 120                                # y of the first inbox row
ROW_HEIGHT          = 70                                 # vertical gap between rows
ROW_TEXT_OFFSET     = 15                                 # text y-offset inside each row
ROW_TEXT_X          = 120                                # x for email text inside each row
ROW_STATUS_X        = 820                                # x for Done/Unread label inside each row
INST_START_Y, INST_LINE_GAP          = 210, 50           # y of first instruction line, gap between lines
HUD_SCORE_X, HUD_LIVES_X, HUD_Y      = 20, 850, 20      # HUD score x, lives x, shared y
EMAIL_LABEL_X                         = 110              # x for FROM/SUBJECT/LINK labels
EMAIL_SENDER_X, EMAIL_SUBJECT_X       = 240, 265         # x for sender and subject values
EMAIL_LINK_X, EMAIL_BODY_MAX_W        = 220, 760         # x for link value, body wrap width
EMAIL_PANEL_Y, EMAIL_PANEL_H          = 70, 490          # email panel top y and height
EMAIL_FROM_Y, EMAIL_SUBJECT_Y         = 100, 150         # y for FROM and SUBJECT rows
EMAIL_BODY_Y, EMAIL_LINK_Y            = 230, 390         # y for body and LINK rows
FB_HEADING_X, FB_BULLET_X, FB_REASON_X = 150, 155, 175  # x positions on feedback screen
FB_REASONS_START_Y                    = 255              # y of first reason bullet
FB_REASON_MAX_W, FB_REASON_GAP        = 650, 40          # reason wrap width and gap after each

btn_start    = pygame.Rect(400, 300, 200, 60)
btn_inst     = pygame.Rect(400, 390, 200, 60)
btn_back     = pygame.Rect(140,   20, 100, 40)
btn_continue = pygame.Rect(350, 590, 300, 55)
btn_play     = pygame.Rect(350, 540, 300, 60)
btn_menu     = pygame.Rect(350, 620, 300, 60)

ACTIONS = [  # buttons shown on the email view; each tuple includes hitbox, label, colour, and expected answer
    (pygame.Rect(100, 610, 190, 55), "Report Phishing", RED,   "phishing"),
    (pygame.Rect(700, 610, 190, 55), "Mark Safe",       GREEN, "legit"), ]
# ── Email data ────────────────────────────────────────────────────────────────
try:
    email_file_path = os.path.join(os.path.dirname(__file__), "emails.json")  # load data relative to this script location
    with open(email_file_path) as email_file:
        EMAILS = json.load(email_file)
except (FileNotFoundError, json.JSONDecodeError) as load_error:
    print(f"Could not load emails.json: {load_error}")
    sys.exit()

font  = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# ── Game state dict ───────────────────────────────────────────────────────────
game_state = {  # central state dict used to control screens, scoring, and email progress
    "state": "menu", "open_email": 0, "feedback": "",
    "feedback_colour": WHITE, "score": 0, "lives": 3,
    "correct": 0, "wrong": 0, "game_emails": [],
    "completed": [], "mistakes": [], "glitch_end": 0, "next_state": "",
}

def start_game():  # reset all progress and load a new shuffled inbox
    """Reset all per-session state and begin the inbox."""
    game_state.update(score=0, lives=3, correct=0, wrong=0,
                      game_emails=random.sample(EMAILS, len(EMAILS)),
                      completed=[], mistakes=[], state="inbox")

# ── Draw helpers ──────────────────────────────────────────────────────────────
def draw_text_center(text, colour, y):  # helper for centered text
    """Render text horizontally centred at the given y-coordinate."""
    rendered_surface = font.render(text, True, colour)
    screen.blit(rendered_surface, rendered_surface.get_rect(center=(WIDTH // 2, y)))

def draw_button(rect, text, colour):
    """Draw a filled, bordered button with centred label."""
    pygame.draw.rect(screen, colour, rect)  # draw the button background
    pygame.draw.rect(screen, WHITE,  rect, 2)            # 2px white border for definition
    rendered_surface = font.render(text, True, WHITE)  # render the button label text

    screen.blit(rendered_surface, rendered_surface.get_rect(center=rect.center))  # center the button label inside the hitbox

def draw_text(text, colour, x, y):
    """Blit text at an absolute position."""
    screen.blit(font.render(text, True, colour), (x, y))

def draw_wrapped(text, colour, x, y, max_w):
    """Word-wrap text within max_w pixels; return y of the last line."""
    current_line, current_y = "", y
    for word in text.split():
        candidate_line = current_line + word + " "  # try adding the next word to the current line
        if font.size(candidate_line)[0] < max_w:
            current_line = candidate_line
        else:
            screen.blit(font.render(current_line, True, colour), (x, current_y))
            current_y += LINE_HEIGHT
            current_line = word + " "  # start a new wrapped line with this word
    screen.blit(font.render(current_line, True, colour), (x, current_y))
    return current_y

def draw_panel(rect, radius=12):
    """Draw a rounded-rectangle panel with a GRAY border."""
    pygame.draw.rect(screen, PANEL, rect, border_radius=radius)
    pygame.draw.rect(screen, GRAY,  rect, 2, border_radius=radius)

def draw_hud():
    """Render score (top-left) and lives (top-right) consistently."""
    draw_text(f"Score: {game_state['score']}", WHITE, HUD_SCORE_X, HUD_Y)
    draw_text(f"Lives: {game_state['lives']}", WHITE, HUD_LIVES_X, HUD_Y)

# ── Screen draw functions ─────────────────────────────────────────────────────
def draw_menu():
    """Main menu with Start and Instructions buttons."""
    screen.fill(BLACK)
    draw_text_center("PHISHGUARD", WHITE, 120)
    draw_text_center("Cybersecurity Awareness Simulator", GRAY,   180)
    draw_text_center("Can you spot the phishing emails?",  YELLOW, 220)
    draw_button(btn_start, "Start Game",   BLUE)
    draw_button(btn_inst,  "Instructions", GREEN)

def draw_instructions():
    """How-to-play screen; press ESC to go back."""
    screen.fill(BLACK)
    draw_text_center("HOW TO PLAY", WHITE, 100)
    lines = [
        "You have an inbox of emails to review.",
        "Click an email to open and inspect it.",
        "Delete or Report Phishing if it looks suspicious.",
        "Open or Mark Safe if it looks legitimate.",
        "Wrong actions cost you a life.",
        "Lose all 3 lives and it is game over.",
    ]
    for index, line in enumerate(lines):
        draw_text_center(line, GRAY, INST_START_Y + index * INST_LINE_GAP)
    draw_text_center("Press ESC to return.", WHITE, 625)

def draw_inbox():
    """Inbox listing all emails with Done/Unread status."""
    screen.fill(BLACK)  # clear the screen before drawing inbox items
    draw_text_center("INBOX", WHITE, 50)  # screen header for the inbox
    draw_hud()  # draw score and lives at the top corners
    for index, email in enumerate(game_state["game_emails"]):  # loop over each email to draw its row
        row = pygame.Rect(ROW_X, ROW_START_Y + index * ROW_HEIGHT, ROW_W, ROW_H)  # calculate the row hitbox
        draw_panel(row, radius=6)  # draw each inbox row panel before placing text
        if index in game_state["completed"]:  # if this email is already reviewed
            pygame.draw.rect(screen, DARK, row, border_radius=6)  # dim reviewed emails to show they are already handled
        draw_text(f"{index+1}.  {email['sender']} - {email['subject']}",
                  WHITE, ROW_TEXT_X, ROW_START_Y + index * ROW_HEIGHT + ROW_TEXT_OFFSET)  # email preview text for the inbox row
        draw_text("Done" if index in game_state["completed"] else "Unread",
                  GRAY, ROW_STATUS_X, ROW_START_Y + index * ROW_HEIGHT + ROW_TEXT_OFFSET)
    draw_text_center(
        f"{len(game_state['game_emails']) - len(game_state['completed'])} email(s) left to action",  # message summarizing how many emails remain
        GRAY, 640)  # summary count at bottom of inbox

def draw_email():
    """Full email view with sender, subject, body, link, and action buttons."""
    screen.fill(BLACK)
    email = game_state["game_emails"][game_state["open_email"]]
    draw_button(btn_back, "Back", DARK)
    draw_hud()
    draw_panel(pygame.Rect(PANEL_X, EMAIL_PANEL_Y, PANEL_W, EMAIL_PANEL_H))
    draw_text("FROM:",    WHITE, EMAIL_LABEL_X, EMAIL_FROM_Y);    draw_text(email["sender"],  GRAY, EMAIL_SENDER_X,  EMAIL_FROM_Y)
    draw_text("SUBJECT:", WHITE, EMAIL_LABEL_X, EMAIL_SUBJECT_Y); draw_text(email["subject"], GRAY, EMAIL_SUBJECT_X, EMAIL_SUBJECT_Y)
    draw_wrapped(email["message"], WHITE, EMAIL_LABEL_X, EMAIL_BODY_Y, EMAIL_BODY_MAX_W)
    draw_text("LINK:",    WHITE, EMAIL_LABEL_X, EMAIL_LINK_Y);    draw_text(email["link"], RED, EMAIL_LINK_X, EMAIL_LINK_Y)
    for rect, label, colour, _ in ACTIONS:
        draw_button(rect, label, colour)

def draw_feedback():  # draw the feedback screen after the player chooses an action
    """Outcome screen with explanation, reasons, and optional glitch effect."""
    screen.fill(BLACK)
    email = game_state["game_emails"][game_state["open_email"]]
    draw_text_center(game_state["feedback"], game_state["feedback_colour"], 70)
    classification_label = "PHISHING EMAIL" if email["answer"] == "phishing" else "LEGITIMATE EMAIL"
    draw_text_center(classification_label, RED if email["answer"] == "phishing" else GREEN, 120)
    draw_text_center(email["tip"], YELLOW, 165)
    pygame.draw.line(screen, GRAY, (SEP_X1, 195), (SEP_X2, 195), 1)
    draw_text("Why this is phishing:" if email["answer"] == "phishing"
              else "Why this is safe:", WHITE, FB_HEADING_X, 215)  # section header depends on the email type
    bullet_colour = RED if email["answer"] == "phishing" else GREEN  # colour for each bullet based on email type
    reason_y = FB_REASONS_START_Y  # starting y position for the reason list
    for reason in email["reasons"]:  # draw each explanation bullet
        draw_text("-", bullet_colour, FB_BULLET_X, reason_y)  # bullet marker for each reason
        reason_y = draw_wrapped(reason, GRAY, FB_REASON_X, reason_y, FB_REASON_MAX_W) + FB_REASON_GAP  # wrap each reason to fit the feedback panel
    if pygame.time.get_ticks() < game_state["glitch_end"]:  # only render glitch while timer is active
        for _ in range(GLITCH_COUNT):  # draw multiple random rectangles
            pygame.draw.rect(screen, RED, (
                random.randint(0, WIDTH),  random.randint(0, HEIGHT),
                random.randint(50, 200),   random.randint(8, 35)))  # flash random rectangles for failure feedback
    draw_button(btn_continue, "Continue", BLUE)  # button to move from feedback to next state

def draw_results():
    """End-of-game results: score, accuracy, and common mistake summary."""
    screen.fill(BLACK)
    total_answered = game_state["correct"] + game_state["wrong"]
    accuracy = round(game_state["correct"] / total_answered * 100) if total_answered else 0
    draw_text_center("INBOX CLEARED",                        WHITE,  100)
    draw_text_center(f"Final Score: {game_state['score']}",  WHITE,  180)
    draw_text_center(f"Correct: {game_state['correct']}",   GREEN,  230)
    draw_text_center(f"Wrong: {game_state['wrong']}",        RED,    275)
    draw_text_center(f"Accuracy: {accuracy}%",               YELLOW, 320)
    pygame.draw.line(screen, GRAY, (SEP_X1, 355), (SEP_X2, 355), 1)
    draw_text_center("Most common mistake:", GRAY,  385)
    draw_text_center(get_mistake_summary(),   WHITE, 425)
    draw_button(btn_play, "Play Again", BLUE)
    draw_button(btn_menu, "Main Menu",  GRAY)

def draw_gameover():
    """Game-over screen shown when all lives are lost."""
    screen.fill(BLACK)
    draw_text_center("SYSTEM COMPROMISED",                     RED,    150)
    draw_text_center("You fell for too many phishing attacks.", WHITE,  270)
    draw_text_center(f"Final Score: {game_state['score']}",    YELLOW, 340)
    draw_text_center("Hackers gained access to your system.",  GRAY,   410)
    draw_button(btn_play, "Play Again", GREEN)
    draw_button(btn_menu, "Main Menu",  BLUE)

# ── Game logic ────────────────────────────────────────────────────────────────
def check_answer(player_choice):  # validate the current action against the email's correct answer
    """Validate the player's action and update score, lives, and state."""
    email = game_state["game_emails"][game_state["open_email"]]  # retrieve the active email
    if player_choice == email["answer"]:  # compare player choice to the correct answer
        game_state["feedback"], game_state["feedback_colour"] = "CORRECT", GREEN  # correct response state
        game_state["score"]   += 10  # reward the player for a correct answer
        game_state["correct"] += 1  # increment correct answer counter
    else:  # wrong answer branch
        game_state["feedback"], game_state["feedback_colour"] = "WRONG", RED  # wrong response state
        game_state["score"]   -= 5  # deduct points for an incorrect choice
        game_state["lives"]   -= 1  # lose a life when wrong
        game_state["wrong"]   += 1  # increment wrong answer counter
        game_state["mistakes"].append(email["answer"])   # record the correct answer for post-game analysis
        game_state["glitch_end"] = pygame.time.get_ticks() + GLITCH_DURATION  # start the glitch effect timer
    game_state["completed"].append(game_state["open_email"])  # mark this email as reviewed
    game_state["next_state"] = ("gameover" if game_state["lives"] <= 0
                                else "results" if len(game_state["completed"]) >= len(game_state["game_emails"])
                                else "inbox")  # choose the next screen after feedback is shown
    game_state["state"] = "feedback"

def get_mistake_summary():  # summarize the player's most common error type
    """Return a summary of the player's most common mistake type."""  # analyze the logged mistakes to provide personalised feedback on error patterns
    if not game_state["mistakes"]:  # if the player made no mistakes
        return "No mistakes! Perfect round!"  # return a congratulatory message instead of an error summary
    phishing_misses  = game_state["mistakes"].count("phishing")  # emails wrongly marked as safe
    legit_misses     = game_state["mistakes"].count("legit")      # emails wrongly flagged as phishing
    if phishing_misses > legit_misses:  return "You missed phishing emails with fake domains."  # focus on phishing cues if most errors were safe misses
    if legit_misses > phishing_misses:  return "You marked legitimate emails as phishing."  # focus on not over-flagging legit emails
    return "You struggled equally with both types."  # equal problems with both error categories

# ── Main loop ─────────────────────────────────────────────────────────────────
DRAW_FUNCTIONS = {
    "menu": draw_menu, "instructions": draw_instructions,
    "inbox": draw_inbox, "email": draw_email,
    "feedback": draw_feedback, "results": draw_results,
    "gameover": draw_gameover, }

if __name__ == "__main__":  # only run the game loop when this script is executed directly
    while True:  # main game loop that runs until the window closes
        clock.tick(FPS)  # cap the frame rate to keep timing consistent
        for event in pygame.event.get():  # process every pending pygame event
            if event.type == pygame.QUIT:  # if the user closes the window
                pygame.quit(); sys.exit()  # close the window and terminate the program
            if event.type == pygame.KEYDOWN:  # handle keyboard input events
                if game_state["state"] == "instructions" and event.key == pygame.K_ESCAPE:  # ESC returns to the menu from instructions
                    game_state["state"] = "menu"         # ESC always returns to menu from instructions
            if event.type == pygame.MOUSEBUTTONDOWN:  # handle mouse click events
                current_screen = game_state["state"]  # snapshot the current screen before handling clicks
                if current_screen == "menu":  # clicks on the main menu
                    if btn_start.collidepoint(event.pos): start_game() # start a new game session with reset state
                    elif btn_inst.collidepoint(event.pos): game_state["state"] = "instructions" # switch to instructions screen
                elif current_screen == "inbox":  # clicks on the inbox list
                    for index in range(len(game_state["game_emails"])):  # check each email row hitbox
                        row = pygame.Rect(ROW_X, ROW_START_Y + index * ROW_HEIGHT, ROW_W, ROW_H) # calculate the hitbox for each email row based on its index
                        if row.collidepoint(event.pos) and index not in game_state["completed"]:  # only open unopened emails
                            game_state["open_email"] = index; game_state["state"] = "email"  # switch to the email detail view
                elif current_screen == "email":  # handle clicks on the open email screen
                    if btn_back.collidepoint(event.pos): game_state["state"] = "inbox"  # go back to inbox without answering
                    for rect, _, _, verdict in ACTIONS:  # unpack button definitions, ignoring unused label and colour here
                        if rect.collidepoint(event.pos): check_answer(verdict)  # validate the chosen verdict
                elif current_screen == "feedback":  # clicks on the feedback screen
                    if btn_continue.collidepoint(event.pos): game_state["state"] = game_state["next_state"]  # move to the queued next screen after feedback
                elif current_screen in ("results", "gameover"):  # handle end-screen buttons
                    if btn_play.collidepoint(event.pos): start_game()  # restart the game from the beginning
                    elif btn_menu.collidepoint(event.pos): game_state["state"] = "menu"  # go back to main menu

        DRAW_FUNCTIONS[game_state["state"]]()
        pygame.display.flip()
