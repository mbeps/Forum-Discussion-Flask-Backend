from app import db


class AppModel:
    def save(self):
        """Allows saving of data to the database
        """
        db.session.add(self)
        db.session.commit()


from models.user import *
