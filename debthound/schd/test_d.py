import pytest
import re
from datetime import datetime
from freezegun import freeze_time
from dateutil.tz import gettz
import requests_mock
import run


@pytest.fixture()
def schedule():
    return [
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-02-04T23:59:20+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-01-01T00:00:00+00:00"
            },
            "id": 51,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2018-03-29",
            "site_id": 3
        }
    ]


address = 'http://127.0.0.1:80/'
dt1 = datetime(2019, 2, 4, 12, 39, tzinfo=gettz()).isoformat()


def test_schedules_dst(schedule):
    """
    when dst or non dst the a reoccurring schedule should run on the same time
    this test should prove the schedule will be ran on the same time whether in dst or not
    """
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 2, 5, 00, 1)) as f:  # non dst
            run.job(address)
            assert '/api/v1/runspiderrequests' in m.request_history[1].url

            f.move_to(datetime(2019, 5, 7, 00, 1))  # dst
            run.job(address)
            assert '/api/v1/runspiderrequests' in m.request_history[4].url


def test_schedule_not_time_to_run(schedule):
    """
    not time to run the scheduled scrape
    the last poll date happened after the scheduled time for scrape so it is assumed it was already ran
    """
    schedule[0]['time'] = '00:58:00'
    schedule[0]['site']['last_scrape_datetime'] = '2019-04-30T00:00:00+00:00'
    schedule[0]['site']['last_poll_datetime'] = '2019-04-30T01:00:00+00:00'
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 4, 30, 1, 5)) as f:  # non dst
            run.job(address)
            assert all(['/api/v1/runspiderrequests' not in r.url for r in m.request_history])
