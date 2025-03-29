from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user = relationship("User", back_populates="blogs")
    user_id = Column(Integer, ForeignKey("users.id"))


    def __repr__(self):
        return f"<Blog(title={self.title}, content={self.content})>"
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    blogs = relationship("Blog", back_populates="user")
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"