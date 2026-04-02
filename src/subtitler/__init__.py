import importlib.metadata as ilm

VERSION = ilm.version(__package__) if __package__ else 'version unknown'
