class SecretTunnelExc(Exception):
    pass


class OnetimePasswordError(SecretTunnelExc):
    pass


class StreamReaderException(SecretTunnelExc):
    pass


class StreamWriterException(SecretTunnelExc):
    pass
