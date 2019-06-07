from TwitterInjector import TwitterInjector

if __name__ == "__main__":

    print("==========STARTING===========")
    connector = TwitterInjector()
    connector.start_stream(follow="85741735")
    print("==========ENDING===========")
