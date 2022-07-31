from src.utils.get_root_path import get_project_root
from src.api_connection import APIConnect

import src.config as config
import src.vars as vars
import pandas as pd
import numpy as np


class Analysis:

    def __init__(self):
        self.path = str(get_project_root())
        self.data_properties = pd.DataFrame()
        self.data_users = pd.DataFrame()
        self.data_visits = pd.DataFrame()
        self.visites_done = None

    def __read_data(self)->None:
        """
        Read files from data file, information for visits, users and properties
        :return: None
        """
        self.data_visits = pd.read_csv(filepath_or_buffer=self.path + config.visits)
        self.data_users = pd.read_csv(filepath_or_buffer=self.path + config.users)
        self.data_properties = pd.read_csv(filepath_or_buffer=self.path + config.properties)

    def __first_question(self)->int:
        """
        Calculate
        :return:
        """
        self.visites_done = len(self.data_visits.loc[self.data_visits["status"]==vars.status].axes[0])
        print(self.visites_done)

    def __second_question(self):
        number_users = len(list(self.data_users["user_id"]))
        df = pd.merge(self.data_properties,self.data_users,how="inner",on="property_id")
        print(df)


    def __third_question(self, user_id:str):

        def which_property(user_id=user_id) -> list:
            list_properties = self.data_users.loc[self.data_users["user_id"]==user_id]["property_id"].values.tolist()
            return list_properties

        def take_information(list_properties:list):
            list_informations = []
            df_dates = pd.DataFrame()
            latitud, longitud = None, None
            for item in list_properties:
                latitud = self.data_properties.loc[self.data_properties["property_id"]==item]["latitude"].values[0]
                longitud = self.data_properties.loc[self.data_properties["property_id"] == item]["longitude"].values[0]

                df_dates = self.data_visits.loc[(self.data_visits["property_id"] == item) & (self.data_visits[
                                                                                              "status"] ==
                                                                                          "Done")][["begin_date",
                                                                                               "end_date"]]
            for index, rows in df_dates.iterrows():
                list_informations.append([latitud, longitud, rows["begin_date"], rows["end_date"]])
            return  list_informations

        def connect_api(list_information:list):
            list_json=[]
            apic = APIConnect(key=config.API_KEY, base_url=config.BaseURL)
            for item in list_information:

                apic.run(latitud=str(item[0]), longitud=str(item[1]), begin_date=str(item[2]),
                     end_date=str(item[3]))
                list_json.append(apic.response_json)
            return list_json

        def extract_temp(list_json:list):
            temp=[]
            for item in list_json:
                for day in item["days"]:
                    temp.append(day["temp"])
            avg = np.average(np.array(temp))
            return avg

        list_properties = which_property(user_id=user_id)
        list_informations = take_information(list_properties=list_properties)
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)

    def __fourth_questions(self):

        def take_information() -> list:
            list_informations =[]
            df_visits = self.data_visits.loc[self.data_visits["status"]=="Done"]
            df = pd.merge(df_visits, self.data_properties, how="inner", on="property_id")
            df = df[["latitude","longitude","begin_date","end_date"]].reset_index(drop=True)
            print(df)
            for index, rows in df.iterrows():
                list_informations.append([rows["latitude"], rows["longitude"], rows["begin_date"], rows["end_date"]])
            return  list_informations[:5]

        def connect_api(list_information:list):
            list_json=[]
            apic = APIConnect(key=config.API_KEY, base_url=config.BaseURL)
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
            return avg

        list_informations = take_information()
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)
        print(average)

    def __fifth_question(self):

        def take_information() -> list:
            list_informations =[]
            df_visits = self.data_visits.loc[self.data_visits["status"]=="Done"]
            df_properties = self.data_properties.loc[self.data_properties["localidad"] == "Suba"]
            df = pd.merge(df_visits,df_properties, on="property_id")
            df = df[["latitude","longitude","begin_date","end_date"]].reset_index(drop=True)
            print(df)
            for index, rows in df.iterrows():
                list_informations.append([rows["latitude"], rows["longitude"], rows["begin_date"], rows["end_date"]])
            return list_informations

        def connect_api(list_information:list):
            list_json=[]
            apic = APIConnect(key=config.API_KEY, base_url=config.BaseURL)
            for item in list_information:
                apic.run(latitud=str(item[0]), longitud=str(item[1]), begin_date=str(item[2]),
                     end_date=str(item[3]))
                list_json.append(apic.response_json)
            return list_json

        def extract_temp(list_json:list):
            temp=[]
            for item in list_json:
                for day in item["days"]:
                    temp.append(day["temp"])
            avg = np.average(np.array(temp))
            return avg

        list_informations = take_information()
        list_json = connect_api(list_information=list_informations)
        average = extract_temp(list_json)
        print(average)

    def run(self):
        self.__read_data()
       # self.__first_question()
       # self.__second_question()
       # self.__third_question(user_id=2)
       # self.__fourth_questions()
        self.__fifth_question()

analysis = Analysis()
analysis.run()

