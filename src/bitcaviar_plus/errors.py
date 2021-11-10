# noinspection PyCompatibility
class InvalidMagicBytes(Exception):
    """
    Exception when magic bytes are different from 'f9beb4d9'
    """

    def __init__(self, magic_bytes):
        self.message = 'Invalid magic bytes: {}'.format(magic_bytes)
        super().__init__(self.message)
