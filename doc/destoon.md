
# destoon 安装

Make sure that the htaccess file is readable by apache:

touch .htaccess
chmod 644 /home/www/destoon/www/.htaccess 

And make sure the directory it's in is readable and executable:

chmod 755 /home/www/destoon/

chmod 777  config.inc.php	
chmod 777  about/
chmod 777  file/*
chmod 777  index.html
chmod 777  baidunews.xml
chmod 777  sitemaps.xml


Ubuntu 更改文件夹及子文件夹权限 
打开终端进入你需要修改的目录 
然后执行下面这条命令 
chmod 777 * -R 

阿里云服务器的Nginx配置目录
```
:/etc/nginx/sites-available# vim default

```