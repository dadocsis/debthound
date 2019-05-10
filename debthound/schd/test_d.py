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


@pytest.fixture()
def schedules():
    return [
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 15,
            "exact": False,
            "end": "9999-12-31",
            "day": 1,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 16,
            "exact": False,
            "end": "9999-12-31",
            "day": 4,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 17,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 18,
            "exact": False,
            "end": "9999-12-31",
            "day": 3,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 19,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 20,
            "exact": False,
            "end": "9999-12-31",
            "day": 6,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "http://oris.co.palm-beach.fl.us",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 21,
            "exact": False,
            "end": "9999-12-31",
            "day": 7,
            "start": "2018-11-30",
            "site_id": 1
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 24,
            "exact": False,
            "end": "9999-12-31",
            "day": 1,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 25,
            "exact": False,
            "end": "9999-12-31",
            "day": 3,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 26,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 27,
            "exact": False,
            "end": "9999-12-31",
            "day": 6,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 28,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 29,
            "exact": False,
            "end": "9999-12-31",
            "day": 4,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "01:00:00",
            "site": {
                "creds": None,
                "spider_name": "broward",
                "authtype": None,
                "id": 2,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.broward.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 30,
            "exact": False,
            "end": "9999-12-31",
            "day": 7,
            "start": "2018-12-12",
            "site_id": 2
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 45,
            "exact": False,
            "end": "9999-12-31",
            "day": 1,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 46,
            "exact": False,
            "end": "9999-12-31",
            "day": 3,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 47,
            "exact": False,
            "end": "9999-12-31",
            "day": 4,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 48,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 49,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 50,
            "exact": False,
            "end": "9999-12-31",
            "day": 6,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "00:00:00",
            "site": {
                "creds": None,
                "spider_name": "duval",
                "authtype": None,
                "id": 3,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://or.duvalclerk.com",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 51,
            "exact": False,
            "end": "9999-12-31",
            "day": 7,
            "start": "2019-03-29",
            "site_id": 3
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 52,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 53,
            "exact": False,
            "end": "9999-12-31",
            "day": 1,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 54,
            "exact": False,
            "end": "9999-12-31",
            "day": 6,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 55,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 56,
            "exact": False,
            "end": "9999-12-31",
            "day": 3,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 57,
            "exact": False,
            "end": "9999-12-31",
            "day": 4,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-09T10:59:28+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-08T00:00:00+00:00"
            },
            "id": 58,
            "exact": False,
            "end": "9999-12-31",
            "day": 7,
            "start": "2019-04-06",
            "site_id": 4
        }
    ]


address = 'http://127.0.0.1:80/'
dt1 = datetime(2019, 2, 4, 12, 39, tzinfo=gettz()).isoformat()


def test_schedules_dst(one_schedule):
    """
    when dst or non dst the a reoccurring one_schedule should run on the same time
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


            f.move_to(datetime(2019, 5, 7, 00, 1))  # dst
            run.job(address)
            lpd = m.request_history[5].json()['site']['last_poll_datetime']
            assert lpd == '2019-05-07T00:01:00+00:00'
            assert '/api/v1/runspiderrequests' in m.request_history[4].url
            # we assert both scheds were ran but also the last scrape times did
            # not change due to dst


def test_schedule_not_time_to_run(one_schedule):
    """
    not time to run the scheduled scrape
    the last poll date happened after the scheduled time for scrape so it is assumed it was already ran
    """
    one_schedule[0]['time'] = '00:58:00'
    one_schedule[0]['site']['last_scrape_datetime'] = '2019-04-30T00:00:00+00:00'
    one_schedule[0]['site']['last_poll_datetime'] = '2019-04-30T01:00:00+00:00'
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=one_schedule)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 4, 30, 1, 5)) as f:  # non dst
            run.job(address)
            assert all(['/api/v1/runspiderrequests' not in r.url for r in m.request_history])


def test_full_schedules_not_time_to_run(schedules):
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=schedules)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 9, 11, 4)) as f:
            run.job(address)
            assert all(['/api/v1/runspiderrequests' not in r.url for r in
                        m.request_history])


def test_sched_should_run():
    s = [{
            "time": "00:58:00",
            "site": {
                "creds": None,
                "spider_name": "pbc",
                "authtype": None,
                "id": 1,
                "last_poll_datetime": "2019-05-10T00:10:11+00:00",
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
        with freeze_time(datetime(2019, 5, 10, 0, 59, 53)) as f:
            run.job(address)
            assert any(['/api/v1/runspiderrequests' in r.url for r in
                        m.request_history])
            
#
def test_pinellas_sched():

    s = [ {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 52,
            "exact": False,
            "end": "9999-12-31",
            "day": 2,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 53,
            "exact": False,
            "end": "9999-12-31",
            "day": 1,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 54,
            "exact": False,
            "end": "9999-12-31",
            "day": 6,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 55,
            "exact": False,
            "end": "9999-12-31",
            "day": 5,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 56,
            "exact": False,
            "end": "9999-12-31",
            "day": 3,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 57,
            "exact": False,
            "end": "9999-12-31",
            "day": 4,
            "start": "2019-04-06",
            "site_id": 4
        },
        {
            "time": "18:30:00",
            "site": {
                "creds": None,
                "spider_name": "pinellas",
                "authtype": None,
                "id": 4,
                "last_poll_datetime": "2019-05-10T18:26:32+00:00",
                "base_url": "https://officialrecords.mypinellasclerk.org",
                "last_scrape_datetime": "2019-05-09T00:00:00+00:00"
            },
            "id": 58,
            "exact": False,
            "end": "9999-12-31",
            "day": 7,
            "start": "2019-04-06",
            "site_id": 4
        }
    ]
    with requests_mock.Mocker() as m:
        m.get('/' + run.SCHEDULES_EP, json=s)
        m.post('/' + run.RUN_REQUEST_EP, json={})
        p = re.compile(
            re.escape(address) + re.escape(run.SCHEDULES_EP) + r'/\d')
        m.put(p, json={'put': True})
        with freeze_time(datetime(2019, 5, 10, 18, 30, 53)) as f:
            run.job(address)
            assert any(['/api/v1/runspiderrequests' in r.url for r in
                        m.request_history])