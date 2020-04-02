from __init__ import *

db.create_all()

a = Students(reg=u"2016914403",name='Abdullah Al Thaki',dept='Computer Science and Engineering',hall='Shahidullah',roll='12',address='Chittagang',merit_score='228', seat_info="")
db.session.add(a)
b = Students(reg=u"2016914404",name='Ishtiaque Zahid',dept='Computer Science and Engineering',hall='Amar Ekushey',roll='1',address='Dhaka',merit_score='40', seat_info="")
db.session.add(b)
c = Students(reg=u"2016914405",name='Abul Fajal',dept='Computer Science and Engineering',hall='Shahidullah',roll='3',address='Dhaka',merit_score='500', seat_info="")
db.session.add(c)
d = Students(reg=u"2016914406",name='Covid-19',dept='Computer Science and Engineering',hall='Shahidullah',roll='5',address='Dhaka',merit_score='300', seat_info="")
db.session.add(d)
e = Students(reg=u"2016914400",name='Jani Na',dept='Computer Science and Engineering',hall='Shahidullah',roll='100',address='Dhaka',merit_score='133', seat_info="")
db.session.add(e)

e = User(reg=u"admin",password='adminadm')
db.session.add(e)


db.session.commit()
