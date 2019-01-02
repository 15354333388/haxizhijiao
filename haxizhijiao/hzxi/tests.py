from django.test import TestCase

# Create your tests here.
def t(*args, **kwargs):
    print(args, kwargs)


t(*(1,2,3,4), u=1)
d = {1:2}
print(type(d))
if type(d) == dict:
    print('ok')

for l in (1, 2, 3):
    print(l)
