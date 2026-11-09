import sys
import pygame
from config import *
from state import GameState
from ui import render_top_hud, render_side_economy, render_anomaly_radial

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isolation-156")
        self.clock = pygame.time.Clock()
        self.gs = GameState()

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
                if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        target_text = self.gs.intro_texts[0] if self.gs.state == 'INTRO_1' else (self.gs.intro_texts[1] if self.gs.state == 'INTRO_2' else self.gs.intro_texts[2])
                        if self.gs.current_char_index < len(target_text):
                            self.gs.displayed_text = target_text
                            self.gs.current_char_index = len(target_text)
                        else:
                            if self.gs.state == 'INTRO_1':
                                self.gs.state = 'INTRO_2'
                                self.gs.current_char_index = 0
                                self.gs.displayed_text = ""
                            elif self.gs.state == 'INTRO_2':
                                self.gs.state = 'INTRO_3'
                                self.gs.current_char_index = 0
                                self.gs.displayed_text = ""
                            else:
                                self.gs.state = 'PLAYING'
                                
                elif self.gs.state == 'RESULT_WAIT':
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if self.gs.result_phase == 'TEXT' and self.gs.current_char_index >= len(self.gs.result_full_string):
                            self.gs.apply_pending_effects()
                            self.gs.state = 'PLAYING'
                        elif self.gs.result_phase == 'DOTS':
                            self.gs.result_phase = 'TEXT'
                            self.gs.current_char_index = 0
                            self.gs.displayed_text = ""
                            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.gs.state == 'PLAYING':
                if event.button == 1:
                    if self.gs.card_rect.collidepoint((event.pos[0] - (self.gs.card_current_x - self.gs.card_rect.x), event.pos[1])):
                        self.gs.is_dragging = True
                        self.gs.card_drag_offset_x = event.pos[0] - self.gs.card_current_x
                        
            elif event.type == pygame.MOUSEBUTTONUP and self.gs.state == 'PLAYING':
                if event.button == 1:
                    if self.gs.is_dragging:
                        self.gs.is_dragging = False
                        if self.gs.card_current_x < self.gs.card_rect.x - 120:
                            self.gs.trigger_choice("LEFT")
                        elif self.gs.card_current_x > self.gs.card_rect.x + 120:
                            self.gs.trigger_choice("RIGHT")
                        else:
                            self.gs.card_current_x = self.gs.card_rect.x
                            
            elif event.type == pygame.MOUSEMOTION and self.gs.state == 'PLAYING':
                if self.gs.is_dragging:
                    self.gs.card_current_x = event.pos[0] - self.gs.card_drag_offset_x

    def update(self):
        if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
            if self.gs.intro_alpha > 0:
                self.gs.intro_alpha = max(0, self.gs.intro_alpha - 2)
                
            target_text = self.gs.intro_texts[0] if self.gs.state == 'INTRO_1' else (self.gs.intro_texts[1] if self.gs.state == 'INTRO_2' else self.gs.intro_texts[2])
            if self.gs.current_char_index < len(target_text):
                self.gs.text_timer += 1
                if self.gs.text_timer >= self.gs.text_speed:
                    self.gs.current_char_index += 2
                    if self.gs.current_char_index > len(target_text):
                        self.gs.current_char_index = len(target_text)
                    self.gs.displayed_text = target_text[:self.gs.current_char_index]
                    self.gs.text_timer = 0
                    
        elif self.gs.state == 'RESULT_WAIT':
            if self.gs.result_phase == 'DOTS':
                self.gs.result_timer += 1
                if self.gs.result_timer > 15:
                    self.gs.displayed_text += "."
                    self.gs.result_timer = 0
                    if len(self.gs.displayed_text) >= 3:
                        self.gs.result_phase = 'TEXT'
                        self.gs.current_char_index = 0
                        self.gs.displayed_text = ""
            elif self.gs.result_phase == 'TEXT':
                if self.gs.current_char_index < len(self.gs.result_full_string):
                    self.gs.text_timer += 1
                    if self.gs.text_timer >= self.gs.text_speed:
                        self.gs.current_char_index += 2
                        if self.gs.current_char_index > len(self.gs.result_full_string):
                            self.gs.current_char_index = len(self.gs.result_full_string)
                        
                        chars_left = self.gs.current_char_index
                        current_rendered_chunks = []
                        for text_chunk, col in self.gs.result_chunks:
                            if chars_left <= 0:
                                break
                            if len(text_chunk) <= chars_left:
                                current_rendered_chunks.append((text_chunk, col))
                                chars_left -= len(text_chunk)
                            else:
                                current_rendered_chunks.append((text_chunk[:chars_left], col))
                                chars_left = 0
                        self.gs.current_rendered_chunks = current_rendered_chunks
                        self.gs.text_timer = 0

    def render(self):
        self.screen.fill(COLOR_BG)
        
        if self.gs.background_art:
            self.screen.blit(self.gs.background_art, (0, 0))
        else:
            for i in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(self.screen, (12, 18, 14), (0, i), (SCREEN_WIDTH, i), 1)

        if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3', 'RESULT_WAIT'):
            dialog_width = SCREEN_WIDTH - 40
            dialog_height = 140
            dialog_x = 20
            dialog_y = 10
            
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((8, 11, 9, 250))
            
            pygame.draw.rect(dialog_surface, COLOR_ACCENT, dialog_surface.get_rect(), 2, border_radius=8)
            
            if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
                lines = self.gs.displayed_text.split('\n')
                y_offset = 18
                for line in lines:
                    text_surf = FONT_MAIN.render(line, True, COLOR_TEXT)
                    dialog_surface.blit(text_surf, (25, y_offset))
                    y_offset += 30
            elif self.gs.state == 'RESULT_WAIT':
                if self.gs.result_phase == 'DOTS':
                    text_surf = FONT_MAIN.render(self.gs.displayed_text, True, COLOR_TEXT)
                    dialog_surface.blit(text_surf, (25, 18))
                elif self.gs.result_phase == 'TEXT':
                    chunks = getattr(self.gs, 'current_rendered_chunks', [])
                    current_x = 25
                    current_y = 18
                    for text_chunk, col in chunks:
                        if "\n" in text_chunk:
                            parts = text_chunk.split("\n")
                            for i, part in enumerate(parts):
                                if i > 0:
                                    current_x = 25
                                    current_y += 30
                                if part:
                                    part_surf = FONT_MAIN.render(part, True, col)
                                    dialog_surface.blit(part_surf, (current_x, current_y))
                                    current_x += part_surf.get_width()
                        else:
                            if text_chunk:
                                chunk_surf = FONT_MAIN.render(text_chunk, True, col)
                                dialog_surface.blit(chunk_surf, (current_x, current_y))
                                current_x += chunk_surf.get_width()
                
            self.screen.blit(dialog_surface, (dialog_x, dialog_y))
            
            prompt_surf = FONT_SMALL.render("[ Нажмите SPACE, чтобы продолжить ]", True, COLOR_ACCENT)
            self.screen_blit_center_x = SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2
            self.screen.blit(prompt_surf, (self.screen_blit_center_x, SCREEN_HEIGHT - 45))
            
        if self.gs.state == 'PLAYING':
            render_top_hud(self.screen, self.gs.stats)
            render_side_economy(self.screen, self.gs.resources)
            render_anomaly_radial(self.screen, self.gs.reality_stability)
            
            card_draw_rect = pygame.Rect(self.gs.card_current_x, self.gs.card_rect.y, self.gs.card_rect.width, self.gs.card_rect.height)
            
            pygame.draw.rect(self.screen, COLOR_CARD_BG, card_draw_rect, border_radius=12)
            pygame.draw.rect(self.screen, (90, 110, 95), card_draw_rect, 3, border_radius=12)
            pygame.draw.rect(self.screen, (50, 65, 55), card_draw_rect.inflate(-8, -8), 1, border_radius=10)
            pygame.draw.rect(self.screen, (110, 135, 115), card_draw_rect.inflate(-16, -16), 1, border_radius=8)
            
            active_card = self.gs.revolution_card if self.gs.revolution_active else self.gs.card_data
            
            # Рендерим заголовок карточки с автоматическим переносом, если он длинный
            title_words = active_card["title"].split(' ')
            title_line = ""
            title_y = card_draw_rect.y + 25
            max_title_width = card_draw_rect.width - 60
            
            for word in title_words:
                test_title_line = title_line + word + " "
                if FONT_TITLE.size(test_title_line)[0] > max_title_width:
                    t_surf = FONT_TITLE.render(title_line, True, (225, 235, 228))
                    self.screen.blit(t_surf, (card_draw_rect.x + 30, title_y))
                    title_y += 30
                    title_line = word + " "
                else:
                    title_line = test_title_line
            t_surf = FONT_TITLE.render(title_line, True, (225, 235, 228))
            self.screen.blit(t_surf, (card_draw_rect.x + 30, title_y))
            
            # Описание карточки
            words = active_card["desc"].split(' ')
            line = ""
            desc_y = title_y + 45
            for word in words:
                test_line = line + word + " "
                if FONT_MAIN.size(test_line)[0] > max_title_width:
                    desc_surf = FONT_MAIN.render(line, True, (190, 210, 195))
                    self.screen.blit(desc_surf, (card_draw_rect.x + 30, desc_y))
                    desc_y += 24
                    line = word + " "
                else:
                    line = test_line
            desc_surf = FONT_MAIN.render(line, True, (190, 210, 195))
            self.screen.blit(desc_surf, (card_draw_rect.x + 30, desc_y))
            
            offset_delta = self.gs.card_current_x - self.gs.card_rect.x
            if offset_delta < -35:
                preview_surf = FONT_MAIN.render(active_card["left_preview"], True, COLOR_DANGER)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((25, 12, 12, 240))
                pygame.draw.rect(bg_surf, COLOR_DANGER, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (60, SCREEN_HEIGHT - 100))
                
            elif offset_delta > 35:
                preview_surf = FONT_MAIN.render(active_card["right_preview"], True, COLOR_ACCENT)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((12, 25, 16, 240))
                pygame.draw.rect(bg_surf, COLOR_ACCENT, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (SCREEN_WIDTH - bg_surf.get_width() - 60, SCREEN_HEIGHT - 100))

        if self.gs.intro_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill(COLOR_BLACK)
            fade_surf.set_alpha(self.gs.intro_alpha)
            self.screen.blit(fade_surf, (0, 0))

        pygame.display.flip()

if __name__ == "__main__":
    game: Game = Game()
    game.run()