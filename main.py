import sys
import pygame
from config import *
from state import GameState
from ui import (
    render_top_hud,
    render_side_economy,
    render_anomaly_radial,
    render_gradient_background,
    render_wrapped_text,
)
from localization import LANGUAGES, get_text, load_language, save_language

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isolation-156")
        self.clock = pygame.time.Clock()
        self.gs = GameState(load_language())
        self.tick_counter = 0

    def run(self):
        while True:
            self.tick_counter += 1
            delta_ms = self.clock.tick(FPS)
            self.handle_events()
            self.update(delta_ms)
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.gs.state == 'MENU':
                    if self.menu_btn_start.collidepoint(mouse_pos):
                        self.gs.state = 'INTRO_1'
                    elif self.menu_btn_saves.collidepoint(mouse_pos):
                        self.gs.state = 'LOAD_MENU'
                    elif self.menu_btn_exit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif self.menu_btn_language.collidepoint(mouse_pos):
                        language_index = LANGUAGES.index(self.gs.language)
                        language = LANGUAGES[(language_index + 1) % len(LANGUAGES)]
                        save_language(language)
                        self.gs.set_language(language)
                elif self.gs.state == 'LOAD_MENU':
                    if self.back_btn_rect.collidepoint(mouse_pos):
                        self.gs.state = 'MENU'
                    for i, rect in enumerate(self.slot_rects):
                        if rect.collidepoint(mouse_pos):
                            if self.gs.save_slots[i] is not None:
                                data = self.gs.save_slots[i]
                                for k, v in data["stats"].items():
                                    self.gs.stats[k]["val"] = v
                                self.gs.resources = data["resources"].copy()
                                self.gs.reality_stability = data["reality"]
                                self.gs.current_card_index = data["card_idx"]
                                self.gs.card_data = self.gs.cards_pool[self.gs.current_card_index]
                                self.gs.turns_counter = data.get("turns", 1)
                                self.gs.start_card_appearance()
                            else:
                                self.gs.save_slots[i] = {
                                    "stats": {k: v["val"] for k, v in self.gs.stats.items()},
                                    "resources": self.gs.resources.copy(),
                                    "reality": self.gs.reality_stability,
                                    "card_idx": self.gs.current_card_index,
                                    "turns": self.gs.turns_counter
                                }
                    if hasattr(self, 'auto_slot_rect') and self.auto_slot_rect.collidepoint(mouse_pos):
                        if self.gs.auto_save is not None:
                            data = self.gs.auto_save
                            for k, v in data["stats"].items():
                                self.gs.stats[k]["val"] = v
                            self.gs.resources = data["resources"].copy()
                            self.gs.reality_stability = data["reality"]
                            self.gs.current_card_index = data["card_idx"]
                            self.gs.card_data = self.gs.cards_pool[self.gs.current_card_index]
                            self.gs.turns_counter = data.get("turns", 1)
                            self.gs.start_card_appearance()
                elif self.gs.state == 'PLAYING':
                    if not self.gs.card_animation_active and self.gs.card_rect.collidepoint(
                        (event.pos[0] - (self.gs.card_current_x - self.gs.card_rect.x), event.pos[1])
                    ):
                        self.gs.is_dragging = True
                        self.gs.card_drag_offset_x = event.pos[0] - self.gs.card_current_x

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.gs.state == 'PLAYING' and self.gs.is_dragging:
                    self.gs.is_dragging = False
                    if self.gs.card_current_x < self.gs.card_rect.x - 120:
                        self.gs.trigger_choice("LEFT")
                    elif self.gs.card_current_x > self.gs.card_rect.x + 120:
                        self.gs.trigger_choice("RIGHT")
                    else:
                        self.gs.card_current_x = self.gs.card_rect.x

            elif event.type == pygame.MOUSEMOTION:
                if self.gs.state == 'PLAYING' and self.gs.is_dragging:
                    self.gs.card_current_x = event.pos[0] - self.gs.card_drag_offset_x

            elif event.type == pygame.KEYDOWN:
                if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        target_text = self.gs.intro_texts[0] if self.gs.state == 'INTRO_1' else (self.gs.intro_texts[1] if self.gs.state == 'INTRO_2' else self.gs.intro_texts[2])
                        if self.gs.current_char_index < len(target_text):
                            self.gs.text_fast = True
                        else:
                            if self.gs.state == 'INTRO_1':
                                self.gs.state = 'INTRO_2'
                                self.gs.current_char_index = 0
                                self.gs.displayed_text = ""
                                self.gs.text_fast = False
                            elif self.gs.state == 'INTRO_2':
                                self.gs.state = 'INTRO_3'
                                self.gs.current_char_index = 0
                                self.gs.displayed_text = ""
                                self.gs.text_fast = False
                            else:
                                self.gs.start_card_appearance()
                                
                elif self.gs.state == 'RESULT_WAIT':
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if self.gs.result_phase == 'TEXT' and self.gs.current_char_index < len(self.gs.result_full_string):
                            self.gs.text_fast = True
                        elif self.gs.result_phase == 'TEXT' and self.gs.current_char_index >= len(self.gs.result_full_string):
                            self.gs.apply_pending_effects()
                        elif self.gs.result_phase == 'DOTS':
                            self.gs.result_phase = 'TEXT'
                            self.gs.current_char_index = 0
                            self.gs.displayed_text = ""
                            self.gs.text_fast = False
                elif self.gs.state == 'PLAYING' and self.gs.card_animation_active:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.gs.text_fast = True

    def update(self, delta_ms=1000 / FPS):
        if self.gs.state == 'MENU':
            if self.gs.menu_alpha > 0:
                self.gs.menu_alpha = max(0, self.gs.menu_alpha - 5)

        if self.gs.game_over_phase == 'FADE_IN':
            self.gs.game_over_alpha = min(
                255, self.gs.game_over_alpha + 255 * delta_ms / 1200
            )
            if self.gs.game_over_alpha >= 255:
                self.gs.game_over_phase = 'HOLD'
                self.gs.game_over_timer = 0
        elif self.gs.game_over_phase == 'HOLD':
            self.gs.game_over_timer += delta_ms
            if self.gs.game_over_timer >= 3000:
                self.gs.restore_autosave()
        elif self.gs.game_over_phase == 'FADE_OUT':
            self.gs.game_over_alpha = max(
                0, self.gs.game_over_alpha - 255 * delta_ms / 1200
            )
            if self.gs.game_over_alpha == 0:
                self.gs.game_over_phase = None

        current_speed = 1 if self.gs.text_fast else self.gs.text_speed

        if self.gs.state in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
            if self.gs.intro_alpha > 0:
                self.gs.intro_alpha = max(0, self.gs.intro_alpha - 2)
                
            target_text = self.gs.intro_texts[0] if self.gs.state == 'INTRO_1' else (self.gs.intro_texts[1] if self.gs.state == 'INTRO_2' else self.gs.intro_texts[2])
            if self.gs.current_char_index < len(target_text):
                self.gs.text_timer += 1
                if self.gs.text_timer >= current_speed:
                    self.gs.current_char_index += 1
                    if self.gs.current_char_index > len(target_text):
                        self.gs.current_char_index = len(target_text)
                    self.gs.displayed_text = target_text[:self.gs.current_char_index]
                    self.gs.text_timer = 0
                    
        elif self.gs.state == 'RESULT_WAIT':
            if self.gs.result_phase == 'DOTS':
                self.gs.result_timer += 1
                dots_speed = 5 if self.gs.text_fast else 20
                if self.gs.result_timer > dots_speed:
                    self.gs.displayed_text += "."
                    self.gs.result_timer = 0
                    if len(self.gs.displayed_text) >= 3:
                        self.gs.result_phase = 'TEXT'
                        self.gs.current_char_index = 0
                        self.gs.displayed_text = ""
                        self.gs.text_fast = False
            elif self.gs.result_phase == 'TEXT':
                if self.gs.current_char_index < len(self.gs.result_full_string):
                    self.gs.text_timer += 1
                    if self.gs.text_timer >= current_speed:
                        self.gs.current_char_index += 1
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
                        
        elif self.gs.state == 'GAME_OVER':
            pass

        elif self.gs.state == 'PLAYING':
            if self.gs.card_fade_alpha < 255:
                self.gs.card_fade_alpha = min(255, self.gs.card_fade_alpha + 15)

            if self.gs.card_animation_active:
                self.gs.card_anim_y = max(self.gs.card_rect.y, self.gs.card_anim_y - 18)
                active_card = self.gs.final_revolution_card if (
                    self.gs.revolution_active and self.gs.revolution_timer <= 0
                ) else (
                    self.gs.revolution_card if self.gs.revolution_active else self.gs.card_data
                )
                card_text_length = len(active_card["title"]) + len(active_card["desc"])
                if self.gs.card_text_char_index < card_text_length:
                    self.gs.card_text_timer += 1
                    if self.gs.card_text_timer >= current_speed:
                        self.gs.card_text_char_index += 1
                        self.gs.card_text_timer = 0

                if (
                    self.gs.card_anim_y == self.gs.card_rect.y
                    and self.gs.card_text_char_index >= card_text_length
                ):
                    self.gs.card_animation_active = False
                    self.gs.text_fast = False

    def render(self):
        render_gradient_background(self.screen, self.tick_counter)
        
        if self.gs.background_art and self.gs.state not in ('MENU', 'LOAD_MENU'):
            art_surf = self.gs.background_art.copy()
            art_surf.set_alpha(100)
            self.screen.blit(art_surf, (0, 0))

        if self.gs.state == 'MENU':
            title_surf = FONT_TITLE.render("ISOLATION-156", True, COLOR_TEXT)
            self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 180))
            
            self.menu_btn_start = pygame.Rect(SCREEN_WIDTH // 2 - 150, 280, 300, 50)
            self.menu_btn_saves = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350, 300, 50)
            self.menu_btn_exit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 420, 300, 50)
            self.menu_btn_language = pygame.Rect(SCREEN_WIDTH // 2 - 150, 490, 300, 50)
            
            menu_buttons = [
                (self.menu_btn_start, "menu_start"),
                (self.menu_btn_saves, "menu_saves"),
                (self.menu_btn_exit, "menu_exit"),
                (self.menu_btn_language, "language_button"),
            ]
            for rect, text_key in menu_buttons:
                pygame.draw.rect(self.screen, (15, 25, 18), rect, border_radius=8)
                pygame.draw.rect(self.screen, COLOR_ACCENT, rect, 2, border_radius=8)
                t_surf = FONT_MAIN.render(get_text(self.gs.language, text_key), True, COLOR_TEXT)
                self.screen.blit(t_surf, (rect.centerx - t_surf.get_width() // 2, rect.centery - t_surf.get_height() // 2))

        elif self.gs.state == 'LOAD_MENU':
            title_surf = FONT_TITLE.render(get_text(self.gs.language, "saves_title"), True, COLOR_TEXT)
            self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))
            
            auto_label = FONT_SMALL.render(get_text(self.gs.language, "autosave"), True, COLOR_WARNING)
            self.screen.blit(auto_label, (100, 130))
            self.auto_slot_rect = pygame.Rect(100, 160, 260, 420)
            pygame.draw.rect(self.screen, (12, 20, 15), self.auto_slot_rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_WARNING, self.auto_slot_rect, 2, border_radius=8)
            if self.gs.auto_save is not None:
                as_text = FONT_MAIN.render(get_text(self.gs.language, "autosave_saved"), True, COLOR_ACCENT)
                self.screen.blit(as_text, (self.auto_slot_rect.x + 20, self.auto_slot_rect.y + 30))
            else:
                as_text = FONT_MAIN.render(get_text(self.gs.language, "empty"), True, (100, 110, 105))
                self.screen.blit(as_text, (self.auto_slot_rect.centerx - as_text.get_width() // 2, self.auto_slot_rect.centery))

            self.slot_rects = []
            grid_x, grid_y = 400, 160
            for i in range(6):
                col = i % 3
                row = i // 3
                rx = grid_x + col * 280
                ry = grid_y + row * 220
                r = pygame.Rect(rx, ry, 260, 200)
                self.slot_rects.append(r)
                
                pygame.draw.rect(self.screen, (12, 20, 15), r, border_radius=8)
                pygame.draw.rect(self.screen, COLOR_ACCENT, r, 2, border_radius=8)
                
                slot_num = FONT_SMALL.render(f"{get_text(self.gs.language, 'slot')} {i+1}", True, COLOR_TEXT)
                self.screen.blit(slot_num, (r.x + 15, r.y + 15))
                
                if self.gs.save_slots[i] is not None:
                    desc_surf = FONT_SMALL.render(get_text(self.gs.language, "occupied"), True, COLOR_ACCENT)
                    self.screen.blit(desc_surf, (r.centerx - desc_surf.get_width() // 2, r.centery))
                else:
                    empty_surf = FONT_MAIN.render(get_text(self.gs.language, "empty"), True, (100, 110, 105))
                    self.screen.blit(empty_surf, (r.centerx - empty_surf.get_width() // 2, r.centery))

            self.back_btn_rect = pygame.Rect(100, 610, 260, 45)
            pygame.draw.rect(self.screen, (25, 15, 15), self.back_btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_DANGER, self.back_btn_rect, 2, border_radius=8)
            b_text = FONT_MAIN.render(get_text(self.gs.language, "back"), True, COLOR_TEXT)
            self.screen.blit(b_text, (self.back_btn_rect.centerx - b_text.get_width() // 2, self.back_btn_rect.centery - b_text.get_height() // 2))

        else:
            render_top_hud(self.screen, self.gs.stats, self.gs.turns_counter, self.gs.language)
            render_side_economy(self.screen, self.gs.resources, self.gs.language)
            if self.gs.state not in ('INTRO_1', 'INTRO_2', 'INTRO_3'):
                render_anomaly_radial(self.screen, self.gs.reality_stability, self.gs.language)

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
            
            prompt_surf = FONT_SMALL.render(get_text(self.gs.language, "continue_prompt"), True, COLOR_ACCENT)
            self.screen.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, SCREEN_HEIGHT - 45))
            
        elif self.gs.state == 'PLAYING':
            card_draw_rect = pygame.Rect(self.gs.card_current_x, self.gs.card_rect.y, self.gs.card_rect.width, self.gs.card_rect.height)
            if self.gs.card_animation_active:
                card_draw_rect.y = self.gs.card_anim_y
            
            card_surf = pygame.Surface((card_draw_rect.width, card_draw_rect.height), pygame.SRCALPHA)
            card_bg_color = (COLOR_CARD_BG[0], COLOR_CARD_BG[1], COLOR_CARD_BG[2], self.gs.card_fade_alpha)
            
            active_card = self.gs.final_revolution_card if (self.gs.revolution_active and self.gs.revolution_timer <= 0) else (self.gs.revolution_card if self.gs.revolution_active else self.gs.card_data)
            border_color = COLOR_DANGER if active_card.get("critical", False) else (90, 110, 95)
            
            pygame.draw.rect(card_surf, card_bg_color, card_surf.get_rect(), border_radius=12)
            pygame.draw.rect(card_surf, (*border_color, self.gs.card_fade_alpha), card_surf.get_rect(), 3, border_radius=12)
            pygame.draw.rect(card_surf, (50, 65, 55, self.gs.card_fade_alpha), card_surf.get_rect().inflate(-8, -8), 1, border_radius=10)
            pygame.draw.rect(card_surf, (110, 135, 115, self.gs.card_fade_alpha), card_surf.get_rect().inflate(-16, -16), 1, border_radius=8)
            
            max_title_width = card_draw_rect.width - 60
            if self.gs.card_animation_active:
                title_chars = min(self.gs.card_text_char_index, len(active_card["title"]))
                desc_chars = max(0, self.gs.card_text_char_index - len(active_card["title"]))
            else:
                title_chars = len(active_card["title"])
                desc_chars = len(active_card["desc"])
            title_y = render_wrapped_text(
                card_surf,
                active_card["title"][:title_chars],
                FONT_TITLE,
                (225, 235, 228),
                (30, 25),
                max_title_width,
                30,
                self.gs.card_fade_alpha,
            )
            render_wrapped_text(
                card_surf,
                active_card["desc"][:desc_chars],
                FONT_MAIN,
                (190, 210, 195),
                (30, title_y + 15),
                max_title_width,
                24,
                self.gs.card_fade_alpha,
            )
            
            self.screen.blit(card_surf, card_draw_rect.topleft)
            
            offset_delta = self.gs.card_current_x - self.gs.card_rect.x
            if not self.gs.card_animation_active and offset_delta < -35:
                preview_surf = FONT_MAIN.render(active_card["left_preview"], True, COLOR_DANGER)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((25, 12, 12, 240))
                pygame.draw.rect(bg_surf, COLOR_DANGER, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (60, SCREEN_HEIGHT - 100))
                
            elif not self.gs.card_animation_active and offset_delta > 35:
                preview_surf = FONT_MAIN.render(active_card["right_preview"], True, COLOR_ACCENT)
                bg_surf = pygame.Surface((preview_surf.get_width() + 24, preview_surf.get_height() + 14), pygame.SRCALPHA)
                bg_surf.fill((12, 25, 16, 240))
                pygame.draw.rect(bg_surf, COLOR_ACCENT, bg_surf.get_rect(), 2, border_radius=4)
                bg_surf.blit(preview_surf, (12, 7))
                self.screen.blit(bg_surf, (SCREEN_WIDTH - bg_surf.get_width() - 60, SCREEN_HEIGHT - 100))

        if self.gs.game_over_phase is not None:
            fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_overlay.fill(COLOR_BLACK)
            fade_overlay.set_alpha(round(self.gs.game_over_alpha))
            self.screen.blit(fade_overlay, (0, 0))
            
            if self.gs.game_over_phase == 'HOLD':
                defeat_surf = FONT_TITLE.render(get_text(self.gs.language, "game_over"), True, COLOR_DANGER)
                defeat_rect = defeat_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(defeat_surf, defeat_rect)

        if self.gs.menu_alpha > 0 and self.gs.state == 'MENU':
            menu_fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            menu_fade.fill(COLOR_BLACK)
            menu_fade.set_alpha(self.gs.menu_alpha)
            self.screen.blit(menu_fade, (0, 0))

        if self.gs.intro_alpha > 0 and self.gs.state not in ('GAME_OVER', 'MENU', 'LOAD_MENU'):
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill(COLOR_BLACK)
            fade_surf.set_alpha(self.gs.intro_alpha)
            self.screen.blit(fade_surf, (0, 0))

        pygame.display.flip()

if __name__ == "__main__":
    game: Game = Game()
    game.run()