import asyncio
import unittest as t
from asyncio.test_utils import TestCase as AsyncTestCase
from unittest.mock import MagicMock
import io

from secrettunnel.streams import SSHWriterAdapter, ByteStreamReader
from secrettunnel.exceptions import StreamWriterException, StreamReaderException


class TestSSHWriterAdapter(t.TestCase):
    def setUp(self):
        self.chan = MagicMock()
        self.adapter = SSHWriterAdapter(self.chan)

    def test_write_pushes_to_underlying_channel(self):
        data = b'data'
        self.adapter.write(data)
        self.chan.write.assert_called_with(data)

    def test_write_raises_exc_when_closed(self):
        self.adapter.open = False
        with self.assertRaises(StreamWriterException):
            self.adapter.write(b'')

    def test_eof_closes_adapter(self):
        self.adapter.eof()
        self.assertFalse(self.adapter.open)

    def test_eof_exits_channel(self):
        self.adapter.eof()
        self.chan.exit.assert_called_with(0)


class TestByteStreamReader(AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_bytes = b'This is an input buffer, over'

    def setUp(self):
        self.loop = self.new_test_loop()
        self.loop.set_debug(True)

        self.input_buf = io.BytesIO()
        self.input_buf.write(self.input_bytes)
        self.input_buf.seek(0)

        self.output_buf = io.BytesIO()
        self.output_adapter = SSHWriterAdapter(self.output_buf)
        self.output_adapter.chan.exit = MagicMock()

        self.reader = ByteStreamReader(self.input_buf, chunk_size=4, loop=self.loop)

    def test_reading_when_finished_raises_exc(self):
        self.reader.finished = True
        with self.assertRaises(StreamReaderException):
            ret = self.loop.run_until_complete(self.reader.read_into(self.output_adapter))
            if ret.exception():
                raise ret.exception()

    def test_bytes_read_reports_correctly(self):
        self.loop.run_until_complete(self.reader.read_into(self.output_adapter))
        self.assertEqual(self.output_buf.tell(), len(self.input_bytes))
        self.assertEqual(self.reader.bytes_read, len(self.input_bytes))

    def test_reading_all_bytes_marks_finished(self):
        self.loop.run_until_complete(self.reader.read_into(self.output_adapter))
        self.assertTrue(self.reader.finished)

    def test_reading_writes_to_out_buf(self):
        self.loop.run_until_complete(self.reader.read_into(self.output_adapter))
        self.assertEqual(self.output_buf.getvalue(), self.input_bytes)
