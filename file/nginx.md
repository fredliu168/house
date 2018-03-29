
# 微信小程序 nginx 配置

参考文章: 怎么搭建微信小程序的本地测试服务器 https://juejin.im/post/59cf120a5188254f58414e91

不要忘记将你的测试域名加入到hosts文件中啊！！！

//hosts文件中添加测试域名
127.0.0.1 weixin.qzcool.com

Mac修改hosts

Finder的“前往”->“前往文件夹” 输入 /private/etc 按回车  就可以看到里面的hosts文件了。直接右键选择“文本编辑”打开，修改，保存即可。

由于使用容器nginx.conf

proxy_pass http://127.0.0.1:5000/ 改为 proxy_pass http://192.168.31.21:5000/ 否则访问不到



nginx.conf 配置
```
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    server {
       listen       443; 
       server_name  weixin.qzcool.com;

       ssl on;
       ssl_certificate /crt/server.crt;
       ssl_certificate_key /crt/server_nopwd.key;
 
       server_name_in_redirect off;
       proxy_set_header Host $host:$server_port;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header REMOTE-HOST $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       location / {
            proxy_pass http://192.168.31.21:5000/;
        }
}
}

```

## https服务安装

利用openssl生成证书
```
cd usr/local/etc/nginx/conf

设置server.key:openssl genrsa -des3 -out server.key 1024

参数设置:openssl req -new -key server.key -out server.csr

写RSA秘钥:openssl rsa -in server.key -out server_nopwd.key

获取私钥:openssl x509 -req -days 365 -in server.csr -signkey server_nopwd.key -out server.crt
```



启动容器

```html

docker run -p 443:443 --name mynginx -v $PWD/www:/www -v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf -v $PWD/crt:/crt -v $PWD/logs:/var/log/nginx  -d nginx

```

## 使用docker exec进入Docker容器

```html
$ sudo docker ps  
$ sudo docker exec -it b187e4175e63 /bin/bash  
```

## docker容器中安装vim

1. apt-get update，这个命令的作用是：同步 /etc/apt/sources.list 和 /etc/apt/sources.list.d 中列出的源的索引，这样才能获取到最新的软件包。

2. 等更新完毕以后再敲命令：apt-get install vim命令即可。

## Docker容器和主机如何互相拷贝传输文件

```html
docker cp cf56aa7e16b2:/etc/nginx/nginx.conf $PWD/conf/nginx.conf
``` 


使用 docker inspect 31bf67c165ad 可以获取所有的变量