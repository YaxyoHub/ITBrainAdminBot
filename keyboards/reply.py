from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.class_db import get_classes
from database.teacher_db import get_teachers

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 To'lovlar"), KeyboardButton(text="📝Sinflar")],
        [KeyboardButton(text="👤 O'quvchilar"), KeyboardButton(text="👤O'qituvchilar")],
        [KeyboardButton(text="📊 Xarajatlar")]
    ],
    resize_keyboard=True
)

### Pupil menu'es ###

pupil_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕O'quvchi qo'shish"), KeyboardButton(text="📝O'quvchilarni ko'rish")],
        [KeyboardButton(text="⬅️ Asosiy menyuga qaytish")]
    ],
    resize_keyboard=True
)

def classes_keyboard_add():
    classes = get_classes()  # [(id, name, type, ...), (...), ...]

    # faqat sinf nomlarini olish (2-ustun `name`)
    class_names = [row[1] for row in classes]

    # 3 tadan tugma qilib joylash
    keyboard = []
    row = []
    for i, cls in enumerate(class_names, start=1):
        row.append(KeyboardButton(text=cls))
        if i % 3 == 0:   # har 3-sida qatorni yopamiz
            keyboard.append(row)
            row = []
    if row:  # qolganlarini ham qo‘shish
        keyboard.append(row)

    # Eng oxirida "⬅️ Ortga" tugmasi alohida qatorda
    keyboard.append([KeyboardButton(text="⬅️ Ortga")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )



def classes_keyboard():
    classes = get_classes()  # [(id, name, type, ...), (...), ...]

    # faqat sinf nomlarini olish (2-ustun `name`)
    class_names = [f"Class_{row[1]}" for row in classes]

    # 3 tadan tugma qilib joylash
    keyboard = []
    row = []
    for i, cls in enumerate(class_names, start=1):
        row.append(KeyboardButton(text=cls))
        if i % 3 == 0:   # har 3-sida qatorni yopamiz
            keyboard.append(row)
            row = []
    if row:  # qolganlarini ham qo‘shish
        keyboard.append(row)

    # Eng oxirida "⬅️ Ortga" tugmasi alohida qatorda
    keyboard.append([KeyboardButton(text="⬅️ Ortga")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )



###  class menu'es  ###

class_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕Sinf qo'shish"), KeyboardButton(text="📝Sinflarni ko'rish")],
        [KeyboardButton(text="⬅️ Asosiy menyuga qaytish")]
    ],
    resize_keyboard=True
)

###    ###

def classes_keyboard_2():
    classes = get_classes()  # [(name, type, ...), (...), ...]
    
    # sinf nomlarini "class_" prefiks bilan olish
    class_names = [f"class_{row[1]}" for row in classes]

    # 3 tadan tugma qilib joylash
    keyboard = []
    row = []
    for i, cls in enumerate(class_names, start=1):
        row.append(KeyboardButton(text=cls))
        if i % 3 == 0:   # har 3-sida qatorni yopamiz
            keyboard.append(row)
            row = []
    if row:  # qolganlarini ham qo‘shish
        keyboard.append(row)

    # Eng oxirida "⬅️ Ortga" tugmasi alohida qatorda
    keyboard.append([KeyboardButton(text="⬅️ Orqaga")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


### teacher menu'es ###

teacher_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕O'qituvchi qo'shish"), KeyboardButton(text="📝O'qituvchilarni ko'rish")],
        [KeyboardButton(text="⬅️ Asosiy menyuga qaytish")]
    ],
    resize_keyboard=True
)

def teachers_keyboard():
    teachers = get_teachers()  # [(id, name, type, ...), (...), ...]

    # faqat sinf nomlarini olish (2-ustun `name`)
    teacher_names = [f"teacher_{row[1]}" for row in teachers]

    # 3 tadan tugma qilib joylash
    keyboard = []
    row = []
    for i, cls in enumerate(teacher_names, start=1):
        row.append(KeyboardButton(text=cls))
        if i % 3 == 0:   # har 3-sida qatorni yopamiz
            keyboard.append(row)
            row = []
    if row:  # qolganlarini ham qo‘shish
        keyboard.append(row)

    # Eng oxirida "⬅️ Ortga" tugmasi alohida qatorda
    keyboard.append([KeyboardButton(text="⬅️ Ortga qaytish")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


### Payment menu'es ###

def classes_keyboard_payment():
    classes = get_classes()  # [(id, name, type, ...), (...), ...]

    # faqat sinf nomlarini olish (2-ustun `name`)
    class_names = [f"💳_{row[1]}" for row in classes]

    # 3 tadan tugma qilib joylash
    keyboard = []
    row = []
    for i, cls in enumerate(class_names, start=1):
        row.append(KeyboardButton(text=cls))
        if i % 3 == 0:   # har 3-sida qatorni yopamiz
            keyboard.append(row)
            row = []
    if row:  # qolganlarini ham qo‘shish
        keyboard.append(row)

    # Eng oxirida "⬅️ Ortga" tugmasi alohida qatorda
    keyboard.append([KeyboardButton(text="⬅️ Asosiy menyuga qaytish")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

