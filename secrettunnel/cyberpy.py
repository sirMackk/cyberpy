import sys
import asyncssh
import asyncio

from secrettunnel.passwords import SimpleNumericPassword
from secrettunnel.streams import ByteStreamReader, SSHWriterAdapter


class SecretServerSession(asyncssh.SSHServerSession):
    def __init__(self, in_buf):
        self._in_buf = in_buf

    def connect_made(self, chan):
        self._chan = chan
        self._stream_reader = ByteStreamReader(self.in_buf)

    def session_started(self):
        self._chan_writer = SSHWriterAdapter(chan)
        self._stream_reader.read_into(self._chan_writer)

    def shell_requested(self):
        return True

class SecretServer(asyncssh.SSHServer):
    def __init__(self, input_buffer):
        self.in_buf = input_buffer
        self.passwd_man = SimpleNumericPassword()
        self.passwd_man.generate()

    def session_requested(self):
        return SecretServerSession(self.in_buf)

    def connect_made(self, conn):
        print('SSH connection received, streaming secret')

    def connection_lost(self, exc):
        if exc is not None:
            print('Connection error: {}'.format(exc))
        else:
            print('Connection closed')

    def begin_auth(self, username):
        return True

    def validate_password(self, username, password):
        return self.passwd_man.validate(password)

    def password_auth_supported(self):
        return True

def serve_secret():
    key = asyncssh.generate_private_key('ssh-rsa', comment='OneTimeKey', key_size=2048)
    await asyncssh.create_server(lambda: SecretServer(sys.stdin.buffer), '', port, server_host_keys=[key])

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(serve_secret())
except (OSError, asyncssh.Error) as e:
    print('Exception: {}'.format(e))
    sys.exit(1)

loop.run_forever()
