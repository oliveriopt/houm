import requests

class APIConnect:

    def __init__(self, key:str, base_url:str):
        self.api_key = key
        self.base_url = base_url
        self.response_json = None

    def __create_string_request(self, latitud:str, longitud:str, begin_date:str, end_date:str) -> str:
        """
        Build the string for the api request
        :param longitud: str
        :param latitud: str
        :param begin_date: str
        :param end_date: str
        :return: str
        """
        str_get = self.base_url + "/" + latitud + "," + longitud + "/" + begin_date[:begin_date.rfind("-")] + "/" + \
                  end_date[:end_date.rfind("-")] + "?key=" + self.api_key + "&include=days"
        return str_get

    def run(self, latitud:str or None, longitud:str or None, begin_date:str, end_date:str) -> str:
        """
        Make the api request and the output is the json response
        :param longitud: str
        :param latitud: str
        :param begin_date: str
        :param end_date: str
        :return: json
        """
        response = requests.get(self.__create_string_request(latitud=latitud, longitud=longitud, begin_date=begin_date,
                                            end_date=end_date))
        self.response_json = response.json()



