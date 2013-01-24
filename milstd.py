import WDMTMKv2 as tmk


if __name__ == "__main__":
    from pickle import dump, load
    dump((1, 2), open("test.pickle", mode="wb"))

    class yoba:
        def __getattr__(self, name):
            return "wow"
    print(yoba().yoba)
