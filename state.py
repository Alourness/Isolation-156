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
            ),
            (
                "Вы просыпаетесь за своим рабочим столом...\n"
                "Лампа мерцает в такт уставшему гулу генераторов.\n"
                "Секретарь кладет на стол первые донесения. Время принимать решения."
            )
        ]
        self.current_intro_index = 0
        self.current_char_index = 0
        self.displayed_text = ""
        self.text_timer = 0
        self.text_speed = 3
        
        self.result_phase = None
        self.result_timer = 0
        self.pending_effects = None
        self.result_deltas = []
        
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
        
        self.cards_pool = [
            {
                "title": "УГРОЗА ВОЗДУШНОГО ФИЛЬТРА",
                "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья в жилых блоках возрастет.",
                "left_preview": "ОТКАЗАТЬ: Сэкономить Материю, уронить Веру людей",
                "right_preview": "ВЫДЕЛИТЬ ДЕТАЛИ: Потратить Материю, поднять Жизнепригодность",
                "left_result": "Вы отказали техникам. Густой углекислотный туман медленно заполняет нижние уровни.",
                "right_result": "Запасные детали доставлены в цех. Турбины взревели новыми оборотами, очищая воздух.",
                "left_effects": {"faith": -15, "matter": 25, "hab": 0},
                "right_effects": {"faith": 0, "matter": -30, "hab": 15}
            },
            {
                "title": "ПРОРЫВ АНОМАЛИИ В СЕКТОРЕ С",
                "desc": "Датчики фиксируют искажение пространственной сетки за перегородкой жилого блока. Физические законы там начинают деформироваться.",
                "left_preview": "УЦЕПИТЬСЯ ЗА СТАБИЛЬНОСТЬ: Рискнуть энергией полей",
                "right_preview": "ЗАБЕТОНИРОВАТЬ ОТСЕК: Замуровать аномалию вместе с частью людей",
                "left_result": "Защитные контуры удержали разлом ценой чудовищного скачка энергопотребления.",
                "right_result": "Автоматические бетононасосы залили отсек за считанные минуты. Крики стихли.",
                "left_effects": {"reality": 10, "energy": -25, "order": 0},
                "right_effects": {"reality": -15, "order": 15, "faith": -10}
            }
        ]
        
        self.current_card_index = 0
        self.card_data = self.cards_pool[self.current_card_index]
        
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

    def trigger_choice(self, direction):
        card = self.cards_pool[self.current_card_index]
        if direction == "LEFT":
            self.displayed_text = ""
            self.pending_effects = card["left_effects"]
            self.result_text_full = card["left_result"]
        else:
            self.displayed_text = ""
            self.pending_effects = card["right_effects"]
            self.result_text_full = card["right_result"]
            
        self.result_deltas = []
        name_map = {
            "faith": "Вера людей",
            "hab": "Жизнепригодность",
            "order": "Порядок",
            "reality": "Стаб. реальности",
            "matter": "Материя",
            "energy": "Энергия"
        }
        for key, val in self.pending_effects.items():
            if val != 0:
                sign = "+" if val > 0 else ""
                name = name_map.get(key, key)
                self.result_deltas.append((f"{name}: {sign}{val}", val > 0))

        self.state = 'RESULT_WAIT'
        self.result_timer = 0
        self.result_phase = 'DOTS'
        self.current_char_index = 0

    def apply_pending_effects(self):
        effects = self.pending_effects
        if "faith" in effects:
            self.stats["Вера людей"]["val"] = max(0, min(100, self.stats["Вера людей"]["val"] + effects["faith"]))
        if "hab" in effects:
            self.stats["Жизнепригодность"]["val"] = max(0, min(100, self.stats["Жизнепригодность"]["val"] + effects["hab"]))
        if "order" in effects:
            self.stats["Порядок"]["val"] = max(0, min(100, self.stats["Порядок"]["val"] + effects["order"]))
        if "reality" in effects:
            self.reality_stability = max(0, min(100, self.reality_stability + effects["reality"]))
        if "matter" in effects:
            self.resources["Материя"] += effects["matter"]
        if "energy" in effects:
            self.resources["Энергия"] += effects["energy"]
            
        self.current_card_index = (self.current_card_index + 1) % len(self.cards_pool)
        self.card_data = self.cards_pool[self.current_card_index]
        self.card_current_x = self.card_rect.x