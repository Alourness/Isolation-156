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
        self.revolution_timer = 0
        self.turns_counter = 1
        
        self.save_slots = [None] * 6
        self.auto_save = None
        
        # Расширенный пул из 44 карточек (включая новые интриги, армию, политику и международные отношения)
        self.card_effects = [
            # 1. Угроза воздушного фильтра
            {"left_effects": {"faith": -5}, "right_effects": {"matter": -15, "hab": 5}, "critical": False},
            # 2. Прорыв аномалии в секторе С (Реальность)
            {"left_effects": {"reality": 5, "energy": -10}, "right_effects": {"reality": -5, "order": 5, "faith": -5}, "critical": False},
            # 3. Утечка радиоактивных отходов
            {"left_effects": {"faith": -8, "hab": -5}, "right_effects": {"energy": -20, "hab": 3}, "critical": False},
            # 4. Контрабанда на черном рынке
            {"left_effects": {"faith": -5, "order": 5, "matter": 10}, "right_effects": {"faith": 8, "energy": -15}, "critical": False},
            # 5. Затмение искусственного солнца
            {"left_effects": {"hab": -6, "order": -8}, "right_effects": {"energy": -25, "hab": 2, "order": 3}, "critical": False},
            # 6. Бунт агрохимикатов
            {"left_effects": {"hab": -7, "order": -5}, "right_effects": {"matter": -15, "hab": 4}, "critical": False},
            # 7. Командирский раскол
            {"left_effects": {"army": 8, "political": -6}, "right_effects": {"army": -5, "political": 5}, "critical": False},
            # 8. Перегрузка квантового узла
            {"left_effects": {"faith": -6}, "right_effects": {"energy": -20}, "critical": False},
            # 9. Эпидемия апатии
            {"left_effects": {"order": 6, "faith": -7}, "right_effects": {"matter": -15, "energy": -10, "faith": 4}, "critical": True},
            # 10. Трещина в несущей стене
            {"left_effects": {"order": -6}, "right_effects": {"matter": -25}, "critical": False},
            # 11. Прорыв персональных данных
            {"left_effects": {"political": -5, "faith": -5}, "right_effects": {"energy": -20}, "critical": False},
            # 12. Сбой гравитационного контура
            {"left_effects": {"hab": -5, "order": -5}, "right_effects": {"energy": -15}, "critical": False},
            # 13. Дезертирство на границе
            {"left_effects": {"order": 7, "faith": -8}, "right_effects": {"army": -6, "faith": 3}, "critical": False},
            # 14. Аномальный туман (Реальность)
            {"left_effects": {"reality": -6, "faith": -5}, "right_effects": {"energy": -25, "reality": 3}, "critical": True},
            # 15. Истощение водных фильтров
            {"left_effects": {"hab": -6, "faith": -4}, "right_effects": {"matter": -20}, "critical": False},
            # 16. Бунт автоматических дронов
            {"left_effects": {"army": 6, "order": -6}, "right_effects": {"energy": -20, "matter": -10}, "critical": False},
            # 17. Приступ ихтиандровой лихорадки
            {"left_effects": {"faith": -6, "political": -5}, "right_effects": {"energy": -15, "matter": -15}, "critical": False},
            # 18. Конфликт силовиков и совета
            {"left_effects": {"army": -5, "political": 5}, "right_effects": {"political": -8, "army": 7}, "critical": False},
            # 19. Пространственная скатка (Реальность)
            {"left_effects": {"matter": -10}, "right_effects": {"energy": -30, "reality": 4}, "critical": True},
            # 20. Забастовка инженеров
            {"left_effects": {"hab": -5, "faith": -5}, "right_effects": {"matter": -25}, "critical": False},
            # 21. Вспышка религиозного фанатизма
            {"left_effects": {"faith": -8, "order": 6}, "right_effects": {"energy": -15}, "critical": False},
            # 22. Сбой вентиляционных шлюзов
            {"left_effects": {"order": -6}, "right_effects": {"energy": -15}, "critical": False},
            # 23. Хищническая утилизация
            {"left_effects": {"matter": 15, "faith": -10}, "right_effects": {"faith": 5}, "critical": False},
            # 24. Кризис снабжения рудника
            {"left_effects": {"hab": -7, "matter": 20}, "right_effects": {"faith": 3}, "critical": False},
            # 25. Раскол в научном совете (Реальность)
            {"left_effects": {"reality": 4, "political": -5}, "right_effects": {"political": 5, "reality": -4}, "critical": False},
            # 26. Экстренный призрение беженцев
            {"left_effects": {"energy": -20, "matter": -15, "faith": 8}, "right_effects": {"faith": -8, "order": -5}, "critical": True},
            # 27. Коррупция на распределении
            {"left_effects": {"matter": 15, "political": -5}, "right_effects": {"faith": 6, "order": 5}, "critical": False},
            # 28. Необходимость усиления патрулей
            {"left_effects": {"army": 6, "energy": -15}, "right_effects": {"order": -7}, "critical": False},
            # 29. Повреждение системы опреснения
            {"left_effects": {"energy": -20}, "right_effects": {"hab": -6, "faith": -5}, "critical": False},
            # 30. Искусственный интеллект сектора
            {"left_effects": {"hab": 6, "faith": -7}, "right_effects": {"energy": -15}, "critical": False},
            # 31. Бунт на гидропонике
            {"left_effects": {"order": 5, "faith": -6}, "right_effects": {"matter": -15, "energy": -10}, "critical": False},
            # 32. Пространственный эхо-сдвиг (Реальность)
            {"left_effects": {"energy": -25, "reality": 5}, "right_effects": {"reality": -7}, "critical": True},
            # 33. Секретный чертеж инженеров
            {"left_effects": {"matter": -20, "hab": 6}, "right_effects": {}, "critical": False},
            # 34. Дефицит медикаментов
            {"left_effects": {"matter": -20}, "right_effects": {"hab": -7, "faith": -5}, "critical": False},
            # 35. Политический тупик в совете
            {"left_effects": {"political": -7, "order": 6}, "right_effects": {"energy": -15}, "critical": False},
            # 36. Угроза обрушения лифтовой шахты
            {"left_effects": {"matter": -10, "order": -5}, "right_effects": {"matter": -20, "energy": -10}, "critical": False},
            # 37. Вспышка кибернетического культа
            {"left_effects": {"order": 6, "faith": -6}, "right_effects": {"energy": -15}, "critical": False},
            # 38. Кризис чести гарнизона
            {"left_effects": {"matter": -25}, "right_effects": {"army": -8}, "critical": False},
            # 39. Аномальный акустический гул (Реальность)
            {"left_effects": {"reality": -5, "hab": -5}, "right_effects": {"energy": -20}, "critical": False},
            # 40. Итоговая инспекция сектора
            {"left_effects": {"matter": -15, "energy": -15}, "right_effects": {"energy": -30}, "critical": True},
            # 41. Теневой ультиматум генералов
            {"left_effects": {"army": 8, "political": -8}, "right_effects": {"political": 6, "army": -6}, "critical": False},
            # 42. Тайный пакт с соседним бункером
            {"left_effects": {"matter": 25, "political": -7}, "right_effects": {"faith": 5, "energy": -15}, "critical": False},
            # 43. Парламентский кризис доверия
            {"left_effects": {"political": -10, "order": -6}, "right_effects": {"matter": -20, "political": 7}, "critical": True},
            # 44. Заговор министра безопасности
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
            "left_result": "Генералы арестовали вас прямо в кабинете. Военная диктатура установлена.",
            "right_result": "Верные вам отряды были разгромлены в уличных боях.",
            "left_effects": {"army": -100, "political": -100},
            "right_effects": {"army": -100, "political": -100},
            "critical": True
        }

        self.chaos_crisis_card = {
            "title": "КАТАСТРОФА ВЫЖИВАНИЯ: МАССОВЫЙ МОР",
            "desc": "Из-за критически низкой жизнедеятельности в течение недели люди начали массово умирать. Бунтующие толпы гроно сносят заграждения. Требуются колоссальные затраты (40 Энергии и 50 Материи) для восстановления порядка!",
            "left_preview": "БРОСИТЬ НА ПРОИЗВОЛ: Полный распад сектора.",
            "right_preview": "ЭКСТРЕННАЯ МОБИЛИЗАЦИЯ: Потратить 40 Энергии и 50 Материи.",
            "left_result": "Сектор погрузился в перманентный хаос и вымер.",
            "right_result": "Ценой колоссальных затрат и чрезвычайных мер вам удалось остановить эпидемию и хаос.",
            "left_effects": {"hab": -100, "order": -100},
            "right_effects": {"energy": -40, "matter": -50, "hab": 25, "order": 20},
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
        
        self.background_art = self.load_background_art()

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
        if not self.can_afford_choice(direction):
            return False

        card = self.get_active_card()
        if (self.revolution_active and self.final_revolution_active) or self.military_coup_active or self.chaos_crisis_active:
            self.is_defeat = True
            
        if direction == "LEFT":
            self.displayed_text = ""
            raw_effects = card["left_effects"]
            self.result_text_full = card["left_result"]
            if (self.revolution_active and self.final_revolution_active) or self.military_coup_active or self.chaos_crisis_active:
                self.is_defeat = True
        else:
            self.displayed_text = ""
            raw_effects = card["right_effects"]
            self.result_text_full = card["right_result"]
            if (self.revolution_active and self.final_revolution_active) or self.military_coup_active or self.chaos_crisis_active:
                self.is_defeat = True

        filtered_effects = {}
        for key, val in raw_effects.items():
            if val < 0:
                if key in self.stats and self.stats[key]["val"] == 0:
                    continue
                if key in ["matter", "energy"] and self.resources[key] == 0:
                    continue
                if key == "reality" and self.reality_stability == 0:
                    continue
            filtered_effects[key] = val

        self.pending_effects = filtered_effects
            
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
        else:
            self.result_chunks.append(("\n", COLOR_TEXT))
            nothing_text = get_text(self.language, "nothing_happened")
            self.result_chunks.append((nothing_text, (150, 150, 150)))

        self.result_full_string = "".join([chunk[0] for chunk in self.result_chunks])

        self.state = 'RESULT_WAIT'
        self.result_timer = 0
        self.result_phase = 'DOTS'
        self.current_char_index = 0
        return True

    def get_active_card(self):
        if self.chaos_crisis_active:
            return self.chaos_crisis_card
        if self.military_coup_active:
            return self.military_coup_card
        if self.revolution_active and self.final_revolution_active:
            return self.final_revolution_card
        if self.revolution_active:
            return self.revolution_card
        return self.card_data

    def can_afford_choice(self, direction):
        if direction not in ("LEFT", "RIGHT"):
            raise ValueError(f"Unknown choice direction: {direction}")

        card = self.get_active_card()
        choice_key = "left_effects" if direction == "LEFT" else "right_effects"
        effects = card[choice_key]
        return all(
            self.resources[resource] >= -change
            for resource, change in effects.items()
            if resource in self.resources and change < 0
        )

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

        # Механика регулярных поставок: энергия каждые 8 дней, деньги/материя каждые 10 дней по 30
        if self.turns_counter % 8 == 0:
            self.resources["energy"] += 25
        if self.turns_counter % 10 == 0:
            self.resources["matter"] += 30

        # Сброс триггеров критических кризисов при их успешном преодолении
        if self.chaos_crisis_active:
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
            # Проверка условия жизнедеятельности (0-10 в течение 7 ивентов/ходов)
            hab_val = self.stats["habitability"]["val"]
            if 0 <= hab_val <= 10:
                self.hab_low_counter += 1
                if self.hab_low_counter >= 7:
                    self.chaos_crisis_active = True
            else:
                self.hab_low_counter = 0

            # Проверка шанса военного переворота при армии > 90 (+15% с каждым днем/ходом)
            army_val = self.stats["army"]["val"]
            if army_val > 90:
                # Базовый шанс при превышении 90 составляет 15%, с каждым ходом растет еще на 15%
                coup_chance = 15 + (army_val - 90) * 3  # масштабирование для азарта
                # Простейшая детерминированная/псевдослучайная проверка через turns_counter или хэш
                import random
                if random.randint(1, 100) <= coup_chance:
                    self.military_coup_active = True

            if not self.chaos_crisis_active and not self.military_coup_active:
                if self.revolution_timer > 0:
                    self.faith_zero_counter = 0
                    if self.stats["faith"]["val"] == 0:
                        self.revolution_timer -= 1
                        if self.revolution_timer == 0:
                            self.revolution_active = True
                            self.final_revolution_active = True
                    else:
                        self.revolution_timer = 9
                else:
                    if self.stats["faith"]["val"] == 0:
                        self.faith_zero_counter += 1
                        if self.faith_zero_counter >= 3:
                            self.revolution_active = True
                            self.final_revolution_active = False
                    else:
                        self.faith_zero_counter = 0

                if not self.revolution_active:
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
                "revolution_timer": self.revolution_timer,
            }
            
        self.start_card_appearance()