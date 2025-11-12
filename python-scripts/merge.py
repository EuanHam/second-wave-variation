import pandas as pd

df1 = pd.read_csv("2nd_wave_coding.csv")
df2 = pd.read_csv("majors_version1.csv")

# Merge on "speaker" column
merged = pd.merge(df1, df2, on="speaker", how="left")
merged.to_csv("majors_2nd_wav.csv", index=False)