from src.repo.config.sqlite import get_session, User, APIKey


session = get_session()

res = session.query(APIKey).all()

for r in res:
    print(r)
