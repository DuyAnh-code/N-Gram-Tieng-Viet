import pandas as pd

data = {
    "title": title,
    "content": content
}

df = pd.DataFrame([data])

df.to_csv("news.csv", mode="a", header=False, index=False)