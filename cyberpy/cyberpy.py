import sys
import asyncssh
import asyncio


async def handle_session(stdin, stdout, stderr):
    stdout.write(b'write file')
    stdout.channel.exit(0)


class CyberServer(asyncssh.SSHServer):
    def __init__(self, *args, **kwargs):
        # inject pin in here
        self.pin = 123

    def connection_made(self, conn):
        print('SSH connection received')
        # check password

    def begin_auth(self, username):
        # dont care about username
        return True

    def validate_password(self, username, password):
        return password == self.pin

    def password_auth_supported(self):
        return True

async def start_server():
    # figure out what to do with server host keys - use users host key? Generate a new key every time?
    await asyncssh.create_server(CyberServer, '', port, session_factory=handle_session, server_host_keys=[])

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as e:
    print('Exception: {}'.format(e))
    sys.exit(1)

loop.run_forever()
