import sys
import os
import pygame

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

COLOR_BG = (10, 13, 11)
COLOR_CARD_BG = (22, 26, 23)
COLOR_TEXT = (195, 215, 200)
COLOR_ACCENT = (70, 190, 110)
COLOR_DANGER = (210, 65, 55)
COLOR_WARNING = (215, 175, 60)
COLOR_ANOMALY = (70, 200, 215)
COLOR_BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isolation-156")
        self.clock = pygame.time.Clock()
        
        self.font_main = pygame.font.SysFont("Courier New", 18, bold=True)
        self.font_title = pygame.font.SysFont("Courier New", 26, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_hud = pygame.font.SysFont("Courier New", 13, bold=True)
        
        self.background_art = self.load_background_art()
        
        self.state = 'INTRO'
        
        self.intro_alpha = 255
        self.intro_text = (
            "Идет 156 год после Инсуффляции...\n"
            "Старый мир сжат, скомкан и сплавлен в бесконечный многослойный лабиринт.\n"
            "Нет неба и земли — только бетон, ржавые трубы и гул вентиляции."
        )
        self.current_char_index = 0
        self.displayed_text = ""
        self.text_timer = 0
        self.text_speed = 3
        
        self.stats = {
            "Вера людей": {"val": 50, "color": (230, 200, 100), "icon": "✦"},
            "Сила армии": {"val": 50, "color": (210, 80, 80), "icon": "⚔"},
            "Жизнепригодность": {"val": 50, "color": (80, 190, 130), "icon": "🫁"},
            "Политическая стабильность": {"val": 50, "color": (150, 110, 210), "icon": "⚖"},
            "Порядок": {"val": 50, "color": (220, 140, 60), "icon": "☩"}
        }
        
        self.reality_stability = 65
        
        self.resources = {
            "Материя": 100,
            "Энергия": 80
        }
        
        self.card_data = {
            "title": "Угроза воздушного фильтра в Секторе 4",
            "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья возрастет.",
            "left_preview": "ОТКАЗАТЬ: Сохранить Материю, уронить Веру людей",
            "right_preview": "ВЫДЕЛИТЬ ДЕТАЛИ: Потратить Материю, поднять Жизнепригодность"
        }
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 - 140, 420, 320)
        self.card_drag_offset_x = 0
        self.is_dragging = False
        self.card_current_x = self.card_rect.x

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

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if self.state == 'INTRO':
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if self.current_char_index < len(self.intro_text):
                            self.displayed_text = self.intro_text
                            self.current_char_index = len(self.intro_text)
                        else:
                            self.state = 'WAKE_UP'
                            self.displayed_text = "Вы просыпаетесь за своим рабочим столом...\nВам приносят первые извести, из которых вы должны принять первое решение."
                            self.current_char_index = len(self.displayed_text)
                            
                elif self.state == 'WAKE_UP':
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.state = 'PLAYING'
                        
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == 'PLAYING':
                if event.button == 1:
                    if self.card_rect.collidepoint((event.pos[0] - (self.card_current_x - self.card_rect.x), event.pos[1])):
                        self.is_dragging = True
                        self.card_drag_offset_x = event.pos[0] - self.card_current_x
                        
            elif event.type == pygame.MOUSEBUTTONUP and self.state == 'PLAYING':
                if event.button == 1:
                    if self.is_dragging:
                        self.is_dragging = False
                        if self.card_current_x < self.card_rect.x - 120:
                            self.resolve_choice("LEFT")
                        elif self.card_current_x > self.card_rect.x + 120:
                            self.resolve_choice("RIGHT")
                        else:
                            self.card_current_x = self.card_rect.x
                            
            elif event.type == pygame.MOUSEMOTION and self.state == 'PLAYING':
                if self.is_dragging:
                    self.card_current_x = event.pos[0] - self.card_drag_offset_x

    def update(self):
        if self.state == 'INTRO':
            if self.intro_alpha > 0:
                self.intro_alpha = max(0, self.intro_alpha - 2)
                
            if self.current_char_index < len(self.intro_text):
                self.text_timer += 1
                if self.text_timer >= self.text_speed:
                    self.current_char_index += 1
                    self.displayed_text = self.intro_text[:self.current_char_index]
                    self.text_timer = 0

    def resolve_choice(self, direction):
        if direction == "LEFT":
            self.stats["Вера людей"]["val"] = max(0, self.stats["Вера людей"]["val"] - 15)
            self.resources["Материя"] += 25
        else:
            self.stats["Жизнепригодность"]["val"] = min(100, self.stats["Жизнепригодность"]["val"] + 15)
            self.resources["Материя"] = max(0, self.resources["Материя"] - 30)
        self.card_current_x = self.card_rect.x

    def render(self):
        self.screen.fill(COLOR_BG)
        
        if self.background_art:
            self.screen.blit(self.background_art, (0, 0))
        else:
            for i in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(self.screen, (15, 20, 16), (0, i), (SCREEN_WIDTH, i), 1)

        if self.state in ('INTRO', 'WAKE_UP'):
            dialog_width = SCREEN_WIDTH - 40
            dialog_height = 130
            dialog_x = 20
            dialog_y = 10
            
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((10, 12, 10, 245))
            
            pygame.draw.rect(dialog_surface, COLOR_ACCENT, dialog_surface.get_rect(), 2, border_radius=8)
            
            lines = self.displayed_text.split('\n')
            y_offset = 18
            for line in lines:
                text_surf = self.font_main.render(line, True, COLOR_TEXT)
                dialog_surface.blit(text_surf, (25, y_offset))
                y_offset += 30
                
            self.screen.blit(dialog_surface, (dialog_x, dialog_y))
            
            prompt_surf = self.font_small.render("[ Нажмите SPACE, чтобы продолжить ]", True, COLOR_ACCENT)
            self.screen.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, SCREEN_HEIGHT - 45))
            
        elif self.state == 'PLAYING':
            self.render_top_hud()
            self.render_side_economy()
            self.render_anomaly_indicator()
            
            card_draw_rect = pygame.Rect(self.card_current_x, self.card_rect.y, self.card_rect.width, self.card_rect.height)
            
            shadow_rect = card_draw_rect.copy()
            shadow_rect.x += 8
            shadow_rect.y += 8
            pygame.draw.rect(self.screen, COLOR_BLACK, shadow_rect, border_radius=6)
            
            pygame.draw.rect(self.screen, COLOR_CARD_BG, card_draw_rect, border_radius=6)
            pygame.draw.rect(self.screen, (75, 95, 80), card_draw_rect, 2, border_radius=6)
            pygame.draw.rect(self.screen, COLOR_ACCENT, card_draw_rect.inflate(-8, -8), 1, border_radius=4)
            
            title_surf = self.font_title.render("КРИЗИС СЕКТОРА", True, COLOR_ACCENT)
            self.screen.blit(title_surf, (card_draw_rect.x + 25, card_draw_rect.y + 25))
            
            desc_y = card_draw_rect.y + 80
            words = self.card_data["desc"].split(' ')
            line = ""
            for word in words:
                test_line = line + word + " "
                if self.font_main.size(test_line)[0] > card_draw_rect.width - 50:
                    desc_surf = self.font_main.render(line, True, COLOR_TEXT)
                    self.screen.blit(desc_surf, (card_draw_rect.x + 25, desc_y))
                    desc_y += 24
                    line = word + " "
                else:
                    line = test_line
            desc_surf = self.font_main.render(line, True, COLOR_TEXT)
            self.screen.blit(desc_surf, (card_draw_rect.x + 25, desc_y))
            
            offset_delta = self.card_current_x - self.card_rect.x
            if offset_delta < -35:
                preview_surf = self.font_main.render(self.card_data["left_preview"], True, COLOR_DANGER)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((25, 12, 12, 240))
                pygame.draw.rect(bg_surf, COLOR_DANGER, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (60, SCREEN_HEIGHT - 100))
                
            elif offset_delta > 35:
                preview_surf = self.font_main.render(self.card_data["right_preview"], True, COLOR_ACCENT)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((12, 25, 16, 240))
                pygame.draw.rect(bg_surf, COLOR_ACCENT, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (SCREEN_WIDTH - bg_surf.get_width() - 60, SCREEN_HEIGHT - 100))

        if self.intro_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill(COLOR_BLACK)
            fade_surf.set_alpha(self.intro_alpha)
            self.screen.blit(fade_surf, (0, 0))

        pygame.display.flip()

    def render_top_hud(self):
        panel_width = 860
        panel_height = 55
        panel_x = 20
        panel_y = 15
        
        hud_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        hud_surf.fill((15, 22, 18, 240))
        pygame.draw.rect(hud_surf, COLOR_ACCENT, hud_surf.get_rect(), 2, border_radius=8)
        
        x_offset = 15
        bar_width = 100
        bar_height = 10
        
        for stat_name, data in self.stats.items():
            val = data["val"]
            color = data["color"]
            icon = data["icon"]
            
            icon_surf = self.font_hud.render(f"{icon} {stat_name[:6]}", True, color)
            hud_surf.blit(icon_surf, (x_offset, 10))
            
            bar_x = x_offset
            bar_y = 30
            pygame.draw.rect(hud_surf, (35, 45, 38), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
            
            fill_w = int((val / 100.0) * bar_width)
            fill_color = color if val > 30 else COLOR_DANGER
            if fill_w > 0:
                pygame.draw.rect(hud_surf, fill_color, (bar_x, bar_y, fill_w, bar_height), border_radius=3)
            
            val_surf = self.font_hud.render(f"{val}%", True, COLOR_TEXT)
            hud_surf.blit(val_surf, (bar_x + bar_width + 6, bar_y - 2))
            
            x_offset += 165
            
        self.screen.blit(hud_surf, (panel_x, panel_y))

    def render_side_economy(self):
        panel_width = 200
        panel_height = 110
        panel_x = SCREEN_WIDTH - 220
        panel_y = 15
        
        econ_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        econ_surf.fill((18, 24, 20, 240))
        pygame.draw.rect(econ_surf, COLOR_WARNING, econ_surf.get_rect(), 2, border_radius=8)
        
        title_surf = self.font_small.render("РЕСУРСЫ СЕКТОРА", True, COLOR_WARNING)
        econ_surf.blit(title_surf, (15, 12))
        
        y_pos = 42
        for res_name, res_val in self.resources.items():
            res_surf = self.font_hud.render(f"• {res_name}: {res_val}", True, COLOR_TEXT)
            econ_surf.blit(res_surf, (15, y_pos))
            y_pos += 26
            
        self.screen.blit(econ_surf, (panel_x, panel_y))

    def render_anomaly_indicator(self):
        panel_width = 200
        panel_height = 75
        panel_x = SCREEN_WIDTH - 220
        panel_y = SCREEN_HEIGHT - 95
        
        anom_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        anom_surf.fill((15, 25, 28, 240))
        pygame.draw.rect(anom_surf, COLOR_ANOMALY, anom_surf.get_rect(), 2, border_radius=8)
        
        title_surf = self.font_hud.render("СТАБИЛЬНОСТЬ РЕАЛЬНОСТИ", True, COLOR_ANOMALY)
        anom_surf.blit(title_surf, (12, 10))
        
        bar_x = 12
        bar_y = 36
        bar_width = 176
        bar_height = 12
        pygame.draw.rect(anom_surf, (30, 45, 48), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
        
        fill_w = int((self.reality_stability / 100.0) * bar_width)
        if fill_w > 0:
            pygame.draw.rect(anom_surf, COLOR_ANOMALY, (bar_x, bar_y, fill_w, bar_height), border_radius=3)
            
        val_surf = self.font_hud.render(f"{self.reality_stability}%", True, COLOR_TEXT)
        anom_surf.blit(val_surf, (bar_x + bar_width - 35, bar_y - 2))
        
        self.screen.blit(anom_surf, (panel_x, panel_y))

if __name__ == "__main__":
    game = Game()
    game.run()