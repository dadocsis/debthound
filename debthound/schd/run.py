import schedule
import time
import argparse
import requests
import datetime
import json
import pytz
from functools import partial

SCHEDULES_EP = 'api/v1/runspiderschedules'
RUN_REQUEST_EP = 'api/v1/runspiderrequests'
DATE_FMT = '%m/%d/%Y'
DATE_FMT_IN = '%Y-%m-%d'
DATE_TM_FMT_IN = '%Y-%m-%dT%H:%M:%S+00:00'
EST = pytz.timezone('US/Eastern')


def run(job, interval: int, api_address):
    to_run = partial(job, api_address)
    future_job = schedule.every(interval).minutes.do(to_run)
    future_job.run() # first time run immediately
    print("polling every {0} minutes".format(interval))

    while True:
        schedule.run_pending()
        time.sleep(1)


# todo: params (ie start end scrape date) should come from database
def job(api_address: str):
    current_dt = datetime.datetime.utcnow()
    rsp = requests.get('{0}{1}'.format(api_address, SCHEDULES_EP))
    schedules = rsp.json(object_hook=deserialize_dates_and_times)
    run_now = []
    for sched in schedules:
        last_poll_date = sched['site']['last_poll_datetime']
        if sched['exact']:
            date_to_run = datetime.datetime(year=current_dt.year, month=current_dt.month,
                                             day=sched['day'], hour=sched['time'].hour,
                                             minute=sched['time'].minute, second=sched['time'].second)
        else:
            first_day_of_week = current_dt - datetime.timedelta(days=current_dt.weekday())
            day_to_run = first_day_of_week + datetime.timedelta(days=sched['day'] -1)
            date_to_run = datetime.datetime(year=current_dt.year,
                                            month=current_dt.month,
                                            day=day_to_run.day,
                                            hour=sched['time'].hour,
                                            minute=sched['time'].minute,
                                            second=sched['time'].second)
        if sched['end'] >= date_to_run.date() >= sched['start']:
            run_sched = {
                'project': 'debthound',
                'spider': sched['site']['spider_name'],
                'params': {
                    'start_date': pytz.utc.localize(sched['site']['last_scrape_datetime']).astimezone(EST).strftime(DATE_FMT),
                    'end_date': pytz.utc.localize(date_to_run).astimezone(EST).strftime(DATE_FMT)
                }
            }

            if last_poll_date < date_to_run and date_to_run.day == current_dt.day:
                if sched['time'] <= current_dt.time():
                    run_now.append(run_sched)
            # if the daemon wasnt running on the day it was scheduled
            elif current_dt.day > date_to_run.day > last_poll_date.day > sched['site']['last_scrape_datetime'].day:
                run_sched['params']['end_date'] = pytz.utc.localize(last_poll_date).astimezone(EST).strftime(DATE_FMT)
                run_now.append(run_sched)

    spiders = []
    for run_sched in run_now:
        if run_sched['spider'] in spiders:
            continue
        r = requests.post('{0}{1}'.format(api_address, RUN_REQUEST_EP), data=json.dumps(run_sched),
                          headers={"Content-Type": "application/json"})
        spiders.append(run_sched['spider'])
        print(r.json())

    for site_id in {s['site']['id'] for s in schedules}:
        sched = next(iter([_s for _s in schedules if _s['site']['id'] == site_id]))
        sched['site']['last_poll_datetime'] = current_dt
        rsp = requests.put('{0}{1}'.format(api_address, SCHEDULES_EP + '/' + str(sched['id'])),
                           data=json.dumps(sched, default=serialize_dates_and_times),
                           headers={"Content-Type": "application/json"})


def deserialize_dates_and_times(obj):
    try:
        obj['start'] = datetime.datetime.strptime(obj['start'], DATE_FMT_IN).date()
        obj['end'] = datetime.datetime.strptime(obj['end'], DATE_FMT_IN).date()
        times = obj['time'].split(':')
        obj['time'] = datetime.time(hour=int(times[0]), minute=int(times[1]), second=int(times[2]))
        site = obj['site']
        site['last_scrape_datetime'] = datetime.datetime.strptime(site['last_scrape_datetime'], DATE_TM_FMT_IN)
        site['last_poll_datetime'] = datetime.datetime.strptime(site['last_poll_datetime'], DATE_TM_FMT_IN)
    except KeyError:
        pass
    return obj


def serialize_dates_and_times(obj):
    if type(obj) is datetime.time:
        return obj.isoformat(timespec='seconds')
        # obj['end'] = datetime.datetime.strptime(DATE_FMT_IN).date()
        # times = obj['time'].split(':')
        # obj['time'] = datetime.time(hour=int(times[0]), minute=int(times[1]), second=int(times[2]))
    if type(obj) is datetime.date:
        return obj.strftime(DATE_FMT_IN)
    if type(obj) is datetime.datetime:
        return obj.strftime(DATE_TM_FMT_IN)
    return obj


parser = argparse.ArgumentParser()
parser.add_argument("-i", type=int, dest='interval',
                    help="polling interval in minutes",
                    required=True)
parser.add_argument("--address", type=str, dest='address',
                    help="polling interval in minutes",
                    required=False, default="http://localhost:80/")
args = parser.parse_args()
try:
    run(job, args.interval, args.address)
except KeyboardInterrupt as kex:
    print("shutting down")


# python ./schd/run.py -i 1 --address http://127.0.0.1:5000/
