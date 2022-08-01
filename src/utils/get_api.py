def get_api_keyboard():
    try:
        key = input("Por favor introduzca su llave API (sin comillas):\n")
    except Exception as error:
        print('ERROR', error)
    return key



