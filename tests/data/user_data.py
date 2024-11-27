class TestUsers:
    SONIC = {
        'email': 'SonicTheHedgehog@yandex.ru',
        'password': 'GottaGoFast',
        'name': 'Sonic'
    }
    
    TAILS = {
        'email': 'MilesTailsPrower@yandex.ru',
        'password': 'GottaFlyFast',
        'name': 'Tails'
    }
    
    METAL_SONIC = {
        'email': 'MetalSonicTheHedgehog@yandex.ru',
        'password': 'GottaGoFast',
        'name': 'MetalSonic'
    }

class TestIngredients:
    VALID_INGREDIENTS = ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa6f']
    INVALID_INGREDIENTS = ['SomeWrongHashStuff'] 