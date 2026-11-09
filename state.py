import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class GameState:
    def __init__(self):
        self.state = 'INTRO_1'
        self.intro_alpha = 255
        
        self.intro_texts = [
            (
                "Идет 156 год после Инсуффляции...\n"
                "Старый мир сжат, скомкан и сплавлен в бесконечный многослойный лабиринт.\n"
                "Нет неба и земли — только бетон, ржавые трубы и гул вентиляции."
            ),
            (
                "Ты — правитель изолированного сектора-укрытия.\n"
                "Твоя задача — балансировать на грани гибели, принимать тяжелые кризисные решения\n"
                "и вести людей через постоянную угрозу пространственных разломов, удушья и бунтов."
            )
        ]
        self.current_intro_index = 0
        self.current_char_index = 0
        self.displayed_text = ""
        self.text_timer = 0
        self.text_speed = 3
        
        self.stats = {
            "Вера людей": {"val": 50, "color": (210, 175, 70)},
            "Сила армии": {"val": 50, "color": (195, 65, 65)},
            "Жизнепригодность": {"val": 50, "color": (50, 180, 110)},
            "Политическая стab.": {"val": 50, "color": (130, 95, 195)},
            "Порядок": {"val": 50, "color": (210, 125, 50)}
        }
        
        self.reality_stability = 65
        
        self.resources = {
            "Материя": 100,
            "Энергия": 80
        }
        
        self.card_data = {
            "title": "УГРОЗА ВОЗДУШНОГО ФИЛЬТРА",
            "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья возрастет.",
            "left_preview": "ОТКАЗАТЬ: Сохранить Материю, уронить Веру людей",
            "right_preview": "ВЫДЕЛИТЬ ДЕТАЛИ: Потратить Материю, поднять Жизнепригодность"
        }
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 160, 460, 340)
        self.card_drag_offset_x = 0
        self.is_dragging = False
        self.card_current_x = self.card_rect.x
        
        self.background_art = self.load_background_art()

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

    def resolve_choice(self, direction):
        if direction == "LEFT":
            self.stats["Вера людей"]["val"] = max(0, self.stats["Вера людей"]["val"] - 15)
            self.resources["Материя"] += 25
        else:
            self.stats["Жизнепригодность"]["val"] = min(100, self.stats["Жизнепригодность"]["val"] + 15)
            self.resources["Материя"] = max(0, self.resources["Материя"] - 30)
        self.card_current_x = self.card_rect.x