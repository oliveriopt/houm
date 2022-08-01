from src.utils.get_root_path import get_project_root
from src.api_connection import APIConnect

import src.config as config
import src.vars as vars
import pandas as pd
import numpy as np


class Analysis:

    def __init__(self, key_api:str):
        self.key_api = key_api
        self.path = str(get_project_root())
        self.data_properties = pd.DataFrame()
        self.data_users = pd.DataFrame()
        self.data_visits = pd.DataFrame()


    def __read_data(self) -> None:
        """
        Read files from data file, information for visits, users and properties
        :return: None
        """
        self.data_visits = pd.read_csv(filepath_or_buffer=self.path + config.visits)
        self.data_users = pd.read_csv(filepath_or_buffer=self.path + config.users)
        self.data_properties = pd.read_csv(filepath_or_buffer=self.path + config.properties)

    def __first_question(self) -> int:
        """
        Calculate the first question
        :return:
        """
        return len(self.data_visits.loc[self.data_visits["status"] == vars.status].axes[0])


    def __second_question(self) -> float:
        """
        Calcualte second question
        :return:
        """
        number_users = len(list(set(self.data_users["user_id"].to_list())))
        number_properties = self.data_properties.shape[0]
        return round(number_properties/number_users,2)



    def __third_question(self, user_id:str) -> float:
        """
        Calculate thord question
        :param user_id:
        :return:
        """

        def which_property(user_id:int) -> list:
            """
            Select list of properties for a determined user
            :param user_id:
            :return:
            """
            list_properties = self.data_users.loc[self.data_users["user_id"] == user_id]["property_id"].values.tolist()
            return list_properties

        def take_information(list_properties:list) -> list:
            """
            Select information for a list of properties: latitude, longitude,begin_date and end_date
            :param list_properties:
            :return:
            """
            list_informations = []
            df_dates = pd.DataFrame()
            latitud, longitud = None, None
            for item in list_properties:
                latitud = self.data_properties.loc[self.data_properties["property_id"]==item]["latitude"].values[0]
                longitud = self.data_properties.loc[self.data_properties["property_id"] == item]["longitude"].values[0]

                df_dates = self.data_visits.loc[(self.data_visits["property_id"] == item) & (self.data_visits[
                                                                                              "status"] ==
                                                                                          vars.status)][["begin_date",
                                                                                               "end_date"]]
            for index, rows in df_dates.iterrows():
                list_informations.append([latitud, longitud, rows["begin_date"], rows["end_date"]])
            return  list_informations

        def connect_api(list_information:list) -> list:
            """
            Given a list of information, requst to the api the weather
            :param list_information:
            :return:
            """
            list_json = []
            apic = APIConnect(key=self.key_api, base_url=config.BaseURL)
            for item in list_information :
                apic.run(latitud=str(item[0]), longitud=str(item[1]), begin_date=str(item[2]),
                     end_date=str(item[3]))
                list_json.append(apic.response_json)
            return list_json

        def extract_temp(list_json:list) -> float:
            temp=[]
            for item in list_json:
                for day in item["days"]:
                    temp.append(day["temp"])
            avg = np.average(np.array(temp))
            return round(avg,2)

        ### RUN THE THRID QUESTIONS####
        list_properties = which_property(user_id=user_id)
        list_informations = take_information(list_properties=list_properties)
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)
        return average

    def __fourth_questions(self) -> float:
        """
        Calculate 4th questions
        :return:
        """

        def take_information() -> list:
            """
            Select information from sources tables visit and properties
            :return:
            """
            list_informations =[]
            df_visits = self.data_visits.loc[self.data_visits["status"] == vars.status]
            df = pd.merge(df_visits, self.data_properties, how="inner", on="property_id")
            df = df[["latitude","longitude","begin_date","end_date"]].reset_index(drop=True)
            for index, rows in df.iterrows():
                list_informations.append([rows["latitude"], rows["longitude"], rows["begin_date"], rows["end_date"]])
            return list_informations

        def connect_api(list_information:list) -> list:
            """

            :param list_information:
            :return:
            """
            list_json=[]
            apic = APIConnect(key=self.key_api, base_url=config.BaseURL)
            for item in list_information:
                apic.run(latitud=str(item[0]), longitud=str(item[1]), begin_date=str(item[2]),
                     end_date=str(item[3]))
                list_json.append(apic.response_json)
            return list_json

        def extract_temp(list_json:list):
            temp=[]
            for item in list_json:
                for day in item["days"]:
                   if type(day['preciptype']) is list:
                       if day['preciptype'][0] == 'rain':
                           temp.append(day["temp"])
            avg = np.average(np.array(temp))
            return round(avg,2)

        list_informations = take_information()
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)
        return average

    def __fifth_question(self) -> float:

        def take_information() -> list:
            """
            Select information from sources tables and merge dataframes to have the answers
            :return:
            """
            list_informations =[]
            df_visits = self.data_visits.loc[self.data_visits["status"]==vars.status]
            df_properties = self.data_properties.loc[self.data_properties["localidad"] == vars.localidad]
            df = pd.merge(df_visits,df_properties, on="property_id")
            df = df[["latitude","longitude","begin_date","end_date"]].reset_index(drop=True)
            for index, rows in df.iterrows():
                list_informations.append([rows["latitude"], rows["longitude"], rows["begin_date"], rows["end_date"]])
            return list_informations

        def connect_api(list_information:list) -> list:
            """
            REquest api from list of select information
            :param list_information:
            :return:
            """
            list_json=[]
            apic = APIConnect(key=self.key_api, base_url=config.BaseURL)
            for item in list_information:
                apic.run(latitud=str(item[0]), longitud=str(item[1]), begin_date=str(item[2]),
                     end_date=str(item[3]))
                list_json.append(apic.response_json)
            return list_json

        def extract_temp(list_json:list) -> float:
            """
            Extract temperature from the response
            :param list_json:
            :return:
            """
            temp=[]
            for item in list_json:
                for day in item["days"]:
                    temp.append(day["temp"])
            avg = np.average(np.array(temp))
            return round(avg,1)

        list_informations = take_information()
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)
        return average

    def run(self):
        self.__read_data()
        print("Resolviendo primera pregunta")
        first = self.__first_question()
        print("Resolviendo segunda pregunta")
        second = self.__second_question()
        print("Resolviendo tercera pregunta")
        third = self.__third_question(user_id=2)
        print("Resolviendo cuarta pregunta")
        fourth = self.__fourth_questions()
        print("Resolviendo quinta pregunta")
        fifth = self.__fifth_question()

        return first, second, third, fourth, fifth



