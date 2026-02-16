from .models import Person


def get_all_downline_people(person):
    downlines = []

    direct = person.downline.all()
    for p in direct:
        downlines.append(p)
        downlines += get_all_downline_people(p)

    return downlines


def get_all_clients_under(person):
    people = [person] + get_all_downline_people(person)
    return [p for p in people if p.role == "client"]
