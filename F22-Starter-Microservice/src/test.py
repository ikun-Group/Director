from director_resource import DirectorResource
import application
import json


def t1():
    profile = {'first_name': 'test',
               'middle_name': 'test',
               'last_name': 'test',
               'gender': 'test',
               'birth_year': 2022,
               'birth_month': 8,
               'birth_day': 23}
    res = DirectorResource.create_director(**profile)
    print(json.dumps(res, indent=2, default=str))


if __name__ == "__main__":
    t1()
