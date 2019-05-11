import pytest
import re
from datetime import datetime
from freezegun import freeze_time
from dateutil.tz import gettz
import requests_mock
import run


@pytest.fixture()
def one_schedule():
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


def test_schedules_should_run_est(one_schedule):
    """
    when est (non dst) the a reoccurring one_schedule should run on the same time
    this test should prove the one_schedule will be ran on the same time whether in dst or not
    """
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=one_schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 2, 5, 00, 1)) as f:  # non dst
            run.job(address)
            lpd = m.request_history[2].json()['site']['last_poll_datetime']
            assert lpd == '2019-02-05T00:01:00+00:00'
            assert '/api/v1/runspiderrequests' in m.request_history[1].url


def test_schedule_not_time_to_run_est(one_schedule):
    """
    not time to run the scheduled scrape
    the last poll date happened after the scheduled time for scrape so it is assumed it was already ran
    """
    one_schedule[0]['day'] = 2
    one_schedule[0]['time'] = '10:00:00'
    one_schedule[0]['site']['last_scrape_datetime'] = '2018-12-31T10:00:00+00:00'
    one_schedule[0]['site']['last_poll_datetime'] = '2019-01-02T09:55:00+00:00'
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=one_schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 1, 2, 9, 59)) as f:  # est
            run.job(address)
            assert all(['/api/v1/runspiderrequests' not in r.url for r in m.request_history])


def test_sched_should_run_edt():
    s = [{
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T23:10:11+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 19,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2018-11-30",
            "site_id": 1
    }]
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=s)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 9, 23, 59, 53)) as f:
            run.job(address)
            assert any(['/api/v1/runspiderrequests' in r.url for r in
                        m.request_history])


def test_sched_should_not_run_edt(one_schedule):
    one_schedule[0]['day'] = 3
    one_schedule[0]['time'] = '10:00:00'
    one_schedule[0]['site']['last_scrape_datetime'] = '2019-4-30T10:00:00+00:00'
    one_schedule[0]['site']['last_poll_datetime'] = '2019-05-01T8:50:00+00:00'
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=one_schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 1, 8, 55)) as f:
            run.job(address)
            assert all(['/api/v1/runspiderrequests' not in r.url for r in m.request_history])