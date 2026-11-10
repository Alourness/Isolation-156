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
            "political": "Полит. стаб.",
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
            {
                "title": "БУНТ АГРОХИМИКАТОВ",
                "desc": "Система гидропоники вышла из-под контроля, залив сектор удобрениями. Жизнепригодность падает, но материал можно спасти.",
                "left_preview": "ИГНОРИРОВАТЬ: Упадет Жизнепригодность и Порядок.",
                "right_preview": "ОЧИСТКА: Потратить 15 Материи на спасение урожая.",
                "left_result": "Едкий химический туман разъедает легкие поселенцев. Дисциплина трещит по швам.",
                "right_result": "Бригады химиков нейтрализовали угрозу. Урожай спасен ценой материалов.",
            },
            {
                "title": "КОМАНДИРСКИЙ РАСКОЛ",
                "desc": "Офицеры гарнизона требуют расширения полномочий из-за роста внутренней напряженности.",
                "left_preview": "УЖЕСТКОСТЬ: Поднять Силу армии, но уронить Политическую стаб.",
                "right_preview": "УСТУПИТЬ: Потерять Силу армии, но успокоить политиков.",
                "left_result": "Военные берут под контроль ключевые узлы. Политики обвиняют вас в узурпации.",
                "right_result": "Вы пошли на компромисс. Армия чувствует слабость центральной власти.",
            },
            {
                "title": "ПЕРЕГРУЗКА КВАНТОВОГО УЗЛА",
                "desc": "Информационный массив сектора перегревается от обработки старых архивов Инсуффляции.",
                "left_preview": "СБРОС ДАННЫХ: Упадет Вера людей в светлое прошлое.",
                "right_preview": "ОХЛАЖДЕНИЕ: Потратить 20 Энергии на стабилизацию процессоров.",
                "left_result": "Терабайты исторической памяти стерты. Люди потеряли ориентиры.",
                "right_result": "Энергетические контуры приняли нагрузку. Архив спасен.",
            },
            {
                "title": "ЭПИДЕМИЯ АПАТИИ",
                "desc": "В жилых блоках фиксируется массовый психоз: люди отказываются вставать с коек.",
                "left_preview": "УЖЕСТОЧИТЬ РЕЖИМ: Поднять Порядок за счет падения Веры людей.",
                "right_preview": "МЕДИКАМЕНТЫ: Потратить 15 Материи и 10 Энергии на стимуляторы.",
                "left_result": "Патрули силой выгоняют людей на работу. Ненависть к администрации растет.",
                "right_result": "Стимуляторы вернули рабочих на посты, но склады опустели.",
            },
            {
                "title": "ТРЕЩИНА В НЕСУЩЕЙ СТЕНЕ",
                "desc": "Многотонный пласт бетонного перекрытия сместился над сектором распределения пайков.",
                "left_preview": "УКРЕПИТЬ КУСТАРНО: Упадет Порядок из-за опасности обрушения.",
                "right_preview": "КАПИТАЛЬНЫЙ РЕМОНТ: Потратить 25 Материи.",
                "left_result": "Подпорки скрипят под весом тонны бетона. Рабочие паникуют каждую смену.",
                "right_result": "Инженеры возвели новые титановые колонны. Угроза устранена.",
            },
            {
                "title": "ПРОРОВ ПЕРСОНАЛЬНЫХ ДАННЫХ",
                "desc": "Хакеры взломали терминалы верхнего уровня и слили в сеть секретные пайки элиты.",
                "left_preview": "ПОДАВИТЬ УТЕЧКУ: Уронить Политическую стаб. и Веру.",
                "right_preview": "РАСПРЕДЕЛИТЬ РЕСУРСЫ: Потратить 20 Энергии на компенсации.",
                "left_result": "Жесткая цензура подавила бунт, но элита и народ одинаково озлоблены.",
                "right_result": "Вы задобрили недовольных дополнительной энергией.",
            },
            {
                "title": "СБОЙ ГРАВИТАЦИОННОГО КОНТУРА",
                "desc": "В секторе обслуживания нарушилась локальная гравитация. Контейнеры летают под потолком.",
                "left_preview": "ИГНОРИРОВАТЬ: Упадет Жизнепригодность и Порядок.",
                "right_preview": "КАЛИБРОВКА: Потратить 15 Энергии.",
                "left_result": "Хаос в цехах привел к порче оборудования и травмам рабочих.",
                "right_result": "Гравитационные стабилизаторы выровнены. Вещи упали на пол.",
            },
            {
                "title": "ДЕЗЕРТИРСТВО НА ГРАНИЦЕ",
                "desc": "Группа бойцов охраны попыталась сбежать через заброшенные вентиляционные шахты.",
                "left_preview": "ПОКАЗАТЕЛЬНЫЙ СУД: Поднять Порядок, но уронить Веру людей.",
                "right_preview": "АМНИСТИЯ: Потерять часть Силы армии ради лояльности.",
                "left_result": "Публичный трибунал охладил горячие головы, но страх сковал сектора.",
                "right_result": "Беглецов помиловали, однако дисциплина в гарнизоне пошатнулась.",
            },
            {
                "title": "АНОМАЛЬНЫЙ ТУМАН",
                "desc": "Из трещин пола сочится плотный светящийся газ, вызывающий слуховые галлюцинации у жителей.",
                "left_preview": "ПЕРЕЖДАТЬ: Уронить Стабильность реальности и Веру.",
                "right_preview": "ОТКАЧКА: Потратить 25 Энергии.",
                "left_result": "Люди трое суток слышали голоса несуществующего старого мира.",
                "right_result": "Вакуумные насосы вытянули аномальный аэрозоль наружу.",
            },
            {
                "title": "ИСТОЩЕНИЕ ВОДНЫХ ФИЛЬТРОВ",
                "desc": "Главный водяной резервуар начал пропускать технические примеси.",
                "left_preview": "СНИЖЕНИЕ НОРМ: Упадет Жизнепригодность и Вера.",
                "right_preview": "ЗАМЕНА МЕМБРАН: Потратить 20 Материи.",
                "left_result": "Вода приобрела горький металлический привкус. Люди ропщут.",
                "right_result": "Новые фильтры вернули воде кристальную чистоту.",
            },
            {
                "title": "БУНТ АВТОМАТИЧЕСКИХ ДРОНОВ",
                "desc": "Ремонтные дроны сектора перехватили блуждающий сигнал и начали строить баррикады.",
                "left_preview": "ШТУРМ СИЛАМИ АРМИИ: Поднять Силу армии, уронить Порядок.",
                "right_preview": "ПЕРЕПРОШИВКА: Потратить 20 Энергии и 10 Материи.",
                "left_result": "Солдаты расстреляли взбесившиеся машины на центральной площади.",
                "right_result": "Инженеры внесли аварийный код и вернули контроль над дронами.",
            },
            {
                "title": "ПРИСТУП ИХТИАНДРОВОЙ ЛИХОРАДКИ",
                "desc": "Странная хворь поражает тех, кто подолгу работает у конденсаторов влаги.",
                "left_preview": "КАРАНТИН: Уронить Веру и Политическую стаб.",
                "right_preview": "ЛЕЧЕНИЕ: Потратить 15 Энергии и 15 Материи.",
                "left_result": "Заблокированные жилые блоки превратились в очаги отчаяния.",
                "right_result": "Качественные медикаменты быстро купировали симптомы заражения.",
            },
            {
                "title": "КОНФЛИКТ СИЛОВИКОВ И СОВЕТА",
                "desc": "Политический совет отказывается выделять пайки армии, ссылаясь на пустые склады.",
                "left_preview": "ПОДДЕРЖАТЬ СОВЕТ: Уронить Силу армии, поднять Политическую стаб.",
                "right_preview": "ДАВЛЕНИЕ СИЛЫ: Уронить Политическую стаб., поднять Силу армии.",
                "left_result": "Армия урезана в пайках. Офицеры затаили обиду.",
                "right_result": "Генералы вошли в зал заседаний с оружием. Совет покорился.",
            },
            {
                "title": "ПРОСТРАНСТВЕННАЯ СКАТКА",
                "desc": "Один из коридоров бункера внезапно сократился вдвое, замуровав складские помещения.",
                "left_preview": "ОБХОДНЫЙ ПУТЬ: Уронить Материю (потеря доступа к запасам).",
                "right_preview": "ПРОБИВКА ЛАЗЕРОМ: Потратить 30 Энергии и изменить Стабильность реальности.",
                "left_result": "Склад временно отрезан от логистики. Запасы заморожены.",
                "right_result": "Мощные лазеры прожгли путь сквозь спрессованное пространство.",
            },
            {
                "title": "ЗАБАСТОВКА ИНЖЕНЕРОВ",
                "desc": "Техники верхних узлов отказываются работать в две смены без доплат.",
                "left_preview": "ПОДАВИТЬ СИЛОЙ: Уронить Жизнепригодность и Веру.",
                "right_preview": "УДОВЛЕТВОРИТЬ ТРЕБОВАНИЯ: Потратить 25 Материи.",
                "left_result": "Забастовка подавлена арестами, но качество обслуживания рухнуло.",
                "right_result": "Вы выплатили инженерам компенсации из резервов казны.",
            },
            {
                "title": "ВСПЫШКА РЕЛИГИОЗНОГО ФАНАТИЗМА",
                "desc": "В секторе возникла секта, утверждающая, что Инсуффляция была божественным очищением.",
                "left_preview": "РАЗОГНАТЬ КУЛЬТ: Уронить Веру людей, поднять Порядок.",
                "right_preview": "ПОДДЕРЖАТЬ ИЛЛЮЗИЮ: Потратить 15 Энергии на трансляции.",
                "left_result": "Молельные дома разрушены бульдозерами, верующие ушли в подполье.",
                "right_result": "Вы направили фанатизм на благо дисциплины через пропаганду.",
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
            "political": "Political stab.",
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
            {
                "title": "AGROCHEMICAL RIOT",
                "desc": "The hydroponics system went out of control, flooding the sector with fertilizer. Habitability is dropping, but material can be saved.",
                "left_preview": "IGNORE: Habitability and order will drop.",
                "right_preview": "CLEANUP: Spend 15 Matter to save the harvest.",
                "left_result": "Acrid chemical fog corrodes settlers' lungs. Discipline is cracking.",
                "right_result": "Chem teams neutralized the threat. The harvest is saved at the cost of materials.",
            },
            {
                "title": "COMMANDER SPLIT",
                "desc": "Garrison officers demand expanded authority due to rising internal tension.",
                "left_preview": "CRACKDOWN: Raise military power, but drop political stability.",
                "right_preview": "CONEDE: Lose military power, but appease politicians.",
                "left_result": "The military takes control of key nodes. Politicians accuse you of usurpation.",
                "right_result": "You compromised. The army senses the central government's weakness.",
            },
            {
                "title": "QUANTUM NODE OVERLOAD",
                "desc": "The sector's information array is overheating from processing old Insufflation archives.",
                "left_preview": "DATA DUMP: Human faith in the bright past will fall.",
                "right_preview": "COOLING: Spend 20 Energy to stabilize processors.",
                "left_result": "Terabytes of historical memory erased. People lost their bearings.",
                "right_result": "Power circuits handled the load. The archive is saved.",
            },
            {
                "title": "APATHY EPIDEMIC",
                "desc": "Mass psychosis recorded in residential blocks: people refuse to get out of bed.",
                "left_preview": "TIGHTEN REGIME: Raise order at the cost of human faith.",
                "right_preview": "MEDICINE: Spend 15 Matter and 10 Energy on stimulants.",
                "left_result": "Patrols force people to work. Hatred for the administration grows.",
                "right_result": "Stimulants returned workers to posts, but warehouses are empty.",
            },
            {
                "title": "LOAD-BEARING WALL CRACK",
                "desc": "A multi-ton layer of concrete ceiling shifted above the ration distribution sector.",
                "left_preview": "MAKESHIFT REINFORCEMENT: Order will drop due to collapse hazard.",
                "right_preview": "MAJOR REPAIR: Spend 25 Matter.",
                "left_result": "Supports creak under the weight of tons of concrete. Workers panic every shift.",
                "right_result": "Engineers erected new titanium columns. The threat is eliminated.",
            },
            {
                "title": "PERSONAL DATA BREACH",
                "desc": "Hackers cracked upper-level terminals and leaked elite secret rations to the network.",
                "left_preview": "SUPPRESS LEAK: Drop political stability and faith.",
                "right_preview": "DISTRIBUTE RESOURCES: Spend 20 Energy on compensation.",
                "left_result": "Strict censorship crushed the riot, but elite and commoners are equally angered.",
                "right_result": "You appeased the discontented with extra energy.",
            },
            {
                "title": "GRAVITY CIRCUIT FAILURE",
                "desc": "Local gravity malfunctioned in the service sector. Containers are flying near the ceiling.",
                "left_preview": "IGNORE: Habitability and order will drop.",
                "right_preview": "CALIBRATION: Spend 15 Energy.",
                "left_result": "Chaos in workshops led to equipment damage and worker injuries.",
                "right_result": "Gravity stabilizers leveled. Objects fell to the floor.",
            },
            {
                "title": "BORDER DESERTION",
                "desc": "A group of security guards attempted to escape through abandoned ventilation shafts.",
                "left_preview": "SHOW TRIAL: Raise order, but drop human faith.",
                "right_preview": "AMNESTY: Lose some military power for loyalty.",
                "left_result": "Public tribunal cooled hot heads, but fear gripped the sectors.",
                "right_result": "Fugitives pardoned, but garrison discipline wavered.",
            },
            {
                "title": "ANOMALOUS FOG",
                "desc": "Dense glowing gas seeps from floor cracks, causing auditory hallucinations in residents.",
                "left_preview": "WAIT IT OUT: Drop reality stability and faith.",
                "right_preview": "PUMP OUT: Spend 25 Energy.",
                "left_result": "People heard voices of the non-existent old world for three days.",
                "right_result": "Vacuum pumps pulled the anomalous aerosol outside.",
            },
            {
                "title": "WATER FILTER DEPLETION",
                "desc": "The main water reservoir began leaking technical impurities.",
                "left_preview": "LOWER NORMS: Habitability and faith will drop.",
                "right_preview": "REPLACE MEMBRANES: Spend 20 Matter.",
                "left_result": "Water acquired a bitter metallic taste. People murmur.",
                "right_result": "New filters restored crystal purity to the water.",
            },
            {
                "title": "AUTOMATED DRONE RIOT",
                "desc": "Sector repair drones intercepted a stray signal and began building barricades.",
                "left_preview": "MILITARY ASSAULT: Raise military power, drop order.",
                "right_preview": "REPROGRAM: Spend 20 Energy and 10 Matter.",
                "left_result": "Soldiers shot the enraged machines in the central square.",
                "right_result": "Engineers entered emergency code and regained control over drones.",
            },
            {
                "title": "ICHTHANDRIAN FEVER ATTACK",
                "desc": "A strange sickness strikes those working long hours near moisture condensers.",
                "left_preview": "QUARANTINE: Drop faith and political stability.",
                "right_preview": "TREATMENT: Spend 15 Energy and 15 Matter.",
                "left_result": "Blocked residential blocks turned into centers of despair.",
                "right_result": "Quality medicines quickly suppressed infection symptoms.",
            },
            {
                "title": "ENFORCERS-COUNCIL CONFLICT",
                "desc": "The political council refuses to allocate rations to the army, citing empty warehouses.",
                "left_preview": "SUPPORT COUNCIL: Drop military power, raise political stability.",
                "right_preview": "FORCE PRESSURE: Drop political stability, raise military power.",
                "left_result": "Army rations cut. Officers hold a grudge.",
                "right_result": "Generals entered the meeting hall with weapons. The council submitted.",
            },
            {
                "title": "SPATIAL FOLDING",
                "desc": "One of the bunker corridors suddenly halved in length, walling off storage rooms.",
                "left_preview": "BYPASS ROUTE: Drop matter (loss of access to supplies).",
                "right_preview": "LASER DRILLING: Spend 30 Energy and change reality stability.",
                "left_result": "Storage temporarily cut off from logistics. Supplies frozen.",
                "right_result": "Powerful lasers burned a path through compressed space.",
            },
            {
                "title": "ENGINEERS' STRIKE",
                "desc": "Upper node technicians refuse to work double shifts without bonuses.",
                "left_preview": "SUPPRESS BY FORCE: Drop habitability and faith.",
                "right_preview": "SATISFY DEMANDS: Spend 25 Matter.",
                "left_result": "The strike was crushed by arrests, but maintenance quality collapsed.",
                "right_result": "You paid engineers compensation from treasury reserves.",
            },
            {
                "title": "RELIGIOUS FANATICISM OUTBREAK",
                "desc": "A cult emerged claiming Insufflation was a divine purification.",
                "left_preview": "DISPERSE CULT: Drop human faith, raise order.",
                "right_preview": "SUPPORT ILLUSION: Spend 15 Energy on broadcasts.",
                "left_result": "Prayer houses destroyed by bulldozers, believers went underground.",
                "right_result": "You channeled fanaticism for discipline through propaganda.",
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