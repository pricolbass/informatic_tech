class Location:
    def __init__(self, name, description, actions=None):
        self.name = name
        self.description = description
        self.actions = actions or []

    def add_action(self, action):
        self.actions.append(action)


class Action:
    def __init__(self, name, result, required_items=None, next_location=None, reward_items=None):
        self.name = name
        self.result = result
        self.required_items = required_items or []
        self.reward_items = reward_items or []
        self.next_location = next_location


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class DetectiveGame:
    def __init__(self):
        self.locations = {}
        self.current_location = None
        self.inventory = []

    def add_location(self, location):
        self.locations[location.name] = location

    def start_game(self):
        print("Добро пожаловать в детективную игру!")
        self.current_location = self.locations["начальная локация"]
        self.play()

    def play(self):
        while True:
            print("\nВы находитесь в", self.current_location.name)
            print(self.current_location.description)
            print("Доступные действия:")
            for i, action in enumerate(self.current_location.actions):
                print(f"{i + 1}. {action.name}")

            choice = input("Выберите номер действия (или 'выход' для завершения игры): ").lower()

            if choice == 'выход':
                print("\033[3mИгра завершена.\033[0m")
                break

            try:
                choice = int(choice) - 1
                selected_action = self.current_location.actions[choice]

                # Проверяем, есть ли необходимые предметы для выполнения действия. Также проверяем на победу и на проигрыш
                if not selected_action.required_items or all(
                        item.name in [i.name for i in self.inventory] for item in selected_action.required_items):
                    print(selected_action.result)

                    if selected_action.next_location == "конец игры (победа)":  # Проверяем, если это локация победы
                        print(
                            "\033[3mПоздравляем! Вы разгадали преступление и поймали преступника. Игра завершена, "
                            "но точно ли это конец?\033[0m")
                        break  # Завершаем игровой цикл
                    elif selected_action.next_location == "конец игры (вы не смогли разгадать данное дело)":  # Проверяем, если это локация проигрыша
                        print(
                            '\033[3mВас убил подозреваемый и вы не смогли вывести его на чистую воду. Игра '
                            'завершена.\033[0m')
                        break  # Завершаем игровой цикл
                    else:
                        # Добавляем награду (предметы) в инвентарь игрока
                        if selected_action.reward_items:
                            self.inventory.extend(selected_action.reward_items)

                        self.current_location = self.locations[selected_action.next_location]
                else:
                    print("\033[3mВам не хватает необходимых предметов для выполнения этого действия.\033[0m")

            except (ValueError, IndexError):
                print("\033[3mПожалуйста, выберите действие из списка.\033[0m")


# Создаем локации
starting_location = Location(
    "начальная локация",
    "\033[1mВы находитесь в баре, в котором стоит группа людей, одетых по последнему пику моды 18 века.\nВсе удивлены "
    "смерти убитого, но также все очень сильно напуганны, так как это уже не первый случай убийства в этом районе за "
    "такой короткий период времени.\nРазглядывая немного помещение, ваш взгляд бросается на мужчину во фраке.\nВаша "
    "чуйка подсказывает, что он что-то знает о произошедшем, может быть нужно с ним поговорить?\033[0m"
)

basement = Location(
    "подвал",
    "\033[1mВы спустились в мрачный подвал.\nВы понимаете по толстому слою пыли, что никто сюда не спускается"
    "\nИдеальное место для убежища убийцы.\033[0m"
)

outside = Location(
    "улица",
    "\033[1mВы вышли на улицу, заполненную звездами, но вас они не интересуют.\033[0m"
)

rooftop = Location(
    "крыша",
    "\033[1mВы находитесь на крыше здания, ветер свистит вокруг вас.\033[0m"
)

secret_hideout = Location(
    "тайное укрытие",
    "\033[1mВы нашли тайное укрытие преступника.\nВы чувствуете зловещую ауру в этом помещении\033[0m"
)

# Создаем действия
investigate_closet = Action(
    "посмотреть в шкаф",
    "\033[1mВы осматриваете шкаф и обнаруживаете фонарик, который мог бы пригодиться вам в дальнейшем "
    "расследования.\033[0m",
    required_items=None,
    reward_items=[Item("фонарик", "Светящийся фонарик.")],
    next_location="начальная локация"
)

talk_to_witness = Action(
    "поговорить со свидетелем",
    "\033[1mВы беседуете со свидетелем, он рассказывает вам, что видел странного мужчину, убегающего с места "
    "преступления.\nОн описывает мужчину как высокого с характерном шрамом на лице.\033[0m",
    required_items=None,
    next_location="начальная локация"
)

go_to_basement = Action(
    "пойти в подвал",
    "\033[1mВы спускаетесь в подвал, и ваши шаги стихают в мрачной темноте.\nВы еле видете старые ящики и запыленные"
    " полки.\nВ углу помещения стоит забытая лестница, ведущая во тьму, которая могла бы вам пригодиться.\033[0m",
    required_items=None,
    reward_items=None,
    next_location="подвал"
)

lead_staircase = Action(
    "посмотреть куда ведёт лестница",
    "\033[1mВы спускаетесь по лестнице, ведущей во тьму.\nКак только вы оказывается во тьме, вы включаете фонарик и "
    "видете пустую комнату, по стенам которой развешанны фотографии всех убийств.\nТакже вы видете несколько писем на "
    "столе, но не успев дойти до стола вас убивает подозреваемый.\033[0m",
    required_items=[Item("фонарик", "Светящийся фонарик")],
    reward_items=None,
    next_location="конец игры (вы не смогли разгадать данное дело)"

)

go_outside = Action(
    "выйти на улицу",
    "\033[1mВы выходите на улицу и видите, что на улице темно.\nОкрестности плохо освещены. Вы можете разглядеть "
    "некоторые детали домов поблизости, но не видите никаких намеков на следы убийцы.\033[0m",
    required_items=None,
    next_location="улица"
)

find_clues = Action(
    "поискать улики",
    "\033[1mВы аккуратно осматриваете место преступления и обнаруживаете следы ботинок, оставшиеся на полу.\nВы также "
    "находите листок бумаги на котором нарисованна стрелка вверх.\033[0m",
    required_items=[Item("фонарик", "Светящийся фонарик")],
    reward_items=[Item('листок бумаги', 'Возможно это подсказка?')],
    next_location="начальная локация"
)

go_to_rooftop = Action(
    "подняться на крышу",
    "\033[1mВы поднимаетесь на крышу и обнаруживаете следы обуви, ведущие к краю крыши.\nВозможно, кто-то бежал с места"
    " преступления.\033[0m",
    required_items=[Item("фонарик", "Светящийся фонарик"), Item('листок бумаги', 'Возможно это подсказка?')],
    next_location="крыша"
)

discover_secret = Action(
    "расследовать тайну",
    "\033[1mВы решаете расследовать это секретное место и начинаете внимательно осматривать его.\nВнезапно, в темной "
    "углубке, вы находите письмо о выполненном заказе на убийство, которое подписанно тем самым подозреваемым:\n\n"
    "\033[3m'Уважаемый Заказчик, Я надеюсь, что вы удовлетворены результатами моей работы, хотя она, безусловно, "
    "не была дешевой.\nМои услуги всегда стоят своих денег, и я горжусь своей профессиональной репутацией.\nКак и "
    "обещал, я успешно выполнил ваш заказ. Все следы были стерты, и ни один детектив не сможет докопаться до вас."
    "\nВаше имя останется в тайне, как и обещалось.\nЯ надеюсь, что это было последнее сотрудничество между нами."
    "\nТем не менее, если в будущем у вас возникнет необходимость в моих услугах, не стесняйтесь обращаться.\nС "
    "уважением. Подозреваемый'\033[0m",
    required_items=None,
    reward_items=None,
    next_location="тайное укрытие"
)

go_back = Action(
    "вернуться в начальную локацию.",
    "\033[1mВы возвращаетесь в начальную локацию.\033[0m",
    required_items=None,
    reward_items=None,
    next_location='начальная локация'
)

confront_criminal = Action(
    "конфронтировать преступника",
    "\033[1mВы хватаете подозреваемого и решаете поместить его за решетку.\nВы вызываете полицию, и они приезжают в течение "
    "нескольких минут, чтобы забрать подозреваемого и поместить его в тюрьму.\033[0m",
    required_items=None,
    reward_items=None,
    next_location="конец игры (победа)"
)

# Добавляем действия к локациям
starting_location.add_action(find_clues)
starting_location.add_action(talk_to_witness)
starting_location.add_action(go_to_rooftop)
starting_location.add_action(go_to_basement)
starting_location.add_action(investigate_closet)
starting_location.add_action(go_outside)

basement.add_action(lead_staircase)

rooftop.add_action(discover_secret)

secret_hideout.add_action(confront_criminal)

# Добавляем действия по возвращению в начальную локацию
basement.add_action(go_back)
outside.add_action(go_back)
rooftop.add_action(go_back)
secret_hideout.add_action(go_back)

# Добавляем локации к игре
game = DetectiveGame()
game.add_location(rooftop)
game.add_location(secret_hideout)
game.add_location(starting_location)
game.add_location(basement)
game.add_location(outside)

# Начальная локация
game.current_location = starting_location

# Начинаем игру
game.start_game()
