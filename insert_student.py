from __init__ import *

db.create_all()

a = Students(reg='a',name='1',dept='1',hall='1',roll='1',address='1',merit_score='1')
db.session.add(a)
b = Students(reg='b',name='1',dept='1',hall='1',roll='1',address='1',merit_score='1')
db.session.add(b)
c = Students(reg='c',name='1',dept='1',hall='1',roll='1',address='1',merit_score='1')
db.session.add(c)
d = Students(reg='d',name='1',dept='1',hall='1',roll='1',address='1',merit_score='1')
db.session.add(d)
e = Students(reg='e',name='1',dept='1',hall='1',roll='1',address='1',merit_score='1')
db.session.add(e)


db.session.commit()
