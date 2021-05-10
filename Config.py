import yaml


class Config:
    # Common params
    DAYS_TO_LOAD = 30

    # API params
    POLYGON_KEY = ""

    # DB Params
    DB_USERNAME = ""
    DB_PASSWORD = ""
    DB_HOST = ""
    DB_NAME = ""
    DB_PORT = ""

    @staticmethod
    def load_from_yml(
        conf_file: str = "config.yml", db_conf_file: str = "postgres_conf.yml"
    ):
        try:
            with open(db_conf_file) as config_file:
                db_config = yaml.safe_load(config_file)
        except FileNotFoundError:
            raise Exception("There is no postgres_conf.yml in script's root directory")

        try:
            with open(conf_file) as config_file:
                config = yaml.safe_load(config_file)
        except FileNotFoundError:
            raise Exception("There is no config.yml in script's root directory")

        new_config = Config()
        try:
            new_config.POLYGON_KEY = config["polygon"]["key"]
            new_config.DAYS_TO_LOAD = config["common"]["day_to_load"]
        except KeyError:
            raise Exception("Config file incorrect. Check config.yml.dist for example.")
        try:
            new_config.DB_HOST = db_config["creds"]["host"]
            new_config.DB_NAME = db_config["creds"]["db_name"]
            new_config.DB_USERNAME = db_config["creds"]["username"]
            new_config.DB_PASSWORD = db_config["creds"]["password"]
            new_config.DB_PORT = db_config["creds"]["port"]
        except KeyError:
            raise Exception(
                "Config file incorrect. Check postgres_conf.yml.dist for example."
            )
        new_config.validate()
        return new_config

    def validate(self):
        if self.POLYGON_KEY is None or self.POLYGON_KEY == "":
            raise Exception("Config field polygon.key should not pe empty.")
        if self.DB_USERNAME is None or self.DB_USERNAME == "":
            raise Exception("Config field creds.username should not pe empty.")
        if self.DB_HOST is None or self.DB_HOST == "":
            raise Exception("Config field creds.host should not pe empty.")
        if self.DB_NAME is None or self.DB_NAME == "":
            raise Exception("Config field creds.db_name should not pe empty.")


config = Config.load_from_yml()
