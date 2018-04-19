from django.contrib import admin
from .models import Network_Devices_Czy,Login_User
# Register your models here.

# class Devices_Info(admin.TabularInline):
#     model = Network_Devices
#     extra = 2

@admin.register(Network_Devices_Czy)
class Network_Devices_Admin(admin.ModelAdmin):
    #inlines = [Devices_Info]
    # 列表页属性

    def get_ip_addr(self):
        return self.ip_addr
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_super_password(self):
        return self.super_password
    def get_device_name(self):
        return self.device_name
    def get_device_type(self):
        return self.device_type
    def get_device_vender(self):
        return self.device_vender
    def get_device_model(self):
        return self.device_model
    def get_isDelete(self):
        return self.isDelete

    # 修改列名显示名称：
    get_ip_addr.short_description = 'IP地址'
    get_username.short_description = '用户名'
    get_password.short_description = '密码'
    get_super_password.short_description = 'super密码'
    get_device_name.short_description = '设备名'
    get_device_type.short_description = '设备类型'
    get_device_vender.short_description = '设备厂家'
    get_device_model.short_description = '设备型号'
    get_isDelete.short_description = '删除状态'
    # 管理页面显示字段
    list_display = ['pk', get_ip_addr,get_device_name, get_username, get_password,get_super_password,get_device_type,get_device_vender,get_device_model, get_isDelete]
    # 增加列表过滤
    list_filter = ['device_name']
    # 增加查找别字段功能
    search_fields = ['ip_addr']
    # 分布字段
    list_per_page = 5
    # 执行动作位置
    actions_on_top = False
    actions_on_bottom = True

@admin.register(Login_User)
class Login_User_Admin(admin.ModelAdmin):
    #inlines = [Devices_Info]
    # 列表页属性
    def get_name(self):
        return self.name
    def get_realname(self):
        return self.real_name
    def get_password(self):
        return self.password
    def get_email(self):
        return self.email
    def get_sex(self):
        return self.sex
    def get_c_time(self):
        return self.c_time
    def get_isDelete(self):
        return self.isDelete

    # 修改列名显示名称：
    get_name.short_description = '登录名'
    get_realname.short_description = '姓名'
    get_password.short_description = '密码'
    get_email.short_description = 'E-MAIL'
    get_sex.short_description = '性别'
    get_c_time.short_description = '创建时间'
    get_isDelete.short_description = '删除状态'

    # 管理页面显示字段
    list_display = ['pk', get_name,get_realname,get_sex,get_password, get_email, get_c_time, get_isDelete]
    # 增加列表过滤
    list_filter = ['name']
    # 增加查找别字段功能
    search_fields = ['name']
    # 分布字段
    list_per_page = 5
    # 执行动作位置
    actions_on_top = False
    actions_on_bottom = True



