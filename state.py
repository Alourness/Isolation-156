import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_ACCENT, COLOR_DANGER

class GameState:
    def __init__(self):
        self.state = 'MENU'
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
        self.result_full_string = ""
        self.result_chunks = []
        
        self.game_over_alpha = 0
        self.is_defeat = False
        
        self.stats = {
            "Вера людей": {"val": 50, "color": (210, 175, 70)},
            "Сила армии": {"val": 50, "color": (195, 65, 65)},
            "Жизнепригодность": {"val": 50, "color": (50, 180, 110)},
            "Полит. стab.": {"val": 50, "color": (130, 95, 195)},
            "Порядок": {"val": 50, "color": (210, 125, 50)}
        }
        
        self.reality_stability = 65
        
        self.resources = {
            "Материя": 150,
            "Энергия": 100
        }
        
        self.faith_zero_counter = 0
        self.revolution_active = False
        self.revolution_timer = 0
        self.turns_counter = 0
        
        self.save_slots = [None] * 6
        self.auto_save = None
        
        self.cards_pool = [
            {
                "title": "УГРОЗА ВОЗДУШНОГО ФИЛЬТРА",
                "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья в жилых блоках возрастет.",
                "left_preview": "ОТКАЗАТЬ: Вероятно, упадет Вера людей; возможно, пошатнется Порядок.",
                "right_preview": "ВЫДЕЛИТЬ ДЕТАЛИ: Есть риск истощить Материю, но поднимется Жизнепригодность.",
                "left_result": "Вы отказали техникам ради экономии. Густой туман заполняет нижние уровни, вызывая глухой ропот.",
                "right_result": "Запасные детали доставлены в цех. Турбины взревели новыми оборотами, очищая воздух.",
                "left_effects": {"faith": -5, "matter": 0, "hab": 0, "order": 0},
                "right_effects": {"faith": 0, "matter": -15, "hab": 5, "order": 0}
            },
            {
                "title": "ПРОРЫВ АНОМАЛИИ В СЕКТОРЕ С",
                "desc": "Датчики фиксируют искажение пространственной сетки за перегородкой жилого блока. Законы физики деформируются.",
                "left_preview": "УЦЕПИТЬСЯ: Стабильность реальности может вырасти, но Энергия имеет вероятность упасть.",
                "right_preview": "ЗАБЕТОНИРОВАТЬ: Порядок может подняться, но Вера людей и Реальность могут пострадать.",
                "left_result": "Защитные контуры удержали разлом ценой скачка энергопотребления в сетях.",
                "right_result": "Автоматические бетононасосы залили отсек за считанные минуты. Крики затихли под монолитом.",
                "left_effects": {"reality": 5, "energy": -10, "order": 0},
                "right_effects": {"reality": -5, "order": 5, "faith": -5}
            }
        ]
        
        self.revolution_card = {
            "title": "ВОССТАНИЕ В НИЖНИХ УРОВНЯХ",
            "desc": "Народный гнев прорвал блокаду секторов! Толпы с арматурой идут штурмовать административный уровень. Требуется срочно бросить в бой армию и задействовать резервы казны!",
            "left_preview": "СДАТЬ ПОСТЫ: Полный коллапс власти и гибель сектора.",
            "right_preview": "ПОДАВИТЬ БУНТ: Потратить 100 Материи и 30 Энергии для жесткого подавления.",
            "left_result": "Толпы ворвались в кабинет. Ваше правление пало в огне всеобщего хаоса.",
            "right_result": "Армия жестоко подавила восстание на улицах. Порядок восстановлен, но сектор в крови.",
            "left_effects": {"faith": -100, "matter": 0, "hab": 0, "order": -100},
            "right_effects": {"matter": -100, "energy": -30, "army": 15, "order": 10}
        }
        
        self.current_card_index = 0
        self.card_data = self.cards_pool[self.current_card_index]
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 160, 520, 340)
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
        if self.revolution_active:
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
            
        name_map = {
            "faith": "Вера людей",
            "hab": "Жизнепригодность",
            "order": "Порядок",
            "reality": "Стаб. реальности",
            "matter": "Материя",
            "energy": "Энергия",
            "army": "Сила армии"
        }
        
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
            self.stats["Вера людей"]["val"] = max(0, min(100, self.stats["Вера людей"]["val"] + effects["faith"]))
        if "hab" in effects:
            self.stats["Жизнепригодность"]["val"] = max(0, min(100, self.stats["Жизнепригодность"]["val"] + effects["hab"]))
        if "order" in effects:
            self.stats["Порядок"]["val"] = max(0, min(100, self.stats["Порядок"]["val"] + effects["order"]))
        if "army" in effects:
            self.stats["Сила армии"]["val"] = max(0, min(100, self.stats["Сила армии"]["val"] + effects["army"]))
        if "reality" in effects:
            self.reality_stability = max(0, min(100, self.reality_stability + effects["reality"]))
        if "matter" in effects:
            self.resources["Материя"] = max(0, self.resources["Материя"] + effects["matter"])
        if "energy" in effects:
            self.resources["Энергия"] = max(0, self.resources["Энергия"] + effects["energy"])
            
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
            self.revolution_active = False
            self.revolution_timer = 9
            self.faith_zero_counter = 0
        else:
            if self.stats["Вера людей"]["val"] == 0:
                self.faith_zero_counter += 1
                if self.faith_zero_counter >= 3:
                    if self.revolution_timer <= 0:
                        self.revolution_active = True
            else:
                self.faith_zero_counter = 0
                if self.revolution_timer > 0:
                    self.revolution_timer -= 1
                    
            self.current_card_index = (self.current_card_index + 1) % len(self.cards_pool)
            self.card_data = self.cards_pool[self.current_card_index]
            
        self.card_current_x = self.card_rect.x