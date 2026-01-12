from database import DatabaseManager
from server_generator import ServerGenerator
from config import Config


def main():
    db = DatabaseManager(Config.DB_NAME)

    for sid in range(1, Config.SERVER_COUNT + 1):
        db.create_server_table(sid)
        generator = ServerGenerator(sid, db)
        generator.run()

    db.close()


if __name__ == "__main__":
    main()
