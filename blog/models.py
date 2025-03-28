from .database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)


    def __repr__(self):
        return f"<Blog(title={self.title}, content={self.content})>"