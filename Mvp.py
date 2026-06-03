import pygame
import sys
import random

WIDTH, HEIGHT = 950, 720
FPS = 60
COLORS = {
    "bg": (12, 12, 15),
    "card": (28, 28, 38),
    "accent": (212, 175, 55),
    "pitch": (20, 45, 20),
    "white": (240, 240, 240),
    "success": (46, 204, 113),
    "error": (231, 76, 60),
    "gray": (100, 100, 100),
    "btn_hover": (45, 65, 120),
    "btn_normal": (25, 35, 65)
}

# --- EXPANDED 10-PLAYER DATABASE FOR GUESSER ---
PLAYER_POOL = [
    {"name": "Lionel Messi", "hints": ["3 Clubs", "Short", "1x World Cup"], "img": "messi.jpg"},
    {"name": "Michael Olise", "hints": ["Aura", "Test The Pitch", "Bayern Munich"], "img": "olise.jpg"},
    {"name": "Antony", "hints": ["Brazil", "Spin Move", "Real Betis"], "img": "antony.jpg"},
    {"name": "Bernardo Silva", "hints": ["Portuguese", "#20", "Incredible Ball Control"], "img": "silva.jpg"},
    {"name": "Lamine Yamal", "hints": ["Euros 2024", "Barcelona Record Breaker", "Wonderkid"], "img": "yamal.jpg"},
    {"name": "Marcus Rashford", "hints": ["Manchester United #10", "FreeKicks", "Clinical English Forward"], "img": "rashford.jpg"},
    {"name": "Yeremy Pino", "hints": ["Crystal Palace", "Spanish International", "Europa League Winner"], "img": "pino.jpg"},
    {"name": "Crysencio Summerville", "hints": ["West Ham New Signing", "Championship Player of the Season 23/24", "Ex-Leeds Star"], "img": "summerville.jpg"},
    {"name": "Lautaro Martinez", "hints": ["Inter Milan Captain", "Argentine 'El Toro'", "Serie A Top Scorer"], "img": "martinez.jpg"},
    {"name": "Cristiano Ronaldo", "hints": ["Portugal All-Time Scorer", "Al-Nassr Forward", "5 Ballon d'Ors"], "img": "ronaldo.jpg"}
]

# --- 10 RANDOMIZED LINEUPS FOR MISSING XI ---
LINEUP_POOL = [
    {
        "team_name": "Real Madrid 2017 (UCL Final)",
        "target_name": "Casemiro",
        "players": [
            {"name": "Navas",    "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Marcelo",  "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Ramos",    "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Varane",   "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Carvajal", "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Casemiro", "pos": (475, 330), "label": "CDM", "missing": True},
            {"name": "Kroos",    "pos": (350, 280), "label": "CM",  "missing": False},
            {"name": "Modric",   "pos": (600, 280), "label": "CM",  "missing": False},
            {"name": "Isco",     "pos": (475, 200), "label": "CAM", "missing": False},
            {"name": "Benzema",  "pos": (350, 130), "label": "ST",  "missing": False},
            {"name": "Ronaldo",  "pos": (600, 130), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "Barcelona 2011 (UCL Final)",
        "target_name": "Busquets",
        "players": [
            {"name": "Valdes",   "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Abidal",   "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Pique",    "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Mascherano","pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Alves",    "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Busquets", "pos": (475, 330), "label": "CDM", "missing": True},
            {"name": "Iniesta",  "pos": (350, 260), "label": "CM",  "missing": False},
            {"name": "Xavi",     "pos": (600, 260), "label": "CM",  "missing": False},
            {"name": "Pedro",    "pos": (250, 150), "label": "LW",  "missing": False},
            {"name": "Villa",    "pos": (700, 150), "label": "RW",  "missing": False},
            {"name": "Messi",    "pos": (475, 110), "label": "CF",  "missing": False}
        ]
    },
    {
        "team_name": "Arsenal 2003/04 (Invincibles)",
        "target_name": "Vieira",
        "players": [
            {"name": "Lehmann",  "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Cole",     "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Campbell", "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Toure",    "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Lauren",   "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Gilberto", "pos": (380, 310), "label": "CM",  "missing": False},
            {"name": "Vieira",   "pos": (570, 310), "label": "CM",  "missing": True},
            {"name": "Pires",    "pos": (230, 210), "label": "LM",  "missing": False},
            {"name": "Ljungberg","pos": (720, 210), "label": "RM",  "missing": False},
            {"name": "Bergkamp", "pos": (380, 120), "label": "CF",  "missing": False},
            {"name": "Henry",    "pos": (570, 120), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "Manchester United 1999 (Treble)",
        "target_name": "Beckham",
        "players": [
            {"name": "Schmeichel","pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Irwin",    "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Stam",     "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Johnsen",  "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "G. Neville","pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Giggs",    "pos": (230, 280), "label": "LM",  "missing": False},
            {"name": "Butt",     "pos": (380, 310), "label": "CM",  "missing": False},
            {"name": "Blomqvist","pos": (570, 310), "label": "CM",  "missing": False},
            {"name": "Beckham",  "pos": (720, 280), "label": "RM",  "missing": True},
            {"name": "Yorke",    "pos": (380, 130), "label": "ST",  "missing": False},
            {"name": "Cole",     "pos": (570, 130), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "AC Milan 2005 (Istanbul)",
        "target_name": "Kaká",
        "players": [
            {"name": "Dida",     "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Maldini",  "pos": (200, 420), "label": "LB",  "missing": False},
            {"name": "Nesta",    "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Jaap Stam","pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Cafu",     "pos": (750, 420), "label": "RB",  "missing": False},
            {"name": "Pirlo",    "pos": (475, 340), "label": "Regista", "missing": False},
            {"name": "Seedorf",  "pos": (320, 270), "label": "LM",  "missing": False},
            {"name": "Gattuso",  "pos": (630, 270), "label": "RM",  "missing": False},
            {"name": "Kaká",     "pos": (475, 200), "label": "CAM", "missing": True},
            {"name": "Crespo",   "pos": (350, 110), "label": "ST",  "missing": False},
            {"name": "Shevchenko","pos": (600, 110), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "Liverpool 2019 (UCL Winners)",
        "target_name": "Firmino",
        "players": [
            {"name": "Alisson",  "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Robertson","pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Van Dijk", "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Matip",    "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Alexander-A","pos": (750, 400), "label": "RB", "missing": False},
            {"name": "Fabinho",  "pos": (475, 320), "label": "DM",  "missing": False},
            {"name": "Henderson","pos": (350, 250), "label": "CM",  "missing": False},
            {"name": "Wijnaldum","pos": (600, 250), "label": "CM",  "missing": False},
            {"name": "Mané",     "pos": (250, 130), "label": "LW",  "missing": False},
            {"name": "Salah",    "pos": (700, 130), "label": "RW",  "missing": False},
            {"name": "Firmino",  "pos": (475, 120), "label": "CF",  "missing": True}
        ]
    },
    {
        "team_name": "Chelsea 2012 (UCL Final)",
        "target_name": "Drogba",
        "players": [
            {"name": "Cech",     "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Cole",     "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Luiz",     "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Cahill",   "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Bosingwa", "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Mikel",    "pos": (380, 310), "label": "DM",  "missing": False},
            {"name": "Lampard",  "pos": (570, 310), "label": "CM",  "missing": False},
            {"name": "Kalou",    "pos": (230, 210), "label": "LM",  "missing": False},
            {"name": "Mata",     "pos": (475, 200), "label": "CAM", "missing": False},
            {"name": "Bertrand", "pos": (720, 210), "label": "RM",  "missing": False},
            {"name": "Drogba",   "pos": (475, 110), "label": "ST",  "missing": True}
        ]
    },
    {
        "team_name": "Inter Milan 2010 (Treble)",
        "target_name": "Sneijder",
        "players": [
            {"name": "Julio Cesar","pos": (475, 520), "label": "GK", "missing": False},
            {"name": "Chivu",    "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Samuel",   "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Lucio",    "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Maicon",   "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Cambiasso","pos": (380, 310), "label": "DM",  "missing": False},
            {"name": "Zanetti",  "pos": (570, 310), "label": "DM",  "missing": False},
            {"name": "Eto'o",    "pos": (250, 200), "label": "LM",  "missing": False},
            {"name": "Sneijder", "pos": (475, 200), "label": "CAM", "missing": True},
            {"name": "Pandev",   "pos": (700, 200), "label": "RM",  "missing": False},
            {"name": "Milito",   "pos": (475, 110), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "Bayern Munich 2013 (Treble)",
        "target_name": "Robben",
        "players": [
            {"name": "Neuer",    "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Alaba",    "pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Dante",    "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Boateng",  "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Lahm",     "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Martinez", "pos": (380, 310), "label": "DM",  "missing": False},
            {"name": "Schweinsteiger","pos": (570, 310), "label": "DM", "missing": False},
            {"name": "Ribery",   "pos": (230, 200), "label": "LW",  "missing": False},
            {"name": "Müller",   "pos": (475, 200), "label": "CAM", "missing": False},
            {"name": "Robben",   "pos": (720, 200), "label": "RW",  "missing": True},
            {"name": "Mandzukic","pos": (475, 110), "label": "ST",  "missing": False}
        ]
    },
    {
        "team_name": "Spain 2010 (World Cup Final)",
        "target_name": "Iniesta",
        "players": [
            {"name": "Casillas", "pos": (475, 520), "label": "GK",  "missing": False},
            {"name": "Capdevila","pos": (200, 400), "label": "LB",  "missing": False},
            {"name": "Puyol",    "pos": (380, 450), "label": "CB",  "missing": False},
            {"name": "Pique",    "pos": (570, 450), "label": "CB",  "missing": False},
            {"name": "Ramos",    "pos": (750, 400), "label": "RB",  "missing": False},
            {"name": "Busquets", "pos": (350, 320), "label": "DM",  "missing": False},
            {"name": "Alonso",   "pos": (600, 320), "label": "DM",  "missing": False},
            {"name": "Iniesta",  "pos": (230, 210), "label": "LM",  "missing": True},
            {"name": "Xavi",     "pos": (475, 220), "label": "CAM", "missing": False},
            {"name": "Pedro",    "pos": (720, 210), "label": "RM",  "missing": False},
            {"name": "Villa",    "pos": (475, 110), "label": "ST",  "missing": False}
        ]
    }
]

# --- 10 EXPANDED RANDOM QUIZZES ---
QUIZ_POOL = [
    {"title": "TOP EXPENSIVE SIGNINGS", "data": ["Neymar", "Mbappe", "Coutinho", "Dembele", "Felix"]},
    {"title": "BALLON D'OR WINNERS", "data": ["Rodri", "Messi", "Benzema", "Modric", "Ronaldo"]},
    {"title": "PREMIER LEAGUE GOLDEN BOOT (LAST 5)", "data": ["Haaland", "Salah", "Son", "Kane", "Vardy"]},
    {"title": "WORLD CUP WINNING MANAGERS", "data": ["Scaloni", "Deschamps", "Löw", "Del Bosque", "Lippi"]},
    {"title": "CHALKING UP CHAMPIONS LEAGUE G.O.A.T. SCORERS", "data": ["Ronaldo", "Messi", "Lewandowski", "Benzema", "Raul"]},
    {"title": "ENGLISH PLAYERS OUTSIDE THE UK", "data": ["Kane", "Bellingham", "Sancho", "Tomori", "Loftus-Cheek"]},
    {"title": "INVINCIBLE ARSENAL SCORERS (TOP 5)", "data": ["Henry", "Pires", "Bergkamp", "Ljungberg", "Edu"]},
    {"title": "WORLD CUP ALL TIME TOP SCORERS", "data": ["Klose", "Ronaldo", "Müller", "Fontaine", "Pelé"]},
    {"title": "ACTIVE MANAGERS WITH UCL TROPHIES", "data": ["Ancelotti", "Guardiola", "Zidane", "Mourinho", "Tuchel"]},
    {"title": "MOST ENGLISH PREMIER LEAGUE TITLES", "data": ["Giggs", "Scholes", "Neville", "Irwin", "Keane"]}
]

# --- UI COMPONENTS ---
class MenuButton:
    def __init__(self, text, x, y, w, h, target_state):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.target_state = target_state
        self.is_hovered = False

    def draw(self, screen, font):
        color = COLORS["btn_hover"] if self.is_hovered else COLORS["btn_normal"]
        pygame.draw.rect(screen, (5, 5, 5), (self.rect.x+4, self.rect.y+4, self.rect.w, self.rect.h), border_radius=12)
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, COLORS["accent"], self.rect, 2, border_radius=12)
        txt = font.render(self.text, True, COLORS["white"])
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

# --- BASE GAME MODE ---
class GameMode:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.font_m = fonts['m']
        self.font_s = fonts['s']
        self.user_input = ""
        self.feedback = "Type and press Enter"
        self.feedback_color = COLORS["accent"]

    def check_name(self, user_in, correct_full):
        user_in = user_in.lower().strip()
        correct_full = correct_full.lower()
        last_name = correct_full.split()[-1]
        return user_in == correct_full or user_in == last_name

# --- PLAYER GUESSER ---
class PlayerGuesser(GameMode):
    def __init__(self, screen, fonts):
        super().__init__(screen, fonts)
        self.player_list = list(PLAYER_POOL)
        random.shuffle(self.player_list)
        
        self.current_idx = 0
        self.next_btn_rect = pygame.Rect(WIDTH//2 - 100, 530, 200, 50)
        self.setup_round()

    def setup_round(self):
        player = self.player_list[self.current_idx]
        self.name = player["name"]
        self.all_hints = player["hints"]
        self.img_filename = player["img"]
        
        self.attempts = 0
        self.max_attempts = 3
        self.game_over = False
        self.success = False
        self.user_input = ""
        self.feedback = f"Player {self.current_idx + 1} of {len(self.player_list)}"
        self.feedback_color = COLORS["accent"]
        
        try:
            raw_img = pygame.image.load(self.img_filename)
            self.player_img = pygame.transform.smoothscale(raw_img, (134, 174))
        except:
            self.player_img = None

    def draw(self):
        card_rect = pygame.Rect(WIDTH//2 - 70, 70, 140, 180)
        pygame.draw.rect(self.screen, COLORS["card"], card_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS["accent"], card_rect, 3, border_radius=15)
        
        if self.game_over:
            if self.player_img:
                self.screen.blit(self.player_img, (card_rect.x + 3, card_rect.y + 3))
            else:
                last_name_upper = self.name.split()[-1].upper()
                name_t = self.font_s.render(last_name_upper, True, COLORS["accent"])
                self.screen.blit(name_t, name_t.get_rect(center=(WIDTH//2, 160)))
        else:
            display_text = "???"
            main_txt = self.font_m.render(display_text, True, COLORS["accent"])
            self.screen.blit(main_txt, main_txt.get_rect(center=(WIDTH//2, 160)))

        for i in range(self.max_attempts):
            heart_x = WIDTH//2 - 40 + (i * 40)
            color = COLORS["error"] if i < (self.max_attempts - self.attempts) else COLORS["gray"]
            pygame.draw.circle(self.screen, color, (heart_x, 275), 10)

        visible_clues = min(self.attempts + 1, 3)
        for i in range(visible_clues):
            y_pos = 310 + (i * 65)
            h_rect = pygame.Rect(WIDTH//2 - 250, y_pos, 500, 50)
            pygame.draw.rect(self.screen, (40, 40, 60), h_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS["accent"], h_rect, 1, border_radius=10)
            clue_txt = self.font_m.render(self.all_hints[i], True, COLORS["white"])
            self.screen.blit(clue_txt, (h_rect.x + 20, h_rect.y + 12))

        if self.game_over:
            m_pos = pygame.mouse.get_pos()
            btn_col = COLORS["btn_hover"] if self.next_btn_rect.collidepoint(m_pos) else COLORS["btn_normal"]
            pygame.draw.rect(self.screen, btn_col, self.next_btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS["white"], self.next_btn_rect, 2, border_radius=10)
            
            label = "FINISH GAME" if self.current_idx == len(self.player_list) - 1 else "NEXT PLAYER"
            btn_t = self.font_s.render(label, True, COLORS["white"])
            self.screen.blit(btn_t, btn_t.get_rect(center=self.next_btn_rect.center))

    def handle_submit(self):
        if self.game_over: return
        if self.check_name(self.user_input, self.name):
            self.feedback = f"GOAL! It is indeed {self.name}!"; self.feedback_color = COLORS["success"]
            self.success = True; self.game_over = True
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.feedback = f"OUT OF LIVES! Answer: {self.name}"; self.feedback_color = COLORS["error"]
                self.game_over = True
            else:
                self.feedback = "WRONG! New clue revealed."; self.feedback_color = COLORS["error"]
        self.user_input = ""

    def handle_click(self, pos):
        if self.game_over and self.next_btn_rect.collidepoint(pos):
            if self.current_idx < len(self.player_list) - 1:
                self.current_idx += 1
                self.setup_round()
                return "KEEP_PLAYING"
            else:
                return "RETURN_TO_MENU"
        return None

# --- MISSING XI MODE ---
class MissingXI(GameMode):
    def __init__(self, screen, fonts):
        super().__init__(screen, fonts)
        self.lineup_list = [dict(team) for team in LINEUP_POOL]
        random.shuffle(self.lineup_list)
        
        self.current_idx = 0
        self.next_btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 165, 200, 45)
        self.setup_lineup()

    def setup_lineup(self):
        current_team = self.lineup_list[self.current_idx]
        self.team_name = current_team["team_name"]
        self.target_name = current_team["target_name"]
        
        self.players = [dict(p) for p in current_team["players"]]
        self.solved = False
        self.user_input = ""
        self.feedback = f"Lineup {self.current_idx + 1} of {len(self.lineup_list)}: Type missing player name"
        self.feedback_color = COLORS["accent"]

    def draw(self):
        pitch_rect = pygame.Rect(100, 80, WIDTH - 200, 440)
        pygame.draw.rect(self.screen, (20, 45, 20), pitch_rect)
        
        for i in range(11):
            if i % 2 == 0:
                stripe = pygame.Rect(100, 80 + (i * 40), WIDTH - 200, 40)
                pygame.draw.rect(self.screen, (25, 55, 25), stripe)

        pygame.draw.rect(self.screen, COLORS["white"], pitch_rect, 3)
        pygame.draw.line(self.screen, COLORS["white"], (100, 300), (WIDTH-100, 300), 2)
        pygame.draw.circle(self.screen, COLORS["white"], (WIDTH//2, 300), 60, 2)
        pygame.draw.rect(self.screen, COLORS["white"], (WIDTH//2-150, 420, 300, 100), 2)
        
        title = self.font_m.render(self.team_name, True, COLORS["accent"])
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        for p in self.players:
            x, y = p["pos"]
            if p["missing"] and not self.solved:
                pulse = abs((pygame.time.get_ticks() // 10) % 10 - 5)
                pygame.draw.circle(self.screen, COLORS["accent"], (x, y), 25 + pulse, 2)
                name_text = f"??? ({p['label']})"
                color = COLORS["accent"]
            else:
                pygame.draw.circle(self.screen, COLORS["white"], (x, y), 22)
                pygame.draw.circle(self.screen, (30, 30, 50), (x, y), 20)
                name_text = p["name"]
                color = COLORS["white"]

            txt = self.font_s.render(name_text, True, color)
            self.screen.blit(txt, (x - txt.get_width()//2, y + 28))

        if self.solved:
            m_pos = pygame.mouse.get_pos()
            btn_col = COLORS["btn_hover"] if self.next_btn_rect.collidepoint(m_pos) else COLORS["btn_normal"]
            pygame.draw.rect(self.screen, btn_col, self.next_btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS["white"], self.next_btn_rect, 2, border_radius=10)
            
            label = "FINISH GAME" if self.current_idx == len(self.lineup_list) - 1 else "NEXT LINEUP"
            btn_t = self.font_s.render(label, True, COLORS["white"])
            self.screen.blit(btn_t, btn_t.get_rect(center=self.next_btn_rect.center))

    def handle_submit(self):
        if self.solved: return
        if self.check_name(self.user_input, self.target_name):
            self.feedback = f"GOLAZO! {self.target_name} identified."; self.feedback_color = COLORS["success"]
            self.solved = True
            for p in self.players:
                if p["missing"]: p["missing"] = False
        else:
            self.feedback = "Offsides! Try again."; self.feedback_color = COLORS["error"]
        self.user_input = ""

    def handle_click(self, pos):
        if self.solved and self.next_btn_rect.collidepoint(pos):
            if self.current_idx < len(self.lineup_list) - 1:
                self.current_idx += 1
                self.setup_lineup()
                return "KEEP_PLAYING"
            else:
                return "RETURN_TO_MENU"
        return None

# --- RANDOM QUIZ MODE (UPGRADED WITH 3 HEALTH LIVES & 10 RANDOM ROUNDS) ---
class RandomQuiz(GameMode):
    def __init__(self, screen, fonts):
        super().__init__(screen, fonts)
        self.quiz_list = list(QUIZ_POOL)
        random.shuffle(self.quiz_list)
        
        self.current_idx = 0
        self.next_btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 180, 200, 45)
        self.setup_quiz()

    def setup_quiz(self):
        quiz = self.quiz_list[self.current_idx]
        self.title = quiz["title"]
        self.data = quiz["data"]
        
        self.found = []
        self.attempts = 0
        self.max_attempts = 3
        self.game_over = False
        self.user_input = ""
        self.feedback = f"Quiz {self.current_idx + 1} of {len(self.quiz_list)}: Find all items!"
        self.feedback_color = COLORS["accent"]

    def draw(self):
        # 1. Main Title Header Layout
        title_t = self.font_m.render(self.title, True, COLORS["accent"])
        self.screen.blit(title_t, (WIDTH//2 - title_t.get_width()//2, 80))
        
        # 2. Hearts UI Setup
        for i in range(self.max_attempts):
            heart_x = WIDTH//2 - 40 + (i * 40)
            color = COLORS["error"] if i < (self.max_attempts - self.attempts) else COLORS["gray"]
            pygame.draw.circle(self.screen, color, (heart_x, 130), 10)

        # 3. Dynamic Rows for Answers Display
        for i, name in enumerate(self.data):
            y_pos = 170 + (i * 55)
            row = pygame.Rect(WIDTH//2 - 250, y_pos, 500, 42)
            pygame.draw.rect(self.screen, COLORS["card"], row, border_radius=8)
            
            if name in self.found:
                display = name
                color = COLORS["success"]
            elif self.game_over:
                display = name
                color = COLORS["error"]
            else:
                display = "???"
                color = COLORS["gray"]
                
            t = self.font_m.render(f"{i+1}. {display}", True, color)
            self.screen.blit(t, (row.x + 20, row.y + 6))

        # 4. End State System Interaction Elements
        if self.game_over:
            m_pos = pygame.mouse.get_pos()
            btn_col = COLORS["btn_hover"] if self.next_btn_rect.collidepoint(m_pos) else COLORS["btn_normal"]
            pygame.draw.rect(self.screen, btn_col, self.next_btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS["white"], self.next_btn_rect, 2, border_radius=10)
            
            label = "FINISH GAME" if self.current_idx == len(self.quiz_list) - 1 else "NEXT QUIZ"
            btn_t = self.font_s.render(label, True, COLORS["white"])
            self.screen.blit(btn_t, btn_t.get_rect(center=self.next_btn_rect.center))

    def handle_submit(self):
        if self.game_over: return
        
        correct_guess = False
        for p in self.data:
            if self.check_name(self.user_input, p):
                if p not in self.found:
                    self.found.append(p)
                    self.feedback = f"CORRECT! Added {p}."; self.feedback_color = COLORS["success"]
                    correct_guess = True
                    if len(self.found) == len(self.data):
                        self.feedback = "PERFECT! You found them all!"; self.feedback_color = COLORS["success"]
                        self.game_over = True
                    break
                else:
                    self.feedback = "Already discovered!"; self.feedback_color = COLORS["accent"]
                    self.user_input = ""
                    return

        if not correct_guess:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.feedback = "OUT OF LIVES! Answers revealed below."; self.feedback_color = COLORS["error"]
                self.game_over = True
            else:
                self.feedback = "STRIKE! That is incorrect."; self.feedback_color = COLORS["error"]
                
        self.user_input = ""

    def handle_click(self, pos):
        if self.game_over and self.next_btn_rect.collidepoint(pos):
            if self.current_idx < len(self.quiz_list) - 1:
                self.current_idx += 1
                self.setup_quiz()
                return "KEEP_PLAYING"
            else:
                return "RETURN_TO_MENU"
        return None

# --- CORE GAME CORE MANAGER MANAGER ---
class FootballManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Andy's Ultimate Football Trivia Challenge")
        self.fonts = {
            'l': pygame.font.SysFont("Verdana", 42, bold=True),
            'm': pygame.font.SysFont("Verdana", 22),
            's': pygame.font.SysFont("Verdana", 18)
        }
        self.modes = {"PLAYER": PlayerGuesser, "LINEUP": MissingXI, "QUIZ": RandomQuiz}
        self.active_mode = None
        self.menu_buttons = [
            MenuButton("1. Guess the Player", WIDTH//2-225, 240, 450, 65, "PLAYER"),
            MenuButton("2. Missing XI", WIDTH//2-225, 330, 450, 65, "LINEUP"),
            MenuButton("3. Random Quizzes", WIDTH//2-225, 420, 450, 65, "QUIZ")
        ]
        self.state = "MENU"
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit(); sys.exit()
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONUP:
                        for btn in self.menu_buttons:
                            if btn.is_hovered: 
                                self.state = btn.target_state
                                self.active_mode = self.modes[self.state](self.screen, self.fonts)
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        action = self.active_mode.handle_click(event.pos)
                        if action == "RETURN_TO_MENU":
                            self.state = "MENU"

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: 
                            self.state = "MENU"
                        elif event.key == pygame.K_RETURN: 
                            self.active_mode.handle_submit()
                        elif event.key == pygame.K_BACKSPACE: 
                            self.active_mode.user_input = self.active_mode.user_input[:-1]
                        else:
                            if len(self.active_mode.user_input) < 28:
                                self.active_mode.user_input += event.unicode

            self.draw(mouse_pos)
            self.clock.tick(FPS)

    def draw(self, mouse_pos):
        self.screen.fill(COLORS["bg"])
        if self.state == "MENU":
            title = self.fonts['l'].render("FOOTBALL TRIVIA", True, COLORS["accent"])
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            for btn in self.menu_buttons:
                btn.update(mouse_pos)
                btn.draw(self.screen, self.fonts['m'])
        else:
            self.active_mode.draw()
            
            is_over = getattr(self.active_mode, 'game_over', False)
            is_solved = getattr(self.active_mode, 'solved', False)
            
            if not is_over and not is_solved:
                box = pygame.Rect(WIDTH//2-250, HEIGHT-100, 500, 50)
                pygame.draw.rect(self.screen, (20, 20, 20), box, border_radius=12)
                pygame.draw.rect(self.screen, COLORS["accent"], box, 2, border_radius=12)
                txt = self.fonts['m'].render(self.active_mode.user_input + "|", True, COLORS["white"])
                self.screen.blit(txt, (box.x+15, box.y+10))
            
            fb = self.fonts['s'].render(self.active_mode.feedback, True, self.active_mode.feedback_color)
            self.screen.blit(fb, (WIDTH//2 - fb.get_width()//2, HEIGHT-140))
            
        pygame.display.flip()

if __name__ == "__main__":
    FootballManager().run()