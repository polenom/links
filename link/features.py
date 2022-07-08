import string
import random

from django.contrib.auth.models import User

from link.models import Links

PERMIT_PROTOCOL = ['http', 'https', 'ftp']

def littlelink(link, num = 10):
    while True:
        onlink = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(num))
        if not Links.objects.filter(onlink = onlink):
            return onlink


def checklink(link, pk):
    linklist = link.split('/')
    print(linklist)
    if linklist[0][:-1] in PERMIT_PROTOCOL and not User.objects.get(pk=pk).links.filter(inlink=link) :
        return True
    return False