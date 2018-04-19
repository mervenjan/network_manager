from django.db import models
import hashlib
from cryptography.fernet import Fernet


# Create your models here.
class Network_Devices_Manager(models.Manager):
    #过滤掉isDelete条目
    def get_queryset(self):
        return super(Network_Devices_Manager,self).get_queryset().filter(isDelete=False)


class Network_Devices_Czy(models.Model):
    #自定义模型管理器
    #当自定义了模型管理器，objects就不存在了
    #db_column配置数据库中的列名
    devObj = Network_Devices_Manager()
    ip_addr = models.CharField(max_length=32, unique=True,db_column='ip_address')
    username = models.CharField(max_length=128, db_column='username')
    password = models.CharField(max_length=400,db_column='password')
    super_password = models.CharField(max_length=400, blank=True,db_column='super_password')
    device_name = models.CharField(max_length=128, db_column='device_name')
    device_type = models.CharField(max_length=128, db_column='device_type')
    device_vender = models.CharField(max_length=128, db_column='device_vender')
    device_model = models.CharField(max_length=128, db_column='device_model')
    isDelete = models.BooleanField(default=False)

    def encrypt_p(self,password):
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.encrypt(p1)
        p2 = token.decode()
        return p2

    def decrypt_p(self,password):
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.decrypt(p1)
        p2 = token.decode()
        return p2

    def save(self, *args, **kwargs):
        self.password = self.encrypt_p(self.password)
        self.super_password = self.encrypt_p(self.super_password)
        super(Network_Devices_Czy, self).save(*args, **kwargs)

    def __str__(self):
        return self.device_name + '--' + self.ip_addr

    class Meta:
        verbose_name = "设备账号"
        verbose_name_plural = "设备账号"


class Login_User(models.Model):
    userObj = Network_Devices_Manager()
    gender = (('male', "男"), ('female', "女"),)
    name = models.CharField(max_length=128, unique=True)
    real_name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def hash_code(self,s, salt='cqczy_2018'):  # 加点盐
        h = hashlib.sha256()
        s += salt
        h.update(s.encode())  # update方法只接收bytes类型
        return h.hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.hash_code(self.password)
        super(Login_User, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "网站用户"
        verbose_name_plural = "网站用户"
