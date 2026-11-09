"""Russian and English strings used throughout the game."""

import json
from pathlib import Path


LANGUAGES = ("ru", "en")
DEFAULT_LANGUAGE = "ru"
SETTINGS_PATH = Path(__file__).with_name("settings.json")

TEXT = {
    "ru": {
        "language_button": "ЯЗЫК: РУССКИЙ",
        "menu_start": "ПРОДОЛЖИТЬ / ИГРАТЬ",
        "menu_saves": "СОХРАНЕНИЯ",
        "menu_exit": "ВЫЙТИ",
        "saves_title": "ЯЧЕЙКИ СОХРАНЕНИЙ",
        "autosave": "АВТОСОХРАНЕНИЕ",
        "autosave_saved": "Сохранено (Авто)",
        "slot": "Слот",
        "occupied": "Занято",
        "empty": "пусто",
        "back": "НАЗАД В МЕНЮ",
        "turn": "ХОД",
        "resources": "РЕСУРСЫ СЕКТОРА",
        "reality": "СТАБИЛЬНОСТЬ РЕАЛЬНОСТИ",
        "continue_prompt": "[ Нажмите SPACE для ускорения / продолжения ]",
        "game_over": "ПОРАЖЕНИЕ",
        "nothing_happened": "Ничего не произошло",
        "stats": {
            "faith": "ВЕРА ЛЮДЕЙ",
            "army": "СИЛА АРМИИ",
            "habitability": "ЖИЗНЕПРИГОДНОСТЬ",
            "political": "ПОЛИТ. СТАБ.",
            "order": "ПОРЯДОК",
        },
        "resource_names": {"matter": "Материя", "energy": "Энергия"},
        "effect_names": {
            "faith": "Вера людей",
            "hab": "Жизнепригодность",
            "order": "Порядок",
            "reality": "Стаб. реальности",
            "matter": "Материя",
            "energy": "Энергия",
            "army": "Сила армии",
        },
        "intro": [
            "Идет 156 год после Инсуффляции...\n"
            "Старый мир сжат, скомкан и сплавлен в бесконечный многослойный лабиринт.\n"
            "Нет неба и земли — только бетон, ржавые трубы и гул вентиляции.",
            "Ты — правитель изолированного сектора-укрытия.\n"
            "Твоя задача — балансировать на грани гибели, принимать тяжелые кризисные решения\n"
            "и вести людей через постоянную угрозу пространственных разломов, удушья и бунтов.",
            "Вы просыпаетесь за своим рабочим столом...\n"
            "Лампа мерцает в такт уставшему гулу генераторов.\n"
            "Секретарь кладет на стол первые донесения. Время принимать решения.",
        ],
        "cards": [
            {
                "title": "УГРОЗА ВОЗДУШНОГО ФИЛЬТРА",
                "desc": "Начальник нижнего технического цеха докладывает о критическом износе турбин. Без ремонта уровень удушья в жилых блоках возрастет.",
                "left_preview": "ОТКАЗАТЬ: Вероятно, упадет Вера людей; возможно, пошатнется Порядок.",
                "right_preview": "ВЫДЕЛИТЬ ДЕТАЛИ: Есть риск истощить Материю, но поднимется Жизнепригодность.",
                "left_result": "Вы отказали техникам ради экономии. Густой туман заполняет нижние уровни, вызывая глухой ропот.",
                "right_result": "Запасные детали доставлены в цех. Турбины взревели новыми оборотами, очищая воздух.",
            },
            {
                "title": "ПРОРЫВ АНОМАЛИИ В СЕКТОРЕ С",
                "desc": "Датчики фиксируют искажение пространственной сетки за перегородкой жилого блока. Законы физики деформируются.",
                "left_preview": "УЦЕПИТЬСЯ: Стабильность реальности может вырасти, но Энергия имеет вероятность упасть.",
                "right_preview": "ЗАБЕТОНИРОВАТЬ: Порядок может подняться, но Вера людей и Реальность могут пострадать.",
                "left_result": "Защитные контуры удержали разлом ценой скачка энергопотребления в сетях.",
                "right_result": "Автоматические бетононасосы залили отсек за считанные минуты. Крики затихли под монолитом.",
            },
            {
                "title": "УТЕЧКА РАДИОАКТИВНЫХ ОТХОДОВ",
                "desc": "Вентиляционные фильтры сектора Б забились шлаком. Датчики фиксируют ползущее радиационное заражение жилых отсеков.",
                "left_preview": "ИГНОРИРОВАТЬ: Вера людей упадет, а Жизнепригодность ухудшится.",
                "right_preview": "ПРОМЫВКА СИСТЕМЫ: Потратить 20 Энергии, но очистить воздух.",
                "left_result": "Вы решили не тратить ресурсы. Люди задыхаются в кашле, проклиная администрацию в темноте.",
                "right_result": "Инженеры провели экстренную химическую промывку контуров. Радиационный фон пришел в норму.",
            },
            {
                "title": "КОНТРАБАНДА НА ЧЕРНОМ РЫНКЕ",
                "desc": "Служба безопасности перехватила партию нелегальных энергоячеек, украденных из распределителя верхнего уровня.",
                "left_preview": "ИЗЪЯТЬ В КАЗНУ: Порядок поднимется, но Вера людей немного пошатнется от жестких мер.",
                "right_preview": "ПОДЕЛИТЬСЯ С НАРОДОМ: Вера вырастет, но казна потеряет ценные ресурсы.",
                "left_result": "Энергоячейки возвращены на государственные склады. Дисциплина в секторе укреплена.",
                "right_result": "Вы распределили блоки по жилым блокам. Люди рады теплу, но запасы энергии истощены.",
            },
            {
                "title": "ЗАТМЕНИЕ ИСКУССТВЕННОГО СОЛНЦА",
                "desc": "Главный люминофорный излучатель сектора перешел в аварийный режим. Нижние уровни погрузились в кромешную тьму и панику.",
                "left_preview": "РЕМОНТ В ТЕМНОТЕ: Упадет Жизнепригодность и Порядок из-за паники.",
                "right_preview": "ВКЛЮЧИТЬ РЕЗЕРВ: Потратить 25 Энергии на мгновенный запуск подсветки.",
                "left_result": "Ремонт затянулся на сутки. Во тьме вспыхнули стихийные потасовки и грабежи.",
                "right_result": "Резервные генераторы залили улицы искусственным бледным светом. Паника мгновенно улетучилась.",
            },
        ],
        "revolution": {
            "title": "ВОССТАНИЕ В НИЖНИХ УРОВНЯХ",
            "desc": "Народный гнев прорвал блокаду секторов! Толпы с арматурой идут штурмовать административный уровень. Требуется срочно бросить в бой армию и задействовать резервы казны!",
            "left_preview": "СДАТЬ ПОСТЫ: Полный коллапс власти и гибель сектора.",
            "right_preview": "ПОДАВИТЬ БУНТ: Потратить 100 Материи и 30 Энергии для жесткого подавления.",
            "left_result": "Толпы ворвались в кабинет. Ваше правление пало в огне всеобщего хаоса.",
            "right_result": "Армия жестоко подавила восстание на улицах. Порядок восстановлен, но сектор в крови.",
        },
        "final_revolution": {
            "title": "ФИНАЛЬНЫЙ ШТУРМ ЦИТАДЕЛИ",
            "desc": "Прошло 9 ходов после подавления бунта, но народное отчаяние достигло предела. Вера на нуле. Толпы пробивают гермоворота без шанса на переговоры.",
            "left_preview": "ПРИНЯТЬ НЕИЗБЕЖНОЕ: Сдать сектор.",
            "right_preview": "ПОПЫТАТЬСЯ УБЕЖАТЬ: Бесполезно.",
            "left_result": "Гермозатворы рухнули под ударами тарана. Ваше правление окончено навсегда.",
            "right_result": "Вас настигли в пустых коридорах бункера.",
        },
    },
    "en": {
        "language_button": "LANGUAGE: ENGLISH",
        "menu_start": "CONTINUE / PLAY",
        "menu_saves": "SAVED GAMES",
        "menu_exit": "EXIT",
        "saves_title": "SAVE SLOTS",
        "autosave": "AUTOSAVE",
        "autosave_saved": "Autosaved",
        "slot": "Slot",
        "occupied": "Occupied",
        "empty": "Empty",
        "back": "BACK TO MENU",
        "turn": "TURN",
        "resources": "SECTOR RESOURCES",
        "reality": "REALITY STABILITY",
        "continue_prompt": "[ Press SPACE to speed up / continue ]",
        "game_over": "DEFEAT",
        "nothing_happened": "Nothing happened",
        "stats": {
            "faith": "HUMAN FAITH",
            "army": "MILITARY POWER",
            "habitability": "HABITABILITY",
            "political": "POLITICAL STAB.",
            "order": "PUBLIC ORDER",
        },
        "resource_names": {"matter": "Matter", "energy": "Energy"},
        "effect_names": {
            "faith": "Human faith",
            "hab": "Habitability",
            "order": "Public order",
            "reality": "Reality stability",
            "matter": "Matter",
            "energy": "Energy",
            "army": "Military power",
        },
        "intro": [
            "Year 156 after the Insufflation...\n"
            "The old world was crushed, folded, and fused into an endless, layered maze.\n"
            "There is no sky or ground — only concrete, rusted pipes, and the hum of ventilation.",
            "You rule an isolated shelter-sector.\n"
            "Your task is to balance on the edge of extinction, make brutal crisis decisions,\n"
            "and lead your people through spatial ruptures, suffocation, and revolt.",
            "You wake at your desk...\n"
            "The lamp flickers in time with the generators' weary hum.\n"
            "Your secretary lays the first reports on the table. It is time to decide.",
        ],
        "cards": [
            {
                "title": "AIR FILTER FAILURE",
                "desc": "The lower workshop chief reports critically worn turbines. Without repairs, the residential blocks will begin to suffocate.",
                "left_preview": "REFUSE: Human faith may fall; public order may falter.",
                "right_preview": "ISSUE PARTS: Matter reserves may dwindle, but habitability will improve.",
                "left_result": "You denied the technicians to conserve supplies. Dense fog fills the lower levels as a sullen murmur spreads.",
                "right_result": "Spare parts reach the workshop. The turbines roar back to life, clearing the air.",
            },
            {
                "title": "ANOMALY BREACH IN SECTOR C",
                "desc": "Sensors detect a warped spatial grid behind the residential partition. The laws of physics begin to bend.",
                "left_preview": "HOLD THE LINE: Reality may stabilize, but the power grid may falter.",
                "right_preview": "SEAL IT IN CONCRETE: Order may rise, but faith and reality may suffer.",
                "left_result": "The defense circuits contain the rift, at the cost of a surge in the power grid.",
                "right_result": "Automated pumps fill the compartment with concrete. The screams fade beneath the new monolith.",
            },
            {
                "title": "RADIOACTIVE WASTE LEAK",
                "desc": "Sector B ventilation filters are clogged with sludge. Sensors report a creeping radiation hazard in the residential compartments.",
                "left_preview": "IGNORE: Human faith will fall, and habitability will worsen.",
                "right_preview": "FLUSH SYSTEM: Spend 20 Energy to clear the air.",
                "left_result": "You chose to conserve resources. People cough in the dark, cursing the administration.",
                "right_result": "Engineers performed an emergency chemical flush. Radiation levels have normalized.",
            },
            {
                "title": "BLACK MARKET CONTRABAND",
                "desc": "Security intercepted a batch of illegal power cells stolen from the upper-level distributor.",
                "left_preview": "CONFISCATE: Public order rises, but faith dips slightly due to harsh measures.",
                "right_preview": "SHARE WITH THE PEOPLE: Faith rises, but energy reserves are depleted.",
                "left_result": "Power cells returned to state depots. Sector discipline has been reinforced.",
                "right_result": "You distributed the blocks to the living blocks. People appreciate the warmth, but energy runs low.",
            },
            {
                "title": "ARTIFICIAL SUN ECLIPSE",
                "desc": "The sector's main luminophore emitter entered emergency mode. Lower levels plunged into pitch darkness and panic.",
                "left_preview": "REPAIR IN THE DARK: Habitability and order will drop due to panic.",
                "right_preview": "ENGAGE RESERVES: Spend 25 Energy for an instant illumination startup.",
                "left_result": "Repairs dragged on for a day. Spontaneous brawls and looting broke out in the dark.",
                "right_result": "Backup generators flooded the streets with pale artificial light. Panic instantly vanished.",
            },
        ],
        "revolution": {
            "title": "UPRISING IN THE LOWER LEVELS",
            "desc": "Public rage breaks through the sector blockade! Crowds armed with rebar storm the administrative level. The army and treasury reserves must be committed now!",
            "left_preview": "ABANDON YOUR POSTS: The government collapses and the sector falls.",
            "right_preview": "CRUSH THE REVOLT: Spend 100 Matter and 30 Energy to suppress it by force.",
            "left_result": "The crowd storms your office. Your rule ends in the flames of total chaos.",
            "right_result": "The army brutally suppresses the uprising. Order returns, but the sector is soaked in blood.",
        },
        "final_revolution": {
            "title": "THE FINAL ASSAULT",
            "desc": "Nine turns have passed since the revolt was crushed, but despair has reached its limit. Faith is gone. The crowd breaks through the airlocks; there is no chance to negotiate.",
            "left_preview": "ACCEPT THE INEVITABLE: Surrender the sector.",
            "right_preview": "TRY TO ESCAPE: There is no escape.",
            "left_result": "The airlocks buckle beneath the battering ram. Your rule ends forever.",
            "right_result": "They catch you in the bunker's empty corridors.",
        },
    },
}


def get_text(language, key):
    """Return a translated game string for a supported language."""
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    return TEXT[language][key]


def load_language():
    """Load the selected language, defaulting to Russian before settings exist."""
    try:
        with SETTINGS_PATH.open("r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
    except FileNotFoundError:
        return DEFAULT_LANGUAGE
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid language settings in {SETTINGS_PATH}: {error}") from error

    if not isinstance(settings, dict) or settings.get("language") not in LANGUAGES:
        raise ValueError(f"Language setting in {SETTINGS_PATH} must be 'ru' or 'en'.")
    return settings["language"]


def save_language(language):
    """Persist the selected language for the next game launch."""
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    with SETTINGS_PATH.open("w", encoding="utf-8") as settings_file:
        json.dump({"language": language}, settings_file, ensure_ascii=False, indent=2)