from aiogram.fsm.state import StatesGroup, State

class PackageState(StatesGroup):
    isPeople = False
    idPac = State()
    selectPac = State()
    ifSort = State()
    dateSort = State()
    sortPac = State()
    packages = []
    filters = {}
    packages_sort = []