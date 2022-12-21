import pandas as pd

pd.set_option("expand_frame_repr", False)

if __name__ == "__main__":
    file_name = input("Введите имя файла: ")
    df = pd.read_csv(file_name)
    df["years"] = df["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
    years = df["years"].unique()
    for year in years:
        data = df[df["years"] == year]
        data.iloc[:, :6].to_csv(rf"csv_files\part_{year}.csv", index=False)






