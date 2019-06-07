from TwitterInjector import TwitterInjector

if __name__ == "__main__":

    connector = TwitterInjector()
    connector.start_stream(follow="85741735")
