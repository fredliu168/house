# 阿里云服务器ESC环境 FTP配置

远程服务器上，使用FTP上传下载文件的场景貌似挺多的，至少系统应用部署包上传到服务器就需要它了。

Ubuntu上文件上传下载用到的工具是vsftpd，VSFTPD代表非常安全的文件传输协议守护程序，是一个开放源代码，轻量级，稳定，最安全，最快的FTP服务器的Unix和Linux操作系统。它是大多数Linux和Unix操作系统（例如RedHat，CentOS，Fedora和Ubuntu）的默认FTP服务器，同时支持IPv6和SSL，因此，我们可以使用VSFTPD来组织设置安全的FTP服务器。它是根据GPL许可的，完全免费。

## 安装vsftpd
vsftpd 默认是存在于Ubuntu的软件仓库中的，所以只需要在使用命令直接安装即可：

```cmd

sudo apt-get install vsftpd

```


## 创建FTP用户

为FTP创建特定用户，一是为了避免匿名用户登录，二是禁止用户越权访问其它文件目录内容。

FTP用户拥有以下特性：

> 禁止SSH登陆到系统，只允许FTP登录
> 禁止访问非当前用户目录下的内容

```
# 新建用户以及对应的用户目录，禁止登录系统
sudo useradd -d /home/[username] -s /sbin/nologin -m [username]
# 更改密码
sudo passwd [username]
# 调整权限
sudo chmod a-w /home/[username]
# 创建data目录，避免500错误。
# data目录为ftp上传目录
sudo mkdir /home/[username]/data
sudo chown -R [username]:[username] /home/[username]/data

```

创建文件 /etc/vsftpd.allowed_users，写入新建的用户运行该用户FTP登录：

```
# 创建文件
touch /etc/vsftpd.allowed_users
# 编辑文件
nano /etc/vsftpd.allowed_users
# 写入新建用户名并重启vsftpd
# [username]
sudo service vsftpd restart

```

## 配置FTP

vsftpd的配置文件位于： /etc/vsftpd.conf。

通过编辑该文件完成以下几项配置：

```
# 禁止匿名用户
anonymous_enable=NO
# 允许写入
write_enable=YES
# ascii编码上传下载
ascii_upload_enable=YES
ascii_download_enable=YES
# 欢迎提示
ftpd_banner=您正在登录的是IOT-SERVER前置机FTP服务
# 用户只能访问限制的目录
chroot_local_user=YES
# 用户登录后默认目录
local_root=/home/usftper/data
# 是否使用被动模式的数据连接，如果客户机在防火墙后，请开启为YES
pasv_enable=YES
# 设置被动模式后的数据连接端口范围在n和m之间,建议为50000－60000端口
# 别忘了阿里控制台ESC中安全组运行TCP端口：50000/60000
pasv_min_port=50000
pasv_max_port=60000
# 末尾新增：只允许对应用户
userlist_deny=NO
userlist_enable=YES
userlist_file=/etc/vsftpd.allowed_users
```

保存退出，重启FTP服务。

更多配置请参考最后附录。

## 连接FTP

推荐使用工具： FlieZilla

在软件中添加站点信息（服务器IP，FTP用户密码），传输模式选择 被动。

若出现 530 Login incorrect. 错误：

```
# 编辑文件
sudo nano /etc/pam.d/vsftpd
# 注释禁用以下内容
# auth    required pam_shells.so
```
出现 500 OOPS: vsftpd: refusing to run with writable root inside chroot()

``` 
 # 编辑 /etc/vsftpd.conf文件 添加
 allow_writeable_chroot=YES
```

保存重启FTP服务

## 附录：配置属性
以下属性可能某些版本是没有的，仅供参考：
```
# 是否允许匿名登录FTP服务器，默认设置为YES允许
# 用户可使用用户名ftp或anonymous进行ftp登录，口令为用户的E-mail地址。
# 如不允许匿名访问则设置为NO
anonymous_enable=YES
# 是否允许本地用户(即linux系统中的用户帐号)登录FTP服务器，默认设置为YES允许
# 本地用户登录后会进入用户主目录，而匿名用户登录后进入匿名用户的下载目录/var/ftp/pub
# 若只允许匿名用户访问，前面加上#注释掉即可阻止本地用户访问FTP服务器
local_enable=YES
# 是否允许本地用户对FTP服务器文件具有写权限，默认设置为YES允许
write_enable=YES 
# 掩码，本地用户默认掩码为077
# 你可以设置本地用户的文件掩码为缺省022，也可根据个人喜好将其设置为其他值
#local_umask=022
# 是否允许匿名用户上传文件，须将全局的write_enable=YES。默认为YES
#anon_upload_enable=YES
# 是否允许匿名用户创建新文件夹
#anon_mkdir_write_enable=YES 
# 是否激活目录欢迎信息功能
# 当用户用CMD模式首次访问服务器上某个目录时，FTP服务器将显示欢迎信息
# 默认情况下，欢迎信息是通过该目录下的.message文件获得的
# 此文件保存自定义的欢迎信息，由用户自己建立
#dirmessage_enable=YES
# 是否让系统自动维护上传和下载的日志文件
# 默认情况该日志文件为/var/log/vsftpd.log,也可以通过下面的xferlog_file选项对其进行设定
# 默认值为NO
xferlog_enable=YES
# Make sure PORT transfer connections originate from port 20 (ftp-data).
# 是否设定FTP服务器将启用FTP数据端口的连接请求
# ftp-data数据传输，21为连接控制端口
connect_from_port_20=YES
# 设定是否允许改变上传文件的属主，与下面一个设定项配合使用
# 注意，不推荐使用root用户上传文件
#chown_uploads=YES
# 设置想要改变的上传文件的属主，如果需要，则输入一个系统用户名
# 可以把上传的文件都改成root属主。whoever：任何人
#chown_username=whoever
# 设定系统维护记录FTP服务器上传和下载情况的日志文件
# /var/log/vsftpd.log是默认的，也可以另设其它
#xferlog_file=/var/log/vsftpd.log
# 是否以标准xferlog的格式书写传输日志文件
# 默认为/var/log/xferlog，也可以通过xferlog_file选项对其进行设定
# 默认值为NO
#xferlog_std_format=YES
# 以下是附加配置，添加相应的选项将启用相应的设置
# 是否生成两个相似的日志文件
# 默认在/var/log/xferlog和/var/log/vsftpd.log目录下
# 前者是wu_ftpd类型的传输日志，可以利用标准日志工具对其进行分析；后者是vsftpd类型的日志
#dual_log_enable
# 是否将原本输出到/var/log/vsftpd.log中的日志，输出到系统日志
#syslog_enable
# 设置数据传输中断间隔时间，此语句表示空闲的用户会话中断时间为600秒
# 即当数据传输结束后，用户连接FTP服务器的时间不应超过600秒。可以根据实际情况对该值进行修改
#idle_session_timeout=600
# 设置数据连接超时时间，该语句表示数据连接超时时间为120秒，可根据实际情况对其个修改
#data_connection_timeout=120
# 运行vsftpd需要的非特权系统用户，缺省是nobody
#nopriv_user=ftpsecure
# 是否识别异步ABOR请求。
# 如果FTP client会下达“async ABOR”这个指令时，这个设定才需要启用
# 而一般此设定并不安全，所以通常将其取消
#async_abor_enable=YES
# 是否以ASCII方式传输数据。默认情况下，服务器会忽略ASCII方式的请求。
# 启用此选项将允许服务器以ASCII方式传输数据
# 不过，这样可能会导致由"SIZE /big/file"方式引起的DoS攻击
#ascii_upload_enable=YES
#ascii_download_enable=YES
# 登录FTP服务器时显示的欢迎信息
# 如有需要，可在更改目录欢迎信息的目录下创建名为.message的文件，并写入欢迎信息保存后
#ftpd_banner=Welcome to blah FTP service.
# 黑名单设置。如果很讨厌某些email address，就可以使用此设定来取消他的登录权限
# 可以将某些特殊的email address抵挡住。
#deny_email_enable=YES
# 当上面的deny_email_enable=YES时，可以利用这个设定项来规定哪些邮件地址不可登录vsftpd服务器
# 此文件需用户自己创建，一行一个email address即可
#banned_email_file=/etc/vsftpd/banned_emails
# 用户登录FTP服务器后是否具有访问自己目录以外的其他文件的权限
# 设置为YES时，用户被锁定在自己的home目录中，vsftpd将在下面chroot_list_file选项值的位置寻找chroot_list文件
# 必须与下面的设置项配合
#chroot_list_enable=YES
# 被列入此文件的用户，在登录后将不能切换到自己目录以外的其他目录
# 从而有利于FTP服务器的安全管理和隐私保护。此文件需自己建立
#chroot_list_file=/etc/vsftpd/chroot_list
# 是否允许递归查询。默认为关闭，以防止远程用户造成过量的I/O
#ls_recurse_enable=YES
# 是否允许监听。
# 如果设置为YES，则vsftpd将以独立模式运行，由vsftpd自己监听和处理IPv4端口的连接请求
listen=YES
# 设定是否支持IPV6。如要同时监听IPv4和IPv6端口，
# 则必须运行两套vsftpd，采用两套配置文件
# 同时确保其中有一个监听选项是被注释掉的
#listen_ipv6=YES
# 设置PAM外挂模块提供的认证服务所使用的配置文件名，即/etc/pam.d/vsftpd文件
# 此文件中file=/etc/vsftpd/ftpusers字段，说明了PAM模块能抵挡的帐号内容来自文件/etc/vsftpd/ftpusers中
#pam_service_name=vsftpd
# 是否允许ftpusers文件中的用户登录FTP服务器，默认为NO
# 若此项设为YES，则user_list文件中的用户允许登录FTP服务器
# 而如果同时设置了userlist_deny=YES，则user_list文件中的用户将不允许登录FTP服务器，甚至连输入密码提示信息都没有
#userlist_enable=YES/NO
# 设置是否阻扯user_list文件中的用户登录FTP服务器，默认为YES
#userlist_deny=YES/NO
# 是否使用tcp_wrappers作为主机访问控制方式。
# tcp_wrappers可以实现linux系统中网络服务的基于主机地址的访问控制
# 在/etc目录中的hosts.allow和hosts.deny两个文件用于设置tcp_wrappers的访问控制
# 前者设置允许访问记录，后者设置拒绝访问记录。
# 如想限制某些主机对FTP服务器192.168.57.2的匿名访问，编缉/etc/hosts.allow文件，如在下面增加两行命令：
# vsftpd:192.168.57.1:DENY 和vsftpd:192.168.57.9:DENY
# 表明限制IP为192.168.57.1/192.168.57.9主机访问IP为192.168.57.2的FTP服务器
# 此时FTP服务器虽可以PING通，但无法连接
tcp_wrappers=YES
```