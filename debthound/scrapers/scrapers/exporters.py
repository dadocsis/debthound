from scrapy.exporters import CsvItemExporter
import six
import csv
import io


class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, file, include_headers_line=True, join_multivalued=',', **kwargs):
        self._configure(kwargs, dont_fail=True)
        if not self.encoding:
            self.encoding = 'utf-8'
        self.include_headers_line = include_headers_line
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline=''
        ) if six.PY3 else file
        self.csv_writer = csv.writer(self.stream, **kwargs)
        self._headers_not_written = True
        self._join_multivalued = join_multivalued