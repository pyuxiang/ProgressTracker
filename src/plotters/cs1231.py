from src.streams import streams
import collections
import pandas as pd
import datetime as dt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use('ggplot')
colors = plt.rcParams['axes.prop_cycle'].by_key()["color"]
c1 = colors[0]
c2 = colors[1]

IFILE = streams.CS1231
TARGET = ("2020-08-01", None) # manual entry for now

def generate(slope=False):
    if not IFILE.endswith(".xlsx"):
        raise FileImportError("Only .xlsx files supported")

    df = pd.read_excel(IFILE, sheet_name="CS1231")
    items = df["Item"].to_list()
    hours = [float(h) for h in df["Hours"].to_list()]
    dates = df["Date"].to_list()

    # get total hours
    total_hours = sum(hours)
    global TARGET
    TARGET = (TARGET[0], total_hours)

    # ignore nan data
    data = filter(lambda p: type(p[0]) is str, zip(dates, hours))
    data = list(map(lambda p: (p[0], float(p[1])), data))

    # accumulate difficulties on same date
    acc = collections.defaultdict(int)
    for date, diff in data:
        acc[date] += diff
    data = list(acc.items())
    data.sort(key=lambda p: p[0]) # sort by date

    # accumulate across all dates
    rating = [0] # seed
    for date, diff in data:
        rating.append(round(rating[-1] + diff, 1))
    rating = rating[1:] # throw away seed
    dates = list(map(lambda p: p[0], data))

    ########################################################
    ## ACTUAL PLOTTING ##

    dates = [dt.datetime.strptime(d, "%Y-%m-%d") for d in dates]
    ratings = rating

    # Create data point for each day
    all_dates = [dates[0], dates[0]]
    all_ratings = [0, ratings[0]]
    one_day = dt.timedelta(days=1)

    for day, rate in zip(dates[1:], ratings[1:]):
        num_days = round((day - all_dates[-1])/one_day)
        all_dates.extend([all_dates[-1]+one_day*(i+1) for i in range(num_days)])
        all_ratings.extend([all_ratings[-1]]*num_days)
        all_dates.append(day)
        all_ratings.append(rate)

    # extend to today as well
    if (all_dates[-1].toordinal() != dt.datetime.now().toordinal()):
        all_dates.append(dt.datetime.now())
        all_ratings.append(all_ratings[-1])
    ratings = all_ratings
    dates = all_dates

    ############################################################

    # Get 7-day trendline
    deadline, target = TARGET
    deadline = dt.datetime.strptime(deadline, "%Y-%m-%d")
    cutoff = dt.datetime.now() - dt.timedelta(days=7)
    data = {} # get only best rating for each day
    for day, rating in zip(dates, ratings):
        data[day] = rating
    data = list(data.items())
    data = list(filter(lambda p: p[0] >= cutoff, data))
    fit_dates, fit_ratings = list(zip(*data))

    fit_dates = [d.toordinal() for d in fit_dates] # float type for fitting
    m, c = np.polyfit(fit_dates, fit_ratings, 1)
    x1 = cutoff.toordinal()
    y1 = m*x1 + c
    x1 = dt.datetime.fromordinal(x1)
    x2 = deadline.toordinal()
    y2 = m*x2 + c
    x2 = dt.datetime.fromordinal(x2)

    x3, y3 = dates[-1], ratings[-1] # get required progress
    m_req = (target - y3)/(deadline.toordinal()-x3.toordinal())

    # Remove interpolated data points
    _dates = list(dates)
    _ratings = list(ratings)
    dates = [_dates[0], _dates[0]]
    ratings = [0, _ratings[0]]
    for day, rate in zip(_dates[1:], _ratings[1:]):
        dates.extend([day, day])
        ratings.extend([ratings[-1], rate])

    # connect edges
    if slope:
        acc = {}
        for date, rating in zip(dates, ratings):
            acc[date] = rating
        dates, ratings = list(zip(*list(acc.items())))

    def plot(fname, start, end, ylim=None):
        fig, ax = plt.subplots(figsize=(8,5))
        plt.plot([x3, deadline], [y3, target], "--", color=c1, label="Required progress = {} hours/day".format(round(m_req,1)))
        plt.plot(dates, ratings, color=c2)
        plt.plot([x3, x2], [y3, y2], "r--", color=c2, label="Current progress = {} hours/day".format(round(m, 1)))

        # Labels
        plt.ylabel("CS1231 hours")
        plt.yticks(list(range(0, 100, 10)))
        plt.xticks([
            dt.datetime(2018, 1, 1),
            dt.datetime(2018, 4, 1),
            dt.datetime(2018, 7, 1),
            dt.datetime(2018, 10, 1),
            dt.datetime(2019, 1, 1),
            dt.datetime(2019, 4, 1),
            dt.datetime(2019, 7, 1),
            dt.datetime(2019, 10, 1),
            dt.datetime(2020, 1, 1),
            dt.datetime(2020, 2, 1),
            dt.datetime(2020, 3, 1),
            dt.datetime(2020, 4, 1),
            dt.datetime(2020, 5, 1),
            dt.datetime(2020, 6, 1),
            dt.datetime(2020, 7, 1),
            dt.datetime(2020, 8, 1),
            dt.datetime(2020, 9, 1),
            dt.datetime(2020, 10, 1),
            dt.datetime(2020, 11, 1),
            dt.datetime(2020, 12, 1),
            dt.datetime(2021, 1, 1),
        ])
        plt.xlim([start, end])
        plt.ylim(ylim if ylim else [ratings[-1]-10, ratings[-1]+10])

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        fig.autofmt_xdate()
        plt.legend()
        plt.savefig("src/graphs/{}.png".format(fname))
        plt.savefig("src/graphs/{}_{}.png".format(fname, str(dt.datetime.now()).split(" ")[0]))
        plt.close()

    now = dt.datetime.now()
    window = dt.timedelta(days=30)
    plot("cs1231_progress", dt.datetime(2020, 6, 1), deadline, [0, target])
    # plot("cs1231_progress_zoom", now-window, now+window)
