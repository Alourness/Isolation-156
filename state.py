import os
import random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_ACCENT, COLOR_DANGER
from localization import LANGUAGES, TEXT, get_text


AUTOSAVE_ROLLBACK_TURNS = 12
AUTOSAVE_HISTORY_LIMIT = AUTOSAVE_ROLLBACK_TURNS + 1


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
        self.auto_save_history = []
        
        self.card_effects = [
            # Карточки 1–44 (базовые)
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
            {"left_effects": {"order": 8, "political": -8}, "right_effects": {"army": 6, "order": -5}, "critical": True},
            # Карточки 45–80 (новые сюжетные карточки с нарастающей сложностью и кризисами)
            {"left_effects": {"order": -8, "faith": -6}, "right_effects": {"energy": -30}, "critical": False},
            {"left_effects": {"hab": -10, "faith": -8}, "right_effects": {"energy": -35, "matter": -20}, "critical": False},
            {"left_effects": {"army": 10, "faith": -10}, "right_effects": {"political": -8, "matter": -25}, "critical": False},
            {"left_effects": {"reality": 8, "matter": -30}, "right_effects": {"reality": -6}, "critical": False},
            {"left_effects": {"army": -10, "order": 8}, "right_effects": {"matter": -40, "energy": -20}, "critical": True}, # Кризис
            {"left_effects": {"faith": -10}, "right_effects": {"energy": -25, "reality": -5}, "critical": False},
            {"left_effects": {"army": -8, "matter": -25}, "right_effects": {"energy": -30, "order": -5}, "critical": False},
            {"left_effects": {"hab": -12}, "right_effects": {"matter": -40}, "critical": False},
            {"left_effects": {"political": -15, "order": 15}, "right_effects": {"energy": -30, "matter": -30}, "critical": False},
            {"left_effects": {"faith": -12, "order": 10}, "right_effects": {"energy": -25}, "critical": True}, # Кризис
            {"left_effects": {"faith": -10, "hab": -10}, "right_effects": {"matter": -45}, "critical": False},
            {"left_effects": {"order": 10, "faith": -12}, "right_effects": {"energy": -35}, "critical": False},
            {"left_effects": {"hab": -15}, "right_effects": {"matter": -40, "energy": -25}, "critical": False},
            {"left_effects": {"army": 12, "faith": -12}, "right_effects": {"army": -10, "faith": 8}, "critical": False},
            {"left_effects": {"reality": -10}, "right_effects": {"energy": -50}, "critical": True}, # Кризис
            {"left_effects": {"hab": -15}, "right_effects": {"energy": -45, "matter": -30}, "critical": False},
            {"left_effects": {"order": 10, "faith": -10}, "right_effects": {"matter": -35}, "critical": False},
            {"left_effects": {"energy": -40}, "right_effects": {"reality": -10}, "critical": False},
            {"left_effects": {"faith": -15, "order": 10}, "right_effects": {}, "critical": False},
            {"left_effects": {"hab": -10}, "right_effects": {"matter": -40}, "critical": True}, # Кризис
            {"left_effects": {"reality": -8}, "right_effects": {"energy": -35}, "critical": False},
            {"left_effects": {"political": -12, "army": 10}, "right_effects": {"political": 8}, "critical": False},
            {"left_effects": {"hab": -12, "faith": -10}, "right_effects": {"energy": -50}, "critical": False},
            {"left_effects": {"faith": -15, "order": 12}, "right_effects": {"matter": -30, "energy": -20}, "critical": False},
            {"left_effects": {"faith": -20}, "right_effects": {"matter": -35, "energy": -25}, "critical": True}, # Кризис
            {"left_effects": {"faith": -15}, "right_effects": {"matter": -50, "energy": -30}, "critical": False},
            {"left_effects": {"political": -15, "order": 10}, "right_effects": {"matter": -40}, "critical": False},
            {"left_effects": {"faith": -25, "order": 15, "army": 15}, "right_effects": {"matter": -50, "energy": -40}, "critical": True}, # Предфинальный кризис
            {"left_effects": {"hab": -20}, "right_effects": {"energy": -50}, "critical": False},
            {"left_effects": {"faith": -20}, "right_effects": {"matter": -45, "energy": -40}, "critical": False},
            {"left_effects": {"political": -15, "army": 12}, "right_effects": {"political": 10}, "critical": False},
            {"left_effects": {"reality": -15}, "right_effects": {"energy": -60}, "critical": True}, # Кризис
            {"left_effects": {"hab": -20}, "right_effects": {"matter": -45, "energy": -40}, "critical": False},
            {"left_effects": {"faith": -25}, "right_effects": {"matter": -50, "energy": -40}, "critical": False},
            {"left_effects": {"faith": -30, "hab": -25}, "right_effects": {"matter": -70, "energy": -70}, "critical": True}, # 80-я карточка (Финал победы)
            {"left_effects": {}, "right_effects": {}, "critical": False}, # Эпилог / послесловие
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
        
        self.background_arts = {
            "art1": self.load_art("art1"),
            "art2": self.load_art("art2"),
            "art3": self.load_art("art3"),
            "art4": self.load_art("art4"),
            "art5": self.load_art("art5")
        }
        
        self.current_art_key = self.determine_art_key_for_current_card()
        self.background_art = self.background_arts[self.current_art_key] or self.background_arts["art1"]
        self.bg_fade_alpha = 255
        self.bg_transition_state = 'IDLE'
        self.next_art_key = self.current_art_key
        
        self.card_data = self.cards_pool[self.current_card_index]
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 160, 520, 340)
        self.card_drag_offset_x = 0
        self.is_dragging = False
        self.card_current_x = self.card_rect.x
        self.card_anim_y = self.card_rect.y
        self.card_animation_active = False
        self.card_text_char_index = 0
        self.card_text_timer = 0
        self.auto_save_history.append(self.create_save_snapshot())

    def create_save_snapshot(self):
        return {
            "stats": {key: value["val"] for key, value in self.stats.items()},
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

    def reset_autosave_history(self):
        self.auto_save_history = [self.create_save_snapshot()]

    def load_art(self, base_name):
        for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
            filename = os.path.join(os.path.dirname(__file__), f"{base_name}{ext}")
            if os.path.exists(filename):
                try:
                    img = pygame.image.load(filename).convert()
                    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                except Exception:
                    pass
        return None

    def determine_event_tags(self, card, critical=False):
        title_and_desc = f"{card.get('title', '')} {card.get('desc', '')}".casefold()
        tags = []
        if critical:
            tags.append("critical")

        tag_keywords = {
            "military": (
                "арм", "гарнизон", "военн", "министр", "совет", "офицер",
                "командир", "патрул", "бойц", "депутат", "парламент", "суд",
                "генерал", "контрабанд", "тенев", "пакт", "ультиматум",
                "служба безопасности", "army", "garrison", "military", "minister",
                "council", "officer", "commander", "patrol", "soldier", "deputy",
                "parliament", "general", "smuggl", "shadow", "pact", "ultimatum",
                "security service", "coup",
            ),
            "social": (
                "бунт", "восстан", "толп", "демонстрац", "протест", "забастов",
                "ропот", "народн", "рабоч", "митинг", "недовольств",
                "riot", "uprising", "revolt", "crowd", "demonstrat", "protest",
                "strike", "murmur", "people", "worker", "unrest", "looting",
            ),
            "anomaly": (
                "аномал", "реальност", "пространств", "квантов", "искажен",
                "разлом", "гравитац", "параллел", "исчезнов",
                "anomaly", "reality", "spatial", "quantum", "distortion",
                "rift", "gravity", "parallel", "disappear",
            ),
        }
        for tag, keywords in tag_keywords.items():
            if any(keyword in title_and_desc for keyword in keywords):
                tags.append(tag)
                break

        if not tags:
            tags.append("industrial")
        return tags

    def determine_art_key_for_current_card(self):
        card = self.get_active_card()
        if self.revolution_active or self.chaos_crisis_active or self.reality_collapse_active or self.military_coup_active:
            tags = ["critical"]
        elif self.political_paralysis_active:
            tags = ["military"]
        else:
            tags = card.get("tags", ["industrial"])

        tag_to_art = {
            "critical": "art4",
            "military": "art3",
            "social": "art2",
            "anomaly": "art5",
            "industrial": "art1",
        }
        for tag in tags:
            art_key = tag_to_art.get(tag)
            if art_key and self.background_arts.get(art_key):
                return art_key

        for fallback in ("art1", "art5", "art2", "art3", "art4"):
            if self.background_arts.get(fallback):
                return fallback
        return "art1"

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

        new_art_key = self.determine_art_key_for_current_card()
        if new_art_key != self.current_art_key:
            self.next_art_key = new_art_key
            self.bg_transition_state = 'FADING_OUT'
        elif self.bg_transition_state == 'FADING_OUT':
            self.bg_transition_state = 'FADING_IN'
        else:
            self.next_art_key = self.current_art_key

    def update_background_transition(self):
        if self.bg_transition_state == 'FADING_OUT':
            self.bg_fade_alpha -= 15
            if self.bg_fade_alpha <= 0:
                self.bg_fade_alpha = 0
                self.current_art_key = self.next_art_key
                self.background_art = self.background_arts[self.current_art_key] or self.background_arts["art1"]
                self.bg_transition_state = 'FADING_IN'
        elif self.bg_transition_state == 'FADING_IN':
            self.bg_fade_alpha += 15
            if self.bg_fade_alpha >= 255:
                self.bg_fade_alpha = 255
                self.bg_transition_state = 'IDLE'

    def start_game_over(self):
        self.state = 'GAME_OVER'
        self.game_over_alpha = 0
        self.game_over_timer = 0
        self.game_over_phase = 'FADE_IN'
        self.is_defeat = True

    def start_victory_screen(self):
        self.state = 'GAME_OVER'
        self.game_over_alpha = 0
        self.game_over_timer = 0
        self.game_over_phase = 'FADE_IN'
        self.is_defeat = False

    def restore_autosave(self):
        target_turn = max(1, self.turns_counter - AUTOSAVE_ROLLBACK_TURNS)
        eligible_snapshots = [
            snapshot
            for snapshot in self.auto_save_history
            if snapshot.get("turns", 1) <= target_turn
        ]
        if eligible_snapshots:
            data = max(eligible_snapshots, key=lambda snapshot: snapshot.get("turns", 1))
        elif self.auto_save_history:
            data = min(
                self.auto_save_history,
                key=lambda snapshot: snapshot.get("turns", 1),
            )
        else:
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
        previous_snapshots = [
            snapshot
            for snapshot in self.auto_save_history
            if snapshot.get("turns", 1) < self.turns_counter
        ]
        self.auto_save = self.create_save_snapshot()
        self.auto_save_history = (
            previous_snapshots + [self.auto_save]
        )[-AUTOSAVE_HISTORY_LIMIT:]
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
        if len(TEXT["ru"]["cards"]) != len(self.card_effects):
            raise ValueError("Canonical card tags do not match the card effects list.")
        self.cards_pool = [
            {
                **card_text,
                **effects,
                "tags": self.determine_event_tags(
                    TEXT["ru"]["cards"][index],
                    effects.get("critical", False),
                ),
            }
            for index, (card_text, effects) in enumerate(
                zip(localized["cards"], self.card_effects)
            )
        ]
        self.revolution_card = {**localized["revolution"], **self.revolution_effects}
        self.revolution_card["tags"] = ["critical", "social"]
        self.final_revolution_card = {
            **localized["final_revolution"],
            **self.final_revolution_effects,
        }
        self.final_revolution_card["tags"] = ["critical", "social"]
        self.military_coup_card = {**localized["military_coup"], **self.military_coup_card}
        self.military_coup_card["tags"] = ["critical", "military"]
        self.chaos_crisis_card = {**localized["chaos_crisis"], **self.chaos_crisis_card}
        self.chaos_crisis_card["tags"] = ["critical", "social"]
        self.political_paralysis_card = {**localized["political_paralysis"], **self.political_paralysis_card}
        self.political_paralysis_card["tags"] = ["critical", "military"]
        self.reality_collapse_card = {**localized["reality_collapse"], **self.reality_collapse_card}
        self.reality_collapse_card["tags"] = ["critical", "anomaly"]
        
        self.card_data = self.cards_pool[self.current_card_index]

    def trigger_choice(self, direction):
        card = self.get_active_card()
        
        is_ending_choice = False
        if (self.revolution_active and self.final_revolution_active) or self.military_coup_active or self.chaos_crisis_active or self.political_paralysis_active or self.reality_collapse_active:
            is_ending_choice = True
            self.is_defeat = True

        # Проверка на победную 80-ю карточку (индекс 79 в массиве)
        if self.current_card_index == 79 and not is_ending_choice:
            is_ending_choice = True
            self.is_defeat = False
            if direction == "LEFT":
                self.result_text_full = card["left_result"]
            else:
                self.result_text_full = card["right_result"]
            self.pending_effects = {}
            self.result_chunks = [(self.result_text_full, COLOR_TEXT)]
            self.result_chunks.append(("\n\n[ ПОБЕДА: ВЫ УПРАВЛЯЛИ СЕКТОРОМ 80 ЦИКЛОВ. БУНКЕР СТЕРЕЛ УГРОЗУ ИНСУФФЛЯЦИИ ]", COLOR_ACCENT))
            self.result_full_string = "".join([chunk[0] for chunk in self.result_chunks])
            self.state = 'RESULT_WAIT'
            self.result_timer = 0
            self.result_phase = 'DOTS'
            self.current_char_index = 0
            return True

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
                for stat in ("order", "faith"):
                    existing_effect = filtered_effects.get(stat, 0)
                    if existing_effect > 0:
                        existing_effect = max(1, existing_effect // 2)
                    filtered_effects[stat] = existing_effect - 15
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

        if self.current_card_index == 79 and not self.is_defeat:
            self.start_victory_screen()
            return
            
        self.turns_counter += 1

        order_val = self.stats["order"]["val"]
        faith_val = self.stats["faith"]["val"]
        army_val = self.stats["army"]["val"]
        hab_val = self.stats["habitability"]["val"]
        reality_val = self.reality_stability

        base_energy_gain = 25
        base_matter_gain = 30

        resource_penalty = 0.7 if order_val < 10 or faith_val < 10 else 1.0
        resource_bonus = 1.6 if order_val > 80 else 1.0

        total_multiplier = resource_penalty * resource_bonus

        if self.turns_counter % 6 == 0:
            self.resources["energy"] += int(base_energy_gain * total_multiplier)
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
                    # Плавное продвижение по линейке из 80 карточек
                    self.current_card_index = min(len(self.cards_pool) - 1, self.current_card_index + 1)

        self.card_data = self.get_active_card()

        snapshot = self.create_save_snapshot()
        self.auto_save_history.append(snapshot)
        self.auto_save_history = self.auto_save_history[-AUTOSAVE_HISTORY_LIMIT:]
        if self.turns_counter % 5 == 0:
            self.auto_save = snapshot
            
        self.start_card_appearance()