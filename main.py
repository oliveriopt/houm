from src.analysis import Analysis
from src.utils.get_api import get_api_keyboard


def text_results(first:int, second:float, third:float, fourth:float, fifth:float) -> None:

    print("¿Cuántas visitas se realizaron en total?")
    print("En total se realizaron " + str(first) + " visitas.\n\n")
    print("¿Cuál es el promedio de propiedades por propietario?")
    print("Existen " + str(second) + " propiedades por propietario.\n\n")
    print("¿Cuál era la temperatura promedio de todas las visitas que se realizó en la propiedad del propietario con ID 2?")
    print("La temperatura promedio de las visitas que se realizaron en la propiedad del ID 2 fue de " + str(third) +
          " grados Farenheit.\n\n")
    print("¿Cuál es la temperatura promedio de las visitas para los días con lluvia?")
    print("La temperatura promedio de las visitas realizadas con lluvia fueron de " + str(fourth) + " grados Farenheit.\n\n")
    print("¿Cuál es la temperatura promedio para las visitas realizadas en la localidad de Suba?")
    print("La temperatura promedio para las visitas realizadas en la localidad de Suba fueron de " + str(fifth) + " grados Farenheit.")

def main():
    first, second, third, fourth, fifth = None, None, None, None, None
    key = get_api_keyboard()
    analysis = Analysis(key_api=key)
    first, second, third, fourth, fifth = analysis.run()
    text_results(first, second, third, fourth, fifth)

main()