import os
import time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import search_lv_api
#from dotenv import load_dotenv

#load_dotenv()

api_search = search_lv_api.LostVault()

class DBHandler:
    def __init__(self):
        self.last_upd = datetime.today()
        self.upd_uptime = datetime.now()
        self.db_age = round((self.upd_uptime-self.last_upd).total_seconds()/60)
        self.isupdating = False
        self.is_sql_querying = False
        self.id_list = 'tribe_ids.txt'
        self.sql_url = os.getenv('DATABASE_URL')
    
    def get_tribe_ids(self):
        """
        Reads txt file with tribe ids and return list of them to fetch
        """    
        tribe_ids = []
        with open(self.id_list, encoding="utf-8") as file:
            while line := file.readline():
                tribe_ids.append(line.rstrip())
        print(f"Read tribe ids from file. Total ids - {len(tribe_ids)}")
        return tribe_ids
    
    def make_tribes_dict(self):
        # Fetch all tribes info and generate dictionary
        self.isupdating = True
        tribe_ids = self.get_tribe_ids()
        total_ids = len(tribe_ids)
        num_success = 0
        num_fail = 0
        id_fail = []
        tribes={}
        for tribe_id in tqdm(tribe_ids, total=total_ids):
            tribe = api_search.get_tribe(tribe_id)
            if tribe:
                tribes[tribe_id] = api_search.get_tribe(tribe_id)
                num_success += 1
            else:
                num_fail += 1
                id_fail.append(tribe_id)
            time.sleep(1)
        print(
            f"\nProcessed {total_ids} tribe ids\n"
            f"Parsed successful: {num_success}\n"
            f"Errors: {num_fail}\n"
            )  
        print(*id_fail, sep='\n')
        self.last_upd = datetime.now()
        self.isupdating = False
        return tribes
    
    def df_from_dict(self):
        tribes_dict = self.make_tribes_dict()
        tribes_df = pd.DataFrame.from_dict(tribes_dict, orient='index')
        return tribes_df
    
    def df_from_csv(self, csv_file):
        tribes_df = pd.read_csv(csv_file, index_col=[0])
        print('Dataframe loaded')
        return tribes_df
    
    def df_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename)
        print(f"Dataframe successfully saved to {filename}")
        return 
    
    def df_to_sql(self, dataframe):
        engine = create_engine(f"postgresql{self.sql_url[8:]}", echo=False)
        dataframe.to_sql('lvtribes', con=engine, if_exists='replace')
        engine.dispose()
        return
        
    def get_vs(self, tribe_id):
        self.fetch_power = (
            """SELECT "power" FROM lvtribes """
            f"""WHERE index = '{tribe_id}'"""
            )
        self.fetch_tribe = (
            """SELECT "rank", "tribe", "lvl", "fame", "power" """
            f"""FROM lvtribes WHERE index = '{tribe_id}'"""
            )
        engine = create_engine(f"postgresql{self.sql_url[8:]}", echo=False)
        res_power = pd.read_sql(self.fetch_power, con=engine)
        res_tribe = pd.read_sql(self.fetch_tribe, con=engine)
        if res_power.empty:
            engine.dispose()
            return res_power
        treshold = 1.15
        power = int(res_power['power'])*treshold
        self.fetch_vs = (
            """SELECT "rank", "tribe", "lvl", "fame", "power" """
            f"""FROM lvtribes WHERE "power" < {power} """
            """ORDER BY "rank" LIMIT 8"""
            )
        res_vs = pd.read_sql(self.fetch_vs, con=engine)
        vs_exclude = res_vs[~res_vs['tribe'].isin(res_tribe['tribe'])]
        output = pd.concat([res_tribe, vs_exclude])
        engine.dispose()
        return output
    

