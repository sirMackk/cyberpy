import asyncio
import io

from secrettunnel.exceptions import StreamReaderException, StreamWriterException


class ByteStreamReader:
    def __init__(self, in_buf, chunk_size=4096, terminator=b'', loop=None):
        self.in_buf = in_buf
        self.chunk_size = chunk_size
        self.terminator = terminator
        self.finished = False
        self.bytes_read = 0
        self.loop = loop or asyncio.get_event_loop()

    async def read_into(self, out_buf):
        return self.loop.run_in_executor(None, self._read_iostream_into, out_buf)

    def _read_iostream_into(self, out_buf):
        if self.finished:
            raise StreamReaderException('Stream already read')
        for chunk in iter(lambda: self.in_buf.read(self.chunk_size), self.terminator):
            out_buf.write(chunk)
            self.bytes_read += self.chunk_size
        out_buf.eof()
        self.bytes_read -= self.chunk_size - len(chunk)
        self.finished = True


class ByteStreamWriter:
    pass


class SSHWriterAdapter:
    def __init__(self, channel):
        self.chan = channel
        self.open = True

    def write(self, data):
        if not self.open:
            raise StreamWriterException('Tried to write to closed channel')
        self.chan.write(data)

    def eof(self):
        self.open = False
        self.chan.exit(0)


class SSHReaderAdapter:
    pass
