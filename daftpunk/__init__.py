VERSION = 'v0.2'

REDIS_CONFIG = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
        }
GEOCODE_API = "https://maps.googleapis.com/maps/api/geocode/json"
BER_RATINGS = [
        '', # Unknown
        'ber-G',
        'ber-F',
        'ber-E2',
        'ber-E1',
        'ber-D2',
        'ber-D1',
        'ber-C3',
        'ber-C2',
        'ber-C1',
        'ber-B3',
        'ber-B2',
        'ber-B1',
        'ber-A3',
        'ber-A2',
        'ber-A1',
        ]

def get_config():
    from pkg_resources import Requirement, resource_filename
    from daftpunk.schema import DpConfig
    from os.path import isfile

    local_path = './daftpunk/config/config.json'
    global_path = resource_filename(
            Requirement.parse("daftpunk"),
            'daftpunk/config/config.json')

    if isfile(local_path):
        path = local_path
    elif isfile(global_path):
        path = global_path
    else:
        print "Couldn't find a valid config."
        quit()

    return DpConfig().from_file(path)

class DaftMeta(type):
    def __new__(mcls, name, bases, cdict):
        handlers = {}

        ignored = set(['__module__', '__metaclass__', '__doc__'])
        for key, value in cdict.items():
            if key not in ignored:
                if hasattr(value, '__daftpunk__'):
                    handlers[key] = value

        cdict['COMMANDS'] = handlers
        cdict['run'] = handle_command

        return super(DaftMeta, mcls).__new__(mcls, name, bases, cdict)

def handle_command(self):
    if self.config.command in self.COMMANDS:
        self.COMMANDS[self.config.command](self, *self.config.args)

def daftcommand(func):
    setattr(func, '__daftpunk__', None)
    return func
