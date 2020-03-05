from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	nickname = Column(String)
	
	def __repr__(self):
		return "%s %s %s" % (self.name, self.fullname, self.nickname)
