from django.http import HttpResponse
import sys
sys.path.append('G:\\python_source\\django_test\\django_intr')
from testmodel.models import Test

def testdb(request):
    test1= Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
