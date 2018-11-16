import datetime
from multiprocessing.pool import ThreadPool
from plugins.scanners import (
    wpscan,
    droopescan
)
from db import get_db


class Scanner:

    def __init__(self, app, url, cms):
        self.app = app
        self.url = url
        self.cms = cms

    def write_to_db(self, result):
        with self.app.app_context():
            tms = datetime.datetime.now().timestamp()
            qry = "INSERT INTO cmsscan(url, cms, result, tms) VALUES(?,?,?,?)"
            dbo = get_db()
            dbo.cursor().execute(qry, (self.url, self.cms, result, tms,))
            dbo.commit()
            dbo.close()

    def scan_wp(self):
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(wpscan, (self.url,))
        result = async_result.get()
        self.write_to_db(result)

    def scan_drupal(self):
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(droopescan, (self.url,))
        result = async_result.get()
        self.write_to_db(result)

    def scan(self):
        if self.cms == "wordpress":
            self.scan_wp()
        elif self.cms == "drupal":
            self.scan_drupal()
