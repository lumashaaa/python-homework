from utils.database import save_currencies_from_cbr, get_all_currencies_from_db, delete_currency
from utils.currencies_api import get_currencies


class CurrencyController:
    def __init__(self):
     
        pass

    def refresh_from_cbr(self):
        """Скачивает свежие курсы с ЦБ и сохраняет/обновляет в БД"""
        cbr_currencies = get_currencies()        
        save_currencies_from_cbr(cbr_currencies)

    def list(self):
        """Возвращает все валюты из БД"""
        return get_all_currencies_from_db()

    def delete(self, char_code: str):
        """Удаляет валюту по коду (USD, EUR и т.д.)"""
        delete_currency(char_code)
