
class NoMatchingFileError(Exception):

    def __init__(self, patterns):
        msg = f"No matching file for patterns: {patterns}"
        super().__init__(msg)


class NoUsableFileError(Exception):
    pass



