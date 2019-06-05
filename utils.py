import os


def get_from_env(var):
    try:
        return os.environ[var]
    except KeyError:
        raise KeyError("La variable d'environnment {} n'existe pas".format(var))


