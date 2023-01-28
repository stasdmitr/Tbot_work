import requests
import json
from config import keys



class ConvertionException(Exception): # Исключение которое мы будем отлавливать. наследованный от класса Exeception
    pass

class CryptoConverter: 
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Одинаковые переводить не интересно( {base}')

        try: 
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Такое я не умею( {quote}')
            
        try:    
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Такое я не умею( {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Попробуй исправить количество) {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}&amount={amount}')
        total_base = json.loads(r.content)[keys[base]]*amount
        
        return total_base