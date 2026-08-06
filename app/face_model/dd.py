import pprint

def dd(*args):
    raise Exception("\n".join([pprint.pformat(a) for a in args]))
