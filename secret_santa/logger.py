import os
import pandas as pd
import datetime


def log(assignment, filename):
    folder = os.path.dirname(filename)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    giver = [p[0] for p in assignment]
    receiver = [p[1] for p in assignment]
    now = datetime.datetime.now()
    year = [now.year for _ in assignment]
    df = pd.DataFrame(data={
        'year': year,
        'giver': giver,
        'receiver': receiver})
    df.to_csv(filename, index=False)
