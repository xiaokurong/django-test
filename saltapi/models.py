from django.db import models

# Create your models here.
class ServerGroup(models.Model):
    group_name = models.CharField(max_length=25)
    remark = models.CharField(max_length=30,null=True)

class UserPriv(models.Model):
    priv_name = models.CharField(max_length=25)

class ServerInfo(models.Model):
    salt_name = models.CharField(max_length=25)
    server_name = models.CharField(max_length=25,null=True)
    cpu = models.CharField(max_length=100,null=True)
    cpu_core = models.SmallIntegerField(null=True)
    system = models.CharField(max_length=50,null=True)
    ip_addr = models.GenericIPAddressField(protocol='ipv4',null=True)
    ram = models.IntegerField(null=True)
    disk = models.IntegerField(null=True)
    group_id = models.ForeignKey(ServerGroup,null=True,blank=True,on_delete=models.SET_NULL)
    add_date = models.DateTimeField(auto_now_add=True)

class UserInfo(models.Model):
    user_name = models.CharField(max_length=25)
    user_cnname = models.CharField(max_length=25,null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    user_pass = models.CharField(max_length=25)
    user_email = models.CharField(max_length=50,null=True)
    user_priv_id = models.ForeignKey(UserPriv,null=True,blank=True,on_delete=models.SET_NULL)


class OffenCommand(models.Model):
    command_name = models.CharField(max_length=50)
    hostnames = models.CharField(max_length=50,null=True)
    command_result = models.TextField(null=True)
    exec_time = models.DateTimeField(auto_now_add=True,null=True)





