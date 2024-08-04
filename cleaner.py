import numpy as np
import pandas as pd
import os
import re
import glob

files = [file for file in os.listdir(path="surfleague/data") if (file[-3:] == "csv") or (file[-4:] == "json")]
# files = glob.glob("surfleague/data/*.csv") + glob.glob("surfleague/data/*.json")
DATA_DIR = "surfleague/data/"
heats = pd.DataFrame()
scores = pd.DataFrame()
profiles = pd.DataFrame()
for file in files:
    if file[:5] == "heats":
        heat = pd.read_csv(DATA_DIR+file, index_col="Unnamed: 0")
        heats = pd.concat([heats, heat], ignore_index=True)
    if file[:6] == "scores":
        score = pd.read_csv(DATA_DIR+file, index_col="Unnamed: 0")
        scores = pd.concat([scores, score], ignore_index=True)
    if file[:8] == "profiles":
        import json
        with open(DATA_DIR+file, "r") as file:
            df = json.load(file)
        for key, value in df.items():
            if type(value) == list:
                if len(value) == 1:
                    df[key] = value[0]
                else:
                    df[key] = None
            else:
                df[key] = value
        profile = pd.DataFrame([df])
        profiles = pd.concat([profiles, profile], ignore_index=True)
profiles.replace([None], np.nan, inplace=True)

print(profiles.columns)
profiles["Followers"] = profiles["Followers"].str.replace("k", "000").str.replace(",", "").astype(int)
profiles["Age"] = profiles["Age"].str.extract(r"(\d\d)").astype(float)
profiles["Height"] = profiles["Height"].apply(lambda value: value if type(value) == float else np.nan if value.find("kg") >= 0 else value)
profiles["Height"] = profiles["Height"].str.replace(" cm", "").astype(float)
profiles["Weight"] = profiles["Weight"].str.replace(" kg", "").astype(float)
profiles ["First Season"] = profiles["First Season"].fillna(profiles["Stance"])
profiles["First Season"] = profiles["First Season"].apply(lambda value: np.nan if (value == "Regular") or (value == "Goofy") else value)
profiles["Stance"] = profiles.apply(lambda row: np.nan if row["Stance"] == row["First Season"] else row["Stance"], axis=1)