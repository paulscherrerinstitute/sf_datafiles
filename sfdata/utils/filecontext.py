from abc import ABC, abstractmethod


class FileContext(ABC):

    @abstractmethod
    def close(self):
        raise NotImplementedError

    def __enter__(self):
#        print("enter")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
#        print("exit({}, {}, {})".format(exc_type, repr(exc_value), exc_traceback))
        self.close()
        return (exc_type is None)



