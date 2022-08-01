from src.analysis import Analysis
from src.utils.get_api import get_api_keyboard


def text_results(first:int, second:float, third:float, fourth:float, fifth:float) -> None:

    print("¿Cuántas visitas se realizaron en total?")
    print(first)
    print("¿Cuál es el promedio de propiedades por propietario?")
    print(second)
    print("¿Cuál era la temperatura promedio de todas las visitas que se realizó en la propiedad del propietario con ID 2?")
    print(third)
    print("¿Cuál es la temperatura promedio de las visitas para los días con lluvia?")
    print(fourth)
    print("¿Cuál es la temperatura promedio para las visitas realizadas en la localidad de Suba?")
    print(fifth)

def main():
    first, second, third, fourth, fifth = None, None, None, None, None
    key = get_api_keyboard()
    analysis = Analysis(key_api=key)
    first, second, third, fourth, fifth = analysis.run()
    text_results(first, second, third, fourth, fifth)

main()