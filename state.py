import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_ACCENT, COLOR_DANGER
from localization import LANGUAGES, TEXT, get_text

class GameState:
    def __init__(self, language="ru"):
        self.state = 'MENU'
        self.intro_alpha = 255
        self.menu_alpha = 255
        self.card_fade_alpha = 255

        self.language = language
        self.intro_texts = get_text(language, "intro")
        self.current_intro_index = 0
        self.current_char_index = 0
        self.displayed_text = ""
        self.text_timer = 0
        self.text_speed = 4
        self.text_fast = False
        
        self.result_phase = None
        self.result_timer = 0
        self.pending_effects = None
        self.result_full_string = ""
        self.result_chunks = []
        
        self.game_over_alpha = 0
        self.is_defeat = False
        
        self.stats = {
            "faith": {"val": 50, "color": (210, 175, 70)},
            "army": {"val": 50, "color": (195, 65, 65)},
            "habitability": {"val": 50, "color": (50, 180, 110)},
            "political": {"val": 50, "color": (130, 95, 195)},
            "order": {"val": 50, "color": (210, 125, 50)}
        }
        
        self.reality_stability = 65
        
        self.resources = {"matter": 150, "energy": 100}
        
        self.faith_zero_counter = 0
        self.revolution_active = False
        self.revolution_timer = 0
        self.turns_counter = 1
        
        self.save_slots = [None] * 6
        self.auto_save = None
        
        self.card_effects = [
            {
                "left_effects": {"faith": -5, "matter": 0, "hab": 0, "order": 0},
                "right_effects": {"faith": 0, "matter": -15, "hab": 5, "order": 0},
                "critical": False
            },
            {
                "left_effects": {"reality": 5, "energy": -10, "order": 0},
                "right_effects": {"reality": -5, "order": 5, "faith": -5},
                "critical": False
            }
        ]
        
        self.revolution_effects = {
            "left_effects": {"faith": -100, "matter": 0, "hab": 0, "order": -100},
            "right_effects": {"matter": -100, "energy": -30, "army": 15, "order": 10},
            "critical": True
        }

        self.final_revolution_effects = {
            "left_effects": {"faith": -100, "order": -100},
            "right_effects": {"faith": -100, "order": -100},
            "critical": True
        }
        
        self.current_card_index = 0
        self.set_language(language)
        self.card_data = self.cards_pool[self.current_card_index]
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 160, 520, 340)
        self.card_drag_offset_x = 0
        self.is_dragging = False
        self.card_current_x = self.card_rect.x
        
        self.background_art = self.load_background_art()

    def set_language(self, language):
        if language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        self.language = language
        self.intro_texts = get_text(language, "intro")
        localized = TEXT[language]
        if len(localized["cards"]) != len(self.card_effects):
            raise ValueError(f"Card translations are incomplete for language: {language}")
        self.cards_pool = [
            {**card_text, **effects}
            for card_text, effects in zip(localized["cards"], self.card_effects)
        ]
        self.revolution_card = {**localized["revolution"], **self.revolution_effects}
        self.final_revolution_card = {
            **localized["final_revolution"],
            **self.final_revolution_effects,
        }
        self.card_data = self.cards_pool[self.current_card_index]

    def load_background_art(self):
        for ext in [".png", ".jpg", ".jpeg"]:
            filename = f"art1{ext}"
            if os.path.exists(filename):
                try:
                    img = pygame.image.load(filename).convert()
                    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                except Exception:
                    pass
        return None

    def trigger_choice(self, direction):
        if self.revolution_active and self.revolution_timer <= 0:
            card = self.final_revolution_card
            self.is_defeat = True
        elif self.revolution_active:
            card = self.revolution_card
        else:
            card = self.cards_pool[self.current_card_index]
            
        if direction == "LEFT":
            self.displayed_text = ""
            self.pending_effects = card["left_effects"]
            self.result_text_full = card["left_result"]
            if self.revolution_active:
                self.is_defeat = True
        else:
            self.displayed_text = ""
            self.pending_effects = card["right_effects"]
            self.result_text_full = card["right_result"]
            if self.revolution_active and self.revolution_timer <= 0:
                self.is_defeat = True
            
        name_map = get_text(self.language, "effect_names")
        
        self.result_chunks = [(self.result_text_full, COLOR_TEXT)]
        
        delta_parts = []
        for key, val in self.pending_effects.items():
            if val != 0:
                sign = "+" if val > 0 else ""
                name = name_map.get(key, key)
                delta_parts.append((f"{name}: {sign}{val}", val > 0))
                
        if delta_parts:
            self.result_chunks.append(("\n", COLOR_TEXT))
            for idx, (text_str, is_pos) in enumerate(delta_parts):
                col = COLOR_ACCENT if is_pos else COLOR_DANGER
                self.result_chunks.append((text_str + ("   " if idx < len(delta_parts) - 1 else ""), col))

        self.result_full_string = "".join([chunk[0] for chunk in self.result_chunks])

        self.state = 'RESULT_WAIT'
        self.result_timer = 0
        self.result_phase = 'DOTS'
        self.current_char_index = 0

    def apply_pending_effects(self):
        effects = self.pending_effects
        if "faith" in effects:
            self.stats["faith"]["val"] = max(0, min(100, self.stats["faith"]["val"] + effects["faith"]))
        if "hab" in effects:
            self.stats["habitability"]["val"] = max(0, min(100, self.stats["habitability"]["val"] + effects["hab"]))
        if "order" in effects:
            self.stats["order"]["val"] = max(0, min(100, self.stats["order"]["val"] + effects["order"]))
        if "army" in effects:
            self.stats["army"]["val"] = max(0, min(100, self.stats["army"]["val"] + effects["army"]))
        if "reality" in effects:
            self.reality_stability = max(0, min(100, self.reality_stability + effects["reality"]))
        if "matter" in effects:
            self.resources["matter"] = max(0, self.resources["matter"] + effects["matter"])
        if "energy" in effects:
            self.resources["energy"] = max(0, self.resources["energy"] + effects["energy"])
            
        if self.is_defeat:
            self.state = 'GAME_OVER'
            return
            
        self.turns_counter += 1
        if self.turns_counter % 5 == 0:
            self.auto_save = {
                "stats": {k: v["val"] for k, v in self.stats.items()},
                "resources": self.resources.copy(),
                "reality": self.reality_stability,
                "card_idx": self.current_card_index
            }
            
        if self.revolution_active:
            if self.revolution_timer <= 0:
                self.is_defeat = True
                self.state = 'GAME_OVER'
                return
            else:
                self.revolution_active = False
                self.revolution_timer = 9
                self.faith_zero_counter = 0
        else:
            if self.stats["faith"]["val"] == 0:
                self.faith_zero_counter += 1
                if self.faith_zero_counter >= 3:
                    if self.revolution_timer <= 0:
                        self.revolution_active = True
            else:
                self.faith_zero_counter = 0
                if self.revolution_timer > 0:
                    self.revolution_timer -= 1
                    if self.revolution_timer == 0 and self.stats["faith"]["val"] == 0:
                        self.revolution_active = True
                    
            self.current_card_index = (self.current_card_index + 1) % len(self.cards_pool)
            self.card_data = self.cards_pool[self.current_card_index]
            
        self.card_current_x = self.card_rect.x
        self.card_fade_alpha = 0