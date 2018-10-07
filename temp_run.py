import configparser


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("ABS DB")
    config.set("ABS DB", "user", "isb")
    config.set("ABS DB", "pwd", "ewq123")
    config.set("ABS DB", "dbhost", "192.168.60.233")
    config.set("ABS DB", "service_name", "dev8i")

    with open(path, "w") as config_file:
        config.write(config_file)


path = "absgate.ini"
createConfig(path)