import pandas as pd
import datetime as dt
import enum

date_format = "%Y-%m-%d"
time_format = "%H:%M"
datetime_format = date_format + time_format

class Mood(enum.Enum):
    TERRIBLE = "TERRIBLE"
    BAD = "BAD"
    OKAY = "OKAY"
    GOOD = "GOOD"
    GREAT = "GREAT"

class Type(enum.Enum):
    LSD = "LSD"
    HIRT = "HIRT"
    SPRINT = "SPRINT"
    INCLINE = "INCLINE"

# Output DataFrame format
# 0 - Datetime (dt.datetime) - Run start time
# 1 - Distance (float) - Distance in km
# 2 - Duration (dt.timedelta) - Duration
# 3 - Pace (dt.timedelta) - Pace
# 4 - Type (enum.Type) - Type of run training
# 5 - RPE (int)
# 6 - Mood (enum.Mood)
# 7 - Notes (str)

def read(filename):
    if not filename.endswith(".xlsx"):
        raise FileImportError("Only .xlsx files supported")

    df = pd.read_excel(filename, sheet_name="Habit - Running")

    # Parse datetime
    dates = df["Date"].to_list()
    times = df["Time / H"].to_list()
    datetimes = [dt.datetime.strptime(d+t, datetime_format)
                 for d, t in zip(dates, times)]

    # Parse distance
    distances = df["Distance / km"].to_list()

    # Parse durations and pace
    def to_timedelta(lst):
        return [dt.timedelta(minutes=int(m), seconds=int(s))
                for m, s in map(lambda d: d.split(":"), lst)]

    durations = df["Duration / min"].to_list()
    durations = to_timedelta(durations)
    paces = df["Pace / min/km"].to_list()
    paces = to_timedelta(paces)

    # Parse running type
    run_types = df["Type"].to_list()
    mapper_type = {
        "LSD": Type.LSD,
        "HIRT": Type.HIRT,
        "Incline": Type.INCLINE,
        "Sprint": Type.SPRINT,
    }
    run_types = [mapper_type[s] for s in run_types]

    # Parse RPE
    rpes = df["RPE"].to_list()

    # Parse mood
    moods = df["Mood"].to_list()
    mapper_mood = {
        "Terrible": Mood.TERRIBLE,
        "Bad": Mood.BAD,
        "Okay": Mood.OKAY,
        "Good": Mood.GOOD,
        "Great": Mood.GREAT,
    }
    moods = [mapper_mood[s] for s in moods]

    # Parse notes
    notes = df["Notes"].to_list()

    parsed_df = pd.DataFrame(data={
        "Datetime": datetimes,
        "Distance": distances,
        "Duration": durations,
        "Pace": paces,
        "Type": run_types,
        "RPE": rpes,
        "Mood": moods,
        "Notes": notes
    })
    return parsed_df

def write(filename, data):
    raise NotImplementedError("Write method not implemented")

if __name__ == "__main__":
    import const.filepaths
    print(read(const.filepaths.DIR_RUN))
