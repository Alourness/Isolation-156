import sys
import os
import pygame

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

COLOR_BG = (10, 14, 12)
COLOR_PANEL = (20, 28, 22)
COLOR_TEXT = (180, 210, 190)
COLOR_ACCENT = (50, 180, 90)
COLOR_DANGER = (180, 50, 40)
COLOR_BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isolation-156")
        self.clock = pygame.time.Clock()
        
        self.font_main = pygame.font.SysFont("Courier New", 20, bold=True)
        self.font_title = pygame.font.SysFont("Courier New", 28, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 14)
        
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
            "Вера людей": 50,
            "Сила армии": 50,
            "Жизнепригодность": 50,
            "Стабильность реальности": 50,
            "Политическая стабильность": 50,
            "Порядок": 50
        }
        self.resources = {
            "Казна (Материя)": 100,
            "Энергия": 80
        }
        
        self.card_data = {
            "title": "Угроза воздушного фильтра в Секторе 4",
            "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья возрастет.",
            "left_preview": "Отказать в ресурсах (Упадет Вера, сэкономим Материю)",
            "right_preview": "Выделить детали (Потратим Материю, поднимем Жизнепригодность)"
        }
        
        self.card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
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
            self.stats["Вера людей"] -= 10
            self.resources["Казна (Материя)"] += 20
        else:
            self.stats["Жизнепригодность"] += 10
            self.resources["Казна (Материя)"] -= 30
        self.card_current_x = self.card_rect.x

    def render(self):
        self.screen.fill(COLOR_BG)
        
        if self.background_art:
            self.screen.blit(self.background_art, (0, 0))
        else:
            for i in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(self.screen, (15, 20, 16), (0, i), (SCREEN_WIDTH, i), 1)

        if self.state in ('INTRO', 'WAKE_UP'):
            dialog_width = SCREEN_WIDTH - 120
            dialog_height = 180
            dialog_x = 60
            dialog_y = 40  # Окно поднято выше (было 80)
            
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((10, 12, 10, 235))
            
            # Рисуем рамку с закругленными углами (border_radius=12)
            pygame.draw.rect(dialog_surface, COLOR_ACCENT, dialog_surface.get_rect(), 2, border_radius=12)
            
            lines = self.displayed_text.split('\n')
            y_offset = 25
            for line in lines:
                text_surf = self.font_main.render(line, True, COLOR_TEXT)
                dialog_surface.blit(text_surf, (25, y_offset))
                y_offset += 32
                
            self.screen.blit(dialog_surface, (dialog_x, dialog_y))
            
            prompt_surf = self.font_small.render("[ Нажмите SPACE, чтобы продолжить ]", True, (120, 150, 130))
            self.screen.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, SCREEN_HEIGHT - 60))
            
        elif self.state == 'PLAYING':
            self.render_top_hud()
            
            card_draw_rect = pygame.Rect(self.card_current_x, self.card_rect.y, self.card_rect.width, self.card_rect.height)
            
            shadow_rect = card_draw_rect.copy()
            shadow_rect.x += 6
            shadow_rect.y += 6
            pygame.draw.rect(self.screen, COLOR_BLACK, shadow_rect)
            
            pygame.draw.rect(self.screen, COLOR_PANEL, card_draw_rect)
            pygame.draw.rect(self.screen, COLOR_ACCENT, card_draw_rect, 2)
            
            title_surf = self.font_title.render("КРИЗИС СЕКТОРА", True, COLOR_ACCENT)
            self.screen.blit(title_surf, (card_draw_rect.x + 20, card_draw_rect.y + 20))
            
            desc_y = card_draw_rect.y + 70
            words = self.card_data["desc"].split(' ')
            line = ""
            for word in words:
                test_line = line + word + " "
                if self.font_main.size(test_line)[0] > card_draw_rect.width - 40:
                    desc_surf = self.font_main.render(line, True, COLOR_TEXT)
                    self.screen.blit(desc_surf, (card_draw_rect.x + 20, desc_y))
                    desc_y += 24
                    line = word + " "
                else:
                    line = test_line
            desc_surf = self.font_main.render(line, True, COLOR_TEXT)
            self.screen.blit(desc_surf, (card_draw_rect.x + 20, desc_y))
            
            offset_delta = self.card_current_x - self.card_rect.x
            if offset_delta < -30:
                prev_surf = self.font_small.render(self.card_data["left_preview"], True, COLOR_DANGER)
                self.screen.blit(prev_surf, (60, SCREEN_HEIGHT - 90))
            elif offset_delta > 30:
                prev_surf = self.font_small.render(self.card_data["right_preview"], True, COLOR_ACCENT)
                self.screen.blit(prev_surf, (SCREEN_WIDTH - prev_surf.get_width() - 60, SCREEN_HEIGHT - 90))

        if self.intro_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill(COLOR_BLACK)
            fade_surf.set_alpha(self.intro_alpha)
            self.screen.blit(fade_surf, (0, 0))

        pygame.display.flip()

    def render_top_hud(self):
        hud_rect = pygame.Rect(20, 20, SCREEN_WIDTH - 40, 60)
        pygame.draw.rect(self.screen, COLOR_PANEL, hud_rect)
        pygame.draw.rect(self.screen, COLOR_ACCENT, hud_rect, 1)
        
        x_offset = 35
        for stat_name, val in self.stats.items():
            stat_text = self.font_small.render(f"{stat_name[:4]}: {val}%", True, COLOR_TEXT)
            self.screen.blit(stat_text, (x_offset, hud_rect.y + 20))
            x_offset += 190

if __name__ == "__main__":
    game = Game()
    game.run()