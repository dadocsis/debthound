import pytest
import re
from datetime import datetime
from freezegun import freeze_time
from dateutil.tz import gettz
import pytz
import requests_mock
import run


@pytest.fixture()
def all_sched():
    return [
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 1,
        "start": "2018-11-30",
        "id": 15
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 4,
        "start": "2018-11-30",
        "id": 16
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 2,
        "start": "2018-11-30",
        "id": 17
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 3,
        "start": "2018-11-30",
        "id": 18
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 5,
        "start": "2018-11-30",
        "id": 19
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 6,
        "start": "2018-11-30",
        "id": 20
    },
    {
        "exact": False,
        "site_id": 1,
        "site": {
            "authtype": None,
            "base_url": "http://oris.co.palm-beach.fl.us",
            "spider_name": "pbc",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 1,
            "last_scrape_datetime": "2019-05-10T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:58:00",
        "day": 7,
        "start": "2018-11-30",
        "id": 21
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 1,
        "start": "2018-12-12",
        "id": 24
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 3,
        "start": "2018-12-12",
        "id": 25
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 5,
        "start": "2018-12-12",
        "id": 26
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "03:15:00",
        "day": 6,
        "start": "2018-12-12",
        "id": 27
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 2,
        "start": "2018-12-12",
        "id": 28
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 4,
        "start": "2018-12-12",
        "id": 29
    },
    {
        "exact": False,
        "site_id": 2,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.broward.org",
            "spider_name": "broward",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 2,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "01:00:00",
        "day": 7,
        "start": "2018-12-12",
        "id": 30
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 1,
        "start": "2019-03-29",
        "id": 45
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 3,
        "start": "2019-03-29",
        "id": 46
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 4,
        "start": "2019-03-29",
        "id": 47
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 5,
        "start": "2019-03-29",
        "id": 48
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 2,
        "start": "2019-03-29",
        "id": 49
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 6,
        "start": "2019-03-29",
        "id": 50
    },
    {
        "exact": False,
        "site_id": 3,
        "site": {
            "authtype": None,
            "base_url": "https://or.duvalclerk.com",
            "spider_name": "duval",
            "creds": None,
            "last_poll_datetime": "2019-05-12T22:50:33+00:00",
            "id": 3,
            "last_scrape_datetime": "2019-05-11T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "00:00:00",
        "day": 7,
        "start": "2019-03-29",
        "id": 51
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 2,
        "start": "2019-04-06",
        "id": 52
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 1,
        "start": "2019-04-06",
        "id": 53
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 6,
        "start": "2019-04-06",
        "id": 54
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 5,
        "start": "2019-04-06",
        "id": 55
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 3,
        "start": "2019-04-06",
        "id": 56
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 4,
        "start": "2019-04-06",
        "id": 57
    },
    {
        "exact": False,
        "site_id": 4,
        "site": {
            "authtype": None,
            "base_url": "https://officialrecords.mypinellasclerk.org",
            "spider_name": "pinellas",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 4,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "18:30:00",
        "day": 7,
        "start": "2019-05-11",
        "id": 60
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 1,
        "start": "2019-05-10",
        "id": 61
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 2,
        "start": "2019-05-10",
        "id": 62
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 3,
        "start": "2019-05-10",
        "id": 63
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 5,
        "start": "2019-05-10",
        "id": 64
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 6,
        "start": "2019-05-10",
        "id": 65
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 7,
        "start": "2019-05-10",
        "id": 66
    },
    {
        "exact": False,
        "site_id": 5,
        "site": {
            "authtype": None,
            "base_url": "https://apps.polkcountyclerk.net",
            "spider_name": "polk",
            "creds": None,
            "last_poll_datetime": "2019-05-13T01:27:33+00:00",
            "id": 5,
            "last_scrape_datetime": "2019-05-12T00:00:00+00:00"
        },
        "end": "9999-12-31",
        "time": "20:00:00",
        "day": 4,
        "start": "2019-05-10",
        "id": 67
    }
]


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
    when est (non dst) the a 7pm sched is -5 behind UTC

    """
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=one_schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 2, 6, 00, 1)) as f:  # non dst
            run.job(address)
            lpd = m.request_history[2].json()['site']['last_poll_datetime']
            assert lpd == '2019-02-06T00:01:00+00:00'
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
            "day": 4,
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

def test_all(all_sched):
    #one_schedule[0]['day'] = 3
    #one_schedule[0]['time'] = '10:00:00'
    #one_schedule[0]['site']['last_scrape_datetime'] = '2019-4-30T10:00:00+00:00'
    #one_schedule[0]['site']['last_poll_datetime'] = '2019-05-01T8:50:00+00:00'
    for sched in all_sched:
        sched["last_poll_datetime"] = "2019-05-12T18:50:33+00:00"
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=all_sched)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 12, 23)) as f:
            run.job(address)
            #assert all(['/api/v1/runspiderrequests' not in r.url for r in m.request_history])


def test_all_rolling(all_sched):
    scheds = all_sched[21:35]
    for s in scheds:
        s['site']['last_poll_datetime'] = '2019-05-13T18:59:00+00:00'
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=scheds)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 13, 19)) as f:
            run.job(address)
            lpd = m.request_history[4].json()['site']['last_poll_datetime']
            for s in scheds:
                s['site']['last_poll_datetime'] = lpd

            f.move_to(datetime(2019, 5, 13, 19, 5))
            run.job(address)
            print(m.request_history)
            assert len([r for r in m.request_history if r._request.method == 'POST']) == 2


def test_rand():
    #seven_pm_created_during_est = datetime(2019, 2, 1, tzinfo=)
    utc = pytz.UTC
    est_edt = pytz.timezone('America/New_York')
    #  both if these schedules are 8
    sched_8pm_in_utc_during_est = datetime(2019, 2, 2, tzinfo=utc)
    sched_8pm_in_utc_during_edt = datetime(2019, 5, 13, tzinfo=utc)
    with freeze_time(datetime(2019, 2, 2)) as f:
        now_in_est = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(est_edt)
        sched_8pm_in_utc_toestedt_during_est = sched_8pm_in_utc_during_est.astimezone(est_edt)
        f.move_to(datetime(2019, 5, 13))
        uct_now_in_dst = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(est_edt)
        sched_8pm_in_utc_toestedt_during_edt = sched_8pm_in_utc_during_edt.astimezone(est_edt)
        fmt = "%m-%d-%y %I:%M:%S %p"
        print(f'\nnow in est {now_in_est.strftime(fmt)}\nnow in dst {uct_now_in_dst.strftime(fmt)}')
        print(f'\nsched in est {sched_8pm_in_utc_toestedt_during_est.strftime(fmt)}\nsched in dst {sched_8pm_in_utc_toestedt_during_edt.strftime(fmt)}')