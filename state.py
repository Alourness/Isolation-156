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
        self.game_over_timer = 0
        self.game_over_phase = None
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
        self.hab_low_counter = 0
        self.revolution_active = False
        self.final_revolution_active = False
        self.military_coup_active = False
        self.chaos_crisis_active = False
        self.political_paralysis_active = False
        self.reality_collapse_active = False
        self.revolution_timer = 0
        self.turns_counter = 1
        
        self.save_slots = [None] * 6
        self.auto_save = None
        
        self.card_effects = [
            {"left_effects": {"faith": -5}, "right_effects": {"matter": -25, "hab": 5}, "critical": False},
            {"left_effects": {"reality": 5, "energy": -10}, "right_effects": {"reality": -5, "order": 5, "faith": -5}, "critical": False},
            {"left_effects": {"faith": -8, "hab": -5}, "right_effects": {"energy": -20, "hab": 3}, "critical": False},
            {"left_effects": {"faith": -5, "order": 5, "matter": 15}, "right_effects": {"faith": 8, "energy": -25}, "critical": False},
            {"left_effects": {"hab": -6, "order": -8}, "right_effects": {"energy": -25, "hab": 2, "order": 3}, "critical": False},
            {"left_effects": {"hab": -7, "order": -5}, "right_effects": {"matter": -20, "hab": 6}, "critical": False},
            {"left_effects": {"army": 8, "political": -6}, "right_effects": {"army": -5, "political": 5}, "critical": False},
            {"left_effects": {"faith": -6}, "right_effects": {"energy": -25}, "critical": False},
            {"left_effects": {"order": 6, "faith": -7}, "right_effects": {"matter": -35, "energy": -20, "faith": 4}, "critical": True},
            {"left_effects": {"order": -6}, "right_effects": {"matter": -25}, "critical": False},
            {"left_effects": {"political": -5, "faith": -5}, "right_effects": {"energy": -25}, "critical": False},
            {"left_effects": {"hab": -5, "order": -5}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"order": 7, "faith": -8}, "right_effects": {"army": -6, "faith": 3}, "critical": False},
            {"left_effects": {"reality": -6, "faith": -5}, "right_effects": {"energy": -30, "reality": 3}, "critical": True},
            {"left_effects": {"hab": -6, "faith": -4}, "right_effects": {"matter": -20}, "critical": False},
            {"left_effects": {"army": 6, "order": -6}, "right_effects": {"energy": -25, "matter": -25}, "critical": False},
            {"left_effects": {"faith": -6, "political": -5}, "right_effects": {"energy": -20, "matter": -20}, "critical": False},
            {"left_effects": {"army": -5, "political": 5}, "right_effects": {"political": -8, "army": 7}, "critical": False},
            {"left_effects": {"matter": -20}, "right_effects": {"energy": -35, "reality": 4}, "critical": True},
            {"left_effects": {"hab": -5, "faith": -5}, "right_effects": {"matter": -35}, "critical": False},
            {"left_effects": {"faith": -8, "order": 6}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"order": -6}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"matter": 30, "faith": -10}, "right_effects": {"faith": 5}, "critical": False},
            {"left_effects": {"hab": -7, "matter": 30}, "right_effects": {"faith": 3}, "critical": False},
            {"left_effects": {"reality": 4, "political": -5}, "right_effects": {"political": 5, "reality": -4}, "critical": False},
            {"left_effects": {"energy": -25, "matter": -30, "faith": 8}, "right_effects": {"faith": -8, "order": -5}, "critical": True},
            {"left_effects": {"matter": 25, "political": -5}, "right_effects": {"faith": 6, "order": 5}, "critical": False},
            {"left_effects": {"army": 6, "energy": -20}, "right_effects": {"order": -7}, "critical": False},
            {"left_effects": {"energy": -25}, "right_effects": {"hab": -6, "faith": -5}, "critical": False},
            {"left_effects": {"hab": 6, "faith": -7}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"order": 5, "faith": -6}, "right_effects": {"matter": -25, "energy": -15}, "critical": False},
            {"left_effects": {"energy": -30, "reality": 5}, "right_effects": {"reality": -7}, "critical": True},
            {"left_effects": {"matter": -30, "hab": 6}, "right_effects": {}, "critical": False},
            {"left_effects": {"matter": -30}, "right_effects": {"hab": -7, "faith": -5}, "critical": False},
            {"left_effects": {"political": -7, "order": 6}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"matter": -20, "order": -5}, "right_effects": {"matter": -35, "energy": -15}, "critical": False},
            {"left_effects": {"order": 6, "faith": -6}, "right_effects": {"energy": -20}, "critical": False},
            {"left_effects": {"matter": -35}, "right_effects": {"army": -8}, "critical": False},
            {"left_effects": {"reality": -5, "hab": -5}, "right_effects": {"energy": -25}, "critical": False},
            {"left_effects": {"matter": -30, "energy": -20}, "right_effects": {"energy": -35}, "critical": True},
            {"left_effects": {"army": 8, "political": -8}, "right_effects": {"political": 6, "army": -6}, "critical": False},
            {"left_effects": {"matter": 35, "political": -7}, "right_effects": {"faith": 5, "energy": -20}, "critical": False},
            {"left_effects": {"political": -10, "order": -6}, "right_effects": {"matter": -35, "political": 7}, "critical": True},
            {"left_effects": {"order": 8, "political": -8}, "right_effects": {"army": 6, "order": -5}, "critical": True}
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

        self.military_coup_card = {
            "title": "ВОЕННЫЙ ПЕРЕВОРОТ",
            "desc": "Армия под руководством генералов посчитала вашу власть избыточно мягкой. Колонны бронетехники занимают правительственные здания!",
            "left_preview": "КАПИТУЛИРОВАТЬ: Передать власть хунте.",
            "right_preview": "ПОПЫТАТЬСЯ ОТБИТЬСЯ: Рискнуть остатками сил.",
            "left_result": "Генералы зачитали приговор о расформировании вашего правительства. Вас отвели в сырой подвал под гул марширующих сапог. Выстрел в затылок поставил точку в эпохе.",
            "right_result": "Верные вам личные телохранители сложили оружие первыми. Вас выволокли на центральную площадь под камеры трибунала и повесили на ржавой балке.",
            "left_effects": {"army": -100, "political": -100},
            "right_effects": {"army": -100, "political": -100},
            "critical": True
        }

        self.chaos_crisis_card = {
            "title": "КАТАСТРОФА ВЫЖИВАНИЯ: МАССОВЫЙ МОР",
            "desc": "Из-за критически низкой жизнедеятельности в течение недели люди начали массово умирать. Бунтующие толпы сносят заграждения. Требуются колоссальные затраты (40 Энергии и 50 Материи) для восстановления порядка!",
            "left_preview": "БРОСИТЬ НА ПРОИЗВОЛ: Полный распад сектора.",
            "right_preview": "ЭКСТРЕННАЯ МОБИЛИЗАЦИЯ: Потратить 40 Энергии и 50 Материи.",
            "left_result": "Мертвые тела заполнили все жилые ярусы. В тишине умирающего бункера больше некому отдавать приказы — автоматика отключила последние системы жизнеобеспечения.",
            "right_result": "Мобилизация захлебнулась в крови. Вы остались один в пустом, промерзшем бункере, где из стен сочится ядовитая удушливая гарь.",
            "left_effects": {"hab": -100, "order": -100},
            "right_effects": {"energy": -40, "matter": -50, "hab": 25, "order": 20},
            "critical": True
        }

        self.political_paralysis_card = {
            "title": "ПАРАЛИЧ ВЛАСТИ И КРИЗИС СОВЕТА",
            "desc": "Политическая стабильность упала ниже 10%! Аппарат управления парализован, чиновники разбежались, а законы не работают.",
            "left_preview": "УЙТИ В ОТСТАВКУ: Сложить полномочия (Поражение).",
            "right_preview": "ЖЕСТКАЯ МИЛИТАРИЗАЦИЯ: Поднять Армию до +30 для разгона оппозиции.",
            "left_result": "Вы сложили полномочия, но толпа на выходе из зала заседаний не пощадила экс-правителя. Вас затоптали на бетонном полу коридора.",
            "right_result": "Танки открыли огонь прямой наводкой по зданию парламента. Обрушившийся потолок погреб под тоннами бетона и вас, и ваших министров.",
            "left_effects": {"political": -100},
            "right_effects": {"army": 30, "political": 40, "order": 20},
            "critical": True
        }

        self.reality_collapse_card = {
            "title": "КРИСТАЛЛИЗАЦИЯ РЕАЛЬНОСТИ ДО ЧЕРНОГО СТЕКЛА",
            "desc": "Стабильность реальности рухнула ниже 10%! Законы физики окончательно рассыпаются. Стены бункера превращаются в холодное зеркальное стекло, поглощающее людей.",
            "left_preview": "ПРИНЯТЬ КОНЕЦ: Позволить черному стеклу поглотить сектор.",
            "right_preview": "ПРЕДОТВРАТИТЬ КАТАСТРОФУ: Отдать 60 Энергии, 70 Материи и пожертвовать людьми (-30 Веры).",
            "left_result": "Реальность треснула окончательно. Ваши руки и лицо медленно покрылись зеркальной коркой холодного черного стекла. Вы застыли навечно в виде безумной статуи.",
            "right_result": "Пространственная матрица схлопнулась, превратив весь сектор в гладкий монолит из черного глянца. Никаких следов человека — лишь абсолютная тишина.",
            "left_effects": {"reality": -100},
            "right_effects": {"energy": -60, "matter": -70, "faith": -30, "reality": 40},
            "critical": True
        }
        
        self.current_card_index = 0
        self.set_language(language)
        self.card_data = self.cards_pool[self.current_card_index]
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 160, 520, 340)
        self.card_drag_offset_x = 0
        self.is_dragging = False
        self.card_current_x = self.card_rect.x
        self.card_anim_y = self.card_rect.y
        self.card_animation_active = False
        self.card_text_char_index = 0
        self.card_text_timer = 0
        
        # Кэш фонов для разных типов событий
        self.background_arts = {
            "art1": self.load_art("art1"),
            "art2": self.load_art("art2"), # Бунты, социальные проблемы, эпидемии
            "art3": self.load_art("art3"), # Военные, хунта, гарнизон
            "art4": self.load_art("art4")  # Экономика, ресурсы, ремонт, дефицит
        }
        self.background_art = self.get_background_art_for_current_card()

    def load_art(self, base_name):
        for ext in [".png", ".jpg", ".jpeg"]:
            filename = f"{base_name}{ext}"
            if os.path.exists(filename):
                try:
                    img = pygame.image.load(filename).convert()
                    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                except Exception:
                    pass
        return None

    def get_background_art_for_current_card(self):
        card = self.get_active_card()
        title = card.get("title", "").upper()
        desc = card.get("desc", "").upper()

        # 1. Военные события / хунта / армия -> art3
        military_keywords = ["АРМИЯ", "ГАРНИЗОН", "ВОЕННЫЙ", "ПЕРЕВОРОТ", "ОФИЦЕР", "КОМАНДИР", "ПАТРУЛ", "БОЙЦОВ"]
        if any(kw in title or kw in desc for kw in military_keywords) or self.military_coup_active:
            if self.background_arts["art3"]:
                return self.background_arts["art3"]

        # 2. Бунты / народные волнения / социальные проблемы / мор -> art2
        riot_keywords = ["БУНТ", "ВОССТАНИЕ", "МАССОВЫЙ МОР", "АПАТИИ", "ЗАКОВАН", "ЗАБАСТОВКА", "КУЛЬТ", "ФАНАТИЗМ", "БЕЖЕНЦЕВ"]
        if any(kw in title or kw in desc for kw in riot_keywords) or self.revolution_active or self.chaos_crisis_active or self.political_paralysis_active:
            if self.background_arts["art2"]:
                return self.background_arts["art2"]

        # 3. Экономика / ресурсы / ремонт / фильтры / энергия / материя -> art4
        economy_keywords = ["ФИЛЬТР", "МАТЕРИИ", "ЭНЕРГИЯ", "РЕМОНТ", "СКЛАД", "ЛИФТ", "ВОДНЫХ", "ТУРБИН", "УТИЛИЗАЦИЯ", "РУДНИК", "ДЕФИЦИТ", "ОПРЕСНЕНИЯ"]
        if any(kw in title or kw in desc for kw in economy_keywords):
            if self.background_arts["art4"]:
                return self.background_arts["art4"]

        # По умолчанию (или для аномалий/реальности) возвращаем art1
        return self.background_arts["art1"] or self.background_arts["art2"] or self.background_arts["art3"] or self.background_arts["art4"]

    def start_card_appearance(self):
        self.state = 'PLAYING'
        self.card_current_x = self.card_rect.x
        self.card_anim_y = SCREEN_HEIGHT
        self.card_animation_active = True
        self.card_text_char_index = 0
        self.card_text_timer = 0
        self.card_fade_alpha = 0
        self.result_phase = None
        self.result_full_string = ""
        self.result_chunks = []
        self.pending_effects = None
        self.displayed_text = ""
        self.text_fast = False
        self.is_dragging = False
        # Обновляем фон при появлении новой карточки
        self.background_art = self.get_background_art_for_current_card()

    def start_game_over(self):
        self.state = 'GAME_OVER'
        self.game_over_alpha = 0
        self.game_over_timer = 0
        self.game_over_phase = 'FADE_IN'
        self.is_defeat = True

    def restore_autosave(self):
        data = self.auto_save
        if data is None:
            for stat in self.stats.values():
                stat["val"] = 50
            self.resources = {"matter": 150, "energy": 100}
            self.reality_stability = 65
            self.current_card_index = 0
            self.turns_counter = 1
            self.faith_zero_counter = 0
            self.hab_low_counter = 0
            self.revolution_active = False
            self.final_revolution_active = False
            self.military_coup_active = False
            self.chaos_crisis_active = False
            self.political_paralysis_active = False
            self.reality_collapse_active = False
            self.revolution_timer = 0
        else:
            for key, stat in self.stats.items():
                stat["val"] = data["stats"].get(key, 50)
            self.resources = data["resources"].copy()
            self.reality_stability = data.get("reality", 65)
            self.current_card_index = data.get("card_idx", 0) % len(self.cards_pool)
            self.turns_counter = data.get("turns", 1)
            self.faith_zero_counter = data.get("faith_zero_counter", 0)
            self.hab_low_counter = data.get("hab_low_counter", 0)
            self.revolution_active = data.get("revolution_active", False)
            self.final_revolution_active = data.get("final_revolution_active", False)
            self.military_coup_active = data.get("military_coup_active", False)
            self.chaos_crisis_active = data.get("chaos_crisis_active", False)
            self.political_paralysis_active = data.get("political_paralysis_active", False)
            self.reality_collapse_active = data.get("reality_collapse_active", False)
            self.revolution_timer = data.get("revolution_timer", 0)

        self.card_data = self.cards_pool[self.current_card_index]
        self.is_defeat = False
        self.result_phase = None
        self.pending_effects = None
        self.result_full_string = ""
        self.result_chunks = []
        self.displayed_text = ""
        self.text_fast = False
        self.game_over_timer = 0
        self.game_over_phase = 'FADE_OUT'
        self.game_over_alpha = 255
        self.start_card_appearance()

    def set_language(self, language):
        if language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        self.language = language
        self.intro_texts = get_text(language, "intro")
        localized = TEXT[language]
        if len(localized["cards"]) != len(self.card_effects):
            raise ValueError(f"Card translations ({len(localized['cards'])}) mismatch card effects ({len(self.card_effects)}) for language: {language}")
        self.cards_pool = [
            {**card_text, **effects}
            for card_text, effects in zip(localized["cards"], self.card_effects)
        ]
        self.revolution_card = {**localized["revolution"], **self.revolution_effects}
        self.final_revolution_card = {
            **localized["final_revolution"],
            **self.final_revolution_effects,
        }
        self.military_coup_card = {**localized["military_coup"], **self.military_coup_card}
        self.chaos_crisis_card = {**localized["chaos_crisis"], **self.chaos_crisis_card}
        self.political_paralysis_card = {**localized["political_paralysis"], **self.political_paralysis_card}
        self.reality_collapse_card = {**localized["reality_collapse"], **self.reality_collapse_card}
        
        self.card_data = self.cards_pool[self.current_card_index]

    def trigger_choice(self, direction):
        card = self.get_active_card()
        
        is_ending_choice = False
        if (self.revolution_active and self.final_revolution_active) or self.military_coup_active or self.chaos_crisis_active or self.political_paralysis_active or self.reality_collapse_active:
            is_ending_choice = True
            self.is_defeat = True

        if direction == "LEFT":
            self.displayed_text = ""
            raw_effects = card["left_effects"].copy()
            self.result_text_full = card["left_result"]
        else:
            self.displayed_text = ""
            raw_effects = card["right_effects"].copy()
            self.result_text_full = card["right_result"]

        filtered_effects = {}
        bankruptcy_penalty = False

        if not is_ending_choice:
            for key, val in raw_effects.items():
                if val < 0 and key in ["matter", "energy"]:
                    needed = -val
                    available = self.resources[key]
                    if available < needed:
                        filtered_effects[key] = -available
                        bankruptcy_penalty = True
                        continue
                
                if val < 0:
                    if key in self.stats and self.stats[key]["val"] == 0:
                        continue
                    if key == "reality" and self.reality_stability == 0:
                        continue
                filtered_effects[key] = val

            if bankruptcy_penalty:
                filtered_effects["order"] = filtered_effects.get("order", 0) - 15
                filtered_effects["faith"] = filtered_effects.get("faith", 0) - 15
                self.result_text_full += "\n[АВАРИЯ ИЗ-ЗА ДЕФИЦИТА РЕСУРСОВ: Запасы полностью выгорели, сектор охвачен паникой!]"
        else:
            filtered_effects = {}

        self.pending_effects = filtered_effects
            
        name_map = get_text(self.language, "effect_names")
        
        self.result_chunks = [(self.result_text_full, COLOR_TEXT)]
        
        if not is_ending_choice:
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
            else:
                self.result_chunks.append(("\n", COLOR_TEXT))
                nothing_text = get_text(self.language, "nothing_happened")
                self.result_chunks.append((nothing_text, (150, 150, 150)))
        else:
            self.result_chunks.append(("\n\n[ ВАШЕ ПРАВЛЕНИЕ СТЕРТО ИЗ ИСТОРИИ БУНКЕРА ]", COLOR_DANGER))

        self.result_full_string = "".join([chunk[0] for chunk in self.result_chunks])

        self.state = 'RESULT_WAIT'
        self.result_timer = 0
        self.result_phase = 'DOTS'
        self.current_char_index = 0
        return True

    def get_active_card(self):
        if self.reality_collapse_active:
            return self.reality_collapse_card
        if self.political_paralysis_active:
            return self.political_paralysis_card
        if self.chaos_crisis_active:
            return self.chaos_crisis_card
        if self.military_coup_active:
            return self.military_coup_card
        if self.revolution_active and self.final_revolution_active:
            return self.final_revolution_card
        if self.revolution_active:
            return self.revolution_card
        return self.cards_pool[self.current_card_index]

    def can_afford_choice(self, direction):
        return True

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
        if "political" in effects:
            self.stats["political"]["val"] = max(0, min(100, self.stats["political"]["val"] + effects["political"]))
        if "reality" in effects:
            self.reality_stability = max(0, min(100, self.reality_stability + effects["reality"]))
        if "matter" in effects:
            self.resources["matter"] = max(0, self.resources["matter"] + effects["matter"])
        if "energy" in effects:
            self.resources["energy"] = max(0, self.resources["energy"] + effects["energy"])
            
        if self.is_defeat:
            self.start_game_over()
            return
            
        self.turns_counter += 1

        order_val = self.stats["order"]["val"]
        faith_val = self.stats["faith"]["val"]
        army_val = self.stats["army"]["val"]
        hab_val = self.stats["habitability"]["val"]
        reality_val = self.reality_stability

        base_energy_gain = 25
        base_matter_gain = 30

        resource_penalty = 0.15 if order_val < 10 else 1.0
        resource_bonus = 1.6 if order_val > 80 else 1.0

        total_multiplier = resource_penalty * resource_bonus

        if self.turns_counter % 8 == 0:
            self.resources["energy"] += int(base_energy_gain * total_multiplier)
        if self.turns_counter % 10 == 0:
            self.resources["matter"] += int(base_matter_gain * total_multiplier)

        if self.turns_counter % 3 == 0:
            if order_val < 10:
                self.stats["faith"]["val"] = max(0, self.stats["faith"]["val"] - 10)
            
            if army_val < 15:
                self.stats["order"]["val"] = max(0, self.stats["order"]["val"] - 10)

            if faith_val > 90:
                self.stats["order"]["val"] = min(100, self.stats["order"]["val"] + 7)
            elif faith_val > 75:
                self.stats["order"]["val"] = min(100, self.stats["order"]["val"] + 2)

            if hab_val > 85:
                self.stats["faith"]["val"] = min(100, self.stats["faith"]["val"] + 3)
                self.stats["order"]["val"] = min(100, self.stats["order"]["val"] + 2)

        if self.reality_collapse_active:
            self.reality_collapse_active = False
        elif self.political_paralysis_active:
            self.political_paralysis_active = False
        elif self.chaos_crisis_active:
            self.chaos_crisis_active = False
            self.hab_low_counter = 0
        elif self.military_coup_active:
            self.military_coup_active = False
        elif self.revolution_active:
            self.revolution_active = False
            self.final_revolution_active = False
            self.revolution_timer = 9
            self.faith_zero_counter = 0
        else:
            if reality_val < 10:
                self.reality_collapse_active = True
            
            political_val = self.stats["political"]["val"]
            if political_val < 10:
                self.political_paralysis_active = True

            if 0 <= hab_val <= 10:
                self.hab_low_counter += 1
                if self.hab_low_counter >= 7:
                    self.chaos_crisis_active = True
            else:
                self.hab_low_counter = 0

            if army_val > 90:
                coup_chance = 15 + (army_val - 90) * 3
                import random
                if random.randint(1, 100) <= coup_chance:
                    self.military_coup_active = True

            if not self.chaos_crisis_active and not self.military_coup_active and not self.political_paralysis_active and not self.reality_collapse_active:
                if self.revolution_timer > 0:
                    self.faith_zero_counter = 0
                    if self.stats["faith"]["val"] < 10:
                        self.revolution_timer -= 1
                        if self.revolution_timer == 0:
                            self.revolution_active = True
                            self.final_revolution_active = True
                    else:
                        self.revolution_timer = 9
                else:
                    if self.stats["faith"]["val"] < 10:
                        self.faith_zero_counter += 1
                        if self.faith_zero_counter >= 3:
                            self.revolution_active = True
                            self.final_revolution_active = False
                    else:
                        self.faith_zero_counter = 0

                if not self.revolution_active:
                    if reality_val < 30:
                        import random
                        anomaly_indices = [1, 13, 18, 24, 31, 38]
                        if random.randint(1, 100) <= 60:
                            self.current_card_index = random.choice(anomaly_indices) % len(self.cards_pool)
                        else:
                            self.current_card_index = (self.current_card_index + 1) % len(self.cards_pool)
                    else:
                        self.current_card_index = (self.current_card_index + 1) % len(self.cards_pool)

        self.card_data = self.get_active_card()

        if self.turns_counter % 5 == 0:
            self.auto_save = {
                "stats": {k: v["val"] for k, v in self.stats.items()},
                "resources": self.resources.copy(),
                "reality": self.reality_stability,
                "card_idx": self.current_card_index,
                "turns": self.turns_counter,
                "faith_zero_counter": self.faith_zero_counter,
                "hab_low_counter": self.hab_low_counter,
                "revolution_active": self.revolution_active,
                "final_revolution_active": self.final_revolution_active,
                "military_coup_active": self.military_coup_active,
                "chaos_crisis_active": self.chaos_crisis_active,
                "political_paralysis_active": self.political_paralysis_active,
                "reality_collapse_active": self.reality_collapse_active,
                "revolution_timer": self.revolution_timer,
            }
            
        self.start_card_appearance()