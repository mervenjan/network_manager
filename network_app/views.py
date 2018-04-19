from django.shortcuts import render,redirect,HttpResponse
from cryptography.fernet import Fernet
from .models import Network_Devices_Czy,Login_User
import hashlib
from forms import UserForm
from dwebsocket.decorators import accept_websocket, require_websocket
# Create your views here.

#加密登录页面数据库密码
def hash_code(s, salt='cqczy_2018'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
#解释设备登录密码字段
def decrypt_p(password):
    f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
    p1 = password.encode()
    token = f.decrypt(p1)
    p2 = token.decode()
    return p2


import ipaddress
import sys
def private_ip(ip):
    try:
        #判断 python 版本
        if sys.version_info[0] == 2:
            return ipaddress.ip_address(ip.strip().decode("utf-8")).is_private
        elif sys.version_info[0] == 3:
            return ipaddress.ip_address(bytes(ip.strip().encode("utf-8"))).is_private
    except Exception as e:
        print(e)
        return False


def index(request):
    net_dev = Network_Devices_Czy.devObj.get(pk=1)
    net_dev.password = decrypt_p(net_dev.password)
    net_dev.super_password = decrypt_p(net_dev.super_password)
    return render(request,'network_app/index.html',{'dev':net_dev})

def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = Login_User.userObj.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.real_name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'network_app/login.html', locals())

    login_form = UserForm()
    return render(request, 'network_app/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

def backup(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    return render(request,'network_app/backup.html')

from netmiko import ConnectHandler
@accept_websocket
def backup_network_config(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return HttpResponse('执行失败!')
    else:
        #for message in request.websocket:
        for tftp_server in request.websocket:
            tftp_server = tftp_server.decode('utf-8')
            #print(tftp_server)
            device_list = Network_Devices_Czy.devObj.all()
            if private_ip(tftp_server):
                for device in device_list:
                    try:
                        ip, username, password, super_pwd, device_vender,device_model = device.ip_addr, device.username, decrypt_p(
                            device.password), decrypt_p(device.super_password), device.device_vender,device.device_model
                        if device_vender == 'h3c':
                            device_vender = 'huawei'
                        huawei_device = {'ip': ip, 'username': username, 'password': password, 'device_type': device_vender}
                        request.websocket.send(('正在连接设备:' + ip).encode('utf-8'))  # 发送消息到客户端
                        # print('正在连接设备：%s……' % ip)
                        net_connect = ConnectHandler(**huawei_device)
                        # 根据设备类型输入super密码
                        if super_pwd != '' and device_vender != 'cisco':
                            net_connect.send_command("super", ':')
                            net_connect.send_command(super_pwd, '>')
                        elif super_pwd != '' and device_vender == 'cisco':
                            net_connect.send_command("enable\n%s\n" % super_pwd)

                        # 根据设备类型执行保存配置及tftp命令
                        if device_model == 'S3100-52P':
                            net_connect.send_command('u t m')
                            net_connect.send_command('scr disable')
                            request.websocket.send(('正在执行保存操作……').encode('utf-8'))
                            net_connect.send_command('save\ny\n\r\ny\n')  # 执行命令save回车y回车回车y回车
                            request.websocket.send(('正在上传文件至TFTP服务器……').encode('utf-8'))
                            net_connect.send_command('tftp %s put config.cfg %s_backup.cfg' % (tftp_server, ip))

                        elif device_vender == 'cisco':
                            request.websocket.send(('正在执行保存操作……').encode('utf-8'))
                            net_connect.send_command('write\n')
                            request.websocket.send(('正在上传文件至TFTP服务器……').encode('utf-8'))
                            net_connect.send_command("copy running-config tftp:\n %s\r\n" % tftp_server)

                        else:
                            request.websocket.send(('正在执行保存操作……').encode('utf-8'))
                            net_connect.send_command('save\ny\n')
                            request.websocket.send(('正在上传文件至TFTP服务器……').encode('utf-8'))
                            net_connect.send_command('tftp %s put vrpcfg.zip %s_backup.cfg.zip' % (tftp_server, ip))
                            net_connect.disconnect()
                    except Exception as e:
                        print(e)

                request.websocket.send(('设备备份完成，请检查TFTP服务器对应目录文件！备份完成！').encode('utf-8'))
            else:
                request.websocket.send(('输入的IP地址不合法！请重新输入!！').encode('utf-8'))



























