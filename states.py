from aiogram.fsm.state import State, StatesGroup

class PupilForm(StatesGroup):
    fullname = State()
    phone = State()
    course = State()
    class_name = State()

class ClassForm(StatesGroup):
    name = State()
    course = State()
    teacher = State()
    time = State()

class TeacherForm(StatesGroup):
    name = State()
    phone = State()
    nickname = State()
    type_m = State()

class PaymentForm(StatesGroup):
    choose_id = State()
    sum = State()

class KirimState(StatesGroup):
    amount = State()
    description = State()

class ChiqimState(StatesGroup):
    amount = State()
    description = State()
