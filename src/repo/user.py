from src.repo.config.sqlite import (
    get_session,
    User,
)


class UserRepo:
    
    session = get_session
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_one(
        cls,
        user: User
    ):
        with cls.session() as session:
            session.add(user)
            session.commit()

    
    @classmethod
    def get_by_user_id(
        cls,
        user_id: str,
    ) -> User:
        with cls.session() as session:
            return session.query(User).filter_by(user_id=user_id).first()
    
    
    @classmethod
    def get_by_email(
        cls,
        email: str,
    ) -> User:
        with cls.session() as session:
            return session.query(User).filter_by(email=email).first()
    
    
    @classmethod
    def delete_one(
        cls,
        user_id: str,
    ):
        with cls.session() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user is not None:
                user.is_deleted = 1
                user.status = 0
                session.commit()
    