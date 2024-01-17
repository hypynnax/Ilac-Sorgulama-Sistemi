from .models import Kullanici


def verify(tcno=None, password=None):
    persons = Kullanici.objects.all()

    for person in persons:
        if person.tc_no == tcno and person.password == password:
            return person

    return None
