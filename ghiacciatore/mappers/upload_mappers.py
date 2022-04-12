
class UploadsMapper:

    @classmethod
    def dump(cls):
        pass

    @classmethod
    def restore(cls):
        pass

    @classmethod
    def get(cls, storage, key):
        pass

    @classmethod
    def add(cls, storage, key):
        pass


def add_to_uploads_manager(wrapped_func):
    def wrapper():
        storage, resp = wrapped_func()
        UploadsMapper.add(storage)