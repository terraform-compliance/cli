import diskcache
from terraform_compliance.common.defaults import Defaults


class Cache(object):
    def __init__(self):
        self.cache = diskcache.Cache(Defaults.cache_dir)

    def set(self, key, value):
        return self.cache.add(bytes(key, encoding='utf8'), value)

    def get(self, key):
        return self.cache.get(bytes(key, encoding='utf8'))

    def delete(self, key):
        del self.cache[bytes(key, encoding='utf8')]

    def close(self):
        return self.cache.close()
