import math
import pygame
from config import *
from localization import get_text

_gradient_cache = None
_gradient_cache_bucket = None


def render_wrapped_text(surface, text, font, color, position, max_width, line_height, alpha=255):
    x, y = position
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            y += line_height
            continue

        line = ""
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if line and font.size(candidate)[0] > max_width:
                text_surface = font.render(line, True, color)
                text_surface.set_alpha(alpha)
                surface.blit(text_surface, (x, y))
                y += line_height
                line = word
            else:
                line = candidate

        text_surface = font.render(line, True, color)
        text_surface.set_alpha(alpha)
        surface.blit(text_surface, (x, y))
        y += line_height

    return y


def render_unaffordable_glow(screen, direction):
    glow_size = 240
    glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
    center = (0, glow_size) if direction == "LEFT" else (glow_size, glow_size)

    for radius, alpha in ((150, 5), (125, 7), (100, 10), (75, 14), (50, 19), (25, 24)):
        pygame.draw.circle(glow, (*COLOR_DANGER, alpha), center, radius)

    x = 0 if direction == "LEFT" else SCREEN_WIDTH - glow_size
    screen.blit(glow, (x, SCREEN_HEIGHT - glow_size))


def render_top_hud(screen, stats, turns_counter, language):
    panel_width = 1120
    panel_height = 65
    panel_x = 20
    panel_y = 15
    
    hud_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    hud_surf.fill((12, 18, 14, 245))
    pygame.draw.rect(hud_surf, (80, 110, 90), hud_surf.get_rect(), 2, border_radius=8)
    
    x_offset = 15
    bar_width = 110
    bar_height = 10
    stat_labels = get_text(language, "stats")
    
    for stat_name, data in stats.items():
        val = data["val"]
        color = data["color"]
        
        lines = stat_labels[stat_name].split('\n')
        line_y = 8
        for line in lines:
            label_surf = FONT_HUD.render(line, True, color)
            hud_surf.blit(label_surf, (x_offset, line_y))
            line_y += 14
            
        bar_x = x_offset
        bar_y = 38
        pygame.draw.rect(hud_surf, (25, 35, 28), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
        
        fill_w = int((val / 100.0) * bar_width)
        fill_color = color if val > 30 else COLOR_DANGER
        if fill_w > 0:
            pygame.draw.rect(hud_surf, fill_color, (bar_x, bar_y, fill_w, bar_height), border_radius=3)
        
        val_surf = FONT_HUD.render(f"{val}%", True, COLOR_TEXT)
        hud_surf.blit(val_surf, (bar_x + bar_width + 6, bar_y - 2))
        
        x_offset += 190

    # Отрисовка счетчика ходов в правой части панели HUD
    turn_label = FONT_HUD.render(get_text(language, "turn"), True, COLOR_WARNING)
    hud_surf.blit(turn_label, (x_offset + 5, 8))
    turn_val = FONT_TITLE.render(str(turns_counter), True, COLOR_TEXT)
    hud_surf.blit(turn_val, (x_offset + 5, 26))
        
    screen.blit(hud_surf, (panel_x, panel_y))

def render_side_economy(screen, resources, language):
    panel_width = 200
    panel_height = 110
    panel_x = SCREEN_WIDTH - 220
    panel_y = 15
    
    econ_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    econ_surf.fill((15, 20, 16, 245))
    pygame.draw.rect(econ_surf, (150, 130, 50), econ_surf.get_rect(), 2, border_radius=8)
    
    title_surf = FONT_SMALL.render(get_text(language, "resources"), True, COLOR_WARNING)
    econ_surf.blit(title_surf, (15, 12))
    
    y_pos = 42
    resource_names = get_text(language, "resource_names")
    for res_name, res_val in resources.items():
        res_surf = FONT_HUD.render(f"• {resource_names[res_name]}: {res_val}", True, COLOR_TEXT)
        econ_surf.blit(res_surf, (15, y_pos))
        y_pos += 26
        
    screen.blit(econ_surf, (panel_x, panel_y))

def render_anomaly_radial(screen, stability_val, language):
    panel_width = 200
    panel_height = 150
    panel_x = SCREEN_WIDTH - 220
    panel_y = SCREEN_HEIGHT - 165
    
    anom_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    anom_surf.fill((12, 20, 24, 245))
    pygame.draw.rect(anom_surf, (60, 150, 170), anom_surf.get_rect(), 2, border_radius=8)
    
    title_surf = FONT_HUD.render(get_text(language, "reality"), True, COLOR_ANOMALY)
    anom_surf.blit(title_surf, (10, 10))
    
    center_x = panel_width // 2
    center_y = 85
    radius = 36
    thickness = 8
    
    pygame.draw.circle(anom_surf, (20, 35, 40), (center_x, center_y), radius, thickness)
    
    angle_span = (stability_val / 100.0) * 360
    steps = int(angle_span)
    
    for i in range(steps):
        angle_deg = -90 + i
        angle_rad = math.radians(angle_deg)
        
        ratio = i / 360.0
        r = int(40 + ratio * 20)
        g = int(140 + ratio * 70)
        b = int(180 + ratio * 55)
        grad_color = (r, g, b)
        
        x1 = center_x + int((radius - thickness / 2) * math.cos(angle_rad))
        y1 = center_y + int((radius - thickness / 2) * math.sin(angle_rad))
        x2 = center_x + int((radius + thickness / 2) * math.cos(angle_rad))
        y2 = center_y + int((radius + thickness / 2) * math.sin(angle_rad))
        pygame.draw.line(anom_surf, grad_color, (x1, y1), (x2, y2), 2)
        
    val_surf = FONT_TITLE.render(f"{stability_val}%", True, COLOR_TEXT)
    val_rect = val_surf.get_rect(center=(center_x, center_y))
    anom_surf.blit(val_surf, val_rect)
    
    screen.blit(anom_surf, (panel_x, panel_y))

def render_gradient_background(screen, tick):
    global _gradient_cache, _gradient_cache_bucket

    update_bucket = tick // 5
    if _gradient_cache is None or update_bucket != _gradient_cache_bucket:
        if _gradient_cache is None:
            _gradient_cache = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        phase = update_bucket * 5 * 0.02
        for y in range(SCREEN_HEIGHT):
            factor = (math.sin(phase + y * 0.005) + 1) / 2
            color = (
                int(6 + factor * 8),
                int(14 + factor * 16),
                int(10 + factor * 10),
            )
            pygame.draw.line(_gradient_cache, color, (0, y), (SCREEN_WIDTH, y))
        _gradient_cache_bucket = update_bucket

    screen.blit(_gradient_cache, (0, 0))