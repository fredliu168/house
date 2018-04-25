
# 使用acme.sh安装https服务

2018-04-23

参考以下文章完成配置:
> https://ruby-china.org/topics/31983
> https://github.com/Neilpang/acme.sh/wiki/%E8%AF%B4%E6%98%8E

4367 4218 3000 8052 953
许宗华
6217 0018 3000 8589 858


acme.sh 实现了 acme 协议, 可以从 letsencrypt 生成免费的证书.

主要步骤:

安装 acme.sh
生成证书
copy 证书到 nginx/apache 或者其他服务
更新证书
更新 acme.sh

获取证书

```
acme.sh --issue  -d w.qzcool.com   --nginx

```
成功输出以下内容

```
[Mon Apr 23 15:34:55 CST 2018] Your cert is in  /root/.acme.sh/w.qzcool.com/w.qzcool.com.cer
[Mon Apr 23 15:34:55 CST 2018] Your cert key is in  /root/.acme.sh/w.qzcool.com/w.qzcool.com.key
[Mon Apr 23 15:34:56 CST 2018] The intermediate CA cert is in  /root/.acme.sh/w.qzcool.com/ca.cer
[Mon Apr 23 15:34:56 CST 2018] And the full chain certs is there:  /root/.acme.sh/w.qzcool.com/fullchain.cer

```

将 SSL 证书安装到网站的路径

```
acme.sh  --installcert  -d  w.qzcool.com   \
        --key-file   	 /home/www/ssl/w.qzcool.com.key \
        --fullchain-file /home/www/ssl/fullchain.cer \
        --reloadcmd     "service nginx force-reload"
```
编辑nginx配置文件

```
vim /etc/nginx/sites-available/weixin_qzcool_com

```

设置 ssl

```

server {
        listen 80;

        listen [::]:80;

        listen  443 ssl http2 fastopen=3 reuseport;
        # 中间证书 + 站点证书
        ssl_certificate      /home/www/ssl/fullchain.cer;

        # 创建 CSR 文件时用的密钥
        ssl_certificate_key  /home/www/ssl/w.qzcool.com.key;

        ssl_prefer_server_ciphers  on;

        ssl_protocols              TLSv1 TLSv1.1 TLSv1.2;

        server_name w.qzcool.com;

        location / {
         proxy_pass  http://127.0.0.1:5001/;
         proxy_set_header    Host    $host;
         proxy_set_header    X-Real-IP   $remote_addr;
        }
        }





```

重启nginx

```
service nginx restart
```

自动更新证书
```
crontab -l
49 0 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null
```

acme.sh --cron 命令执行以后将会 申请新的证书 并放到相同的文件路径。由于前面执行 --installcert 的时候告知了重新 Nginx 的方法，acme.sh 也同时会在证书更新以后重启 Nginx。


最后走一下 acme.sh --cron 的流程看看能否正确执行

```
acme.sh --cron -f
```

```
[Mon Apr 23 15:51:22 CST 2018] ===Starting cron===
[Mon Apr 23 15:51:22 CST 2018] Installing from online archive.
[Mon Apr 23 15:51:22 CST 2018] Downloading https://github.com/Neilpang/acme.sh/archive/master.tar.gz
[Mon Apr 23 15:51:25 CST 2018] Extracting master.tar.gz
[Mon Apr 23 15:51:25 CST 2018] Installing to /root/.acme.sh
[Mon Apr 23 15:51:25 CST 2018] Installed to /root/.acme.sh/acme.sh
[Mon Apr 23 15:51:25 CST 2018] Good, bash is found, so change the shebang to use bash as preferred.
[Mon Apr 23 15:51:25 CST 2018] OK
[Mon Apr 23 15:51:25 CST 2018] Install success!
[Mon Apr 23 15:51:25 CST 2018] Upgrade success!
[Mon Apr 23 15:51:25 CST 2018] Auto upgraded to: 2.7.9
[Mon Apr 23 15:51:25 CST 2018] Renew: 'w.qzcool.com'
[Mon Apr 23 15:51:26 CST 2018] Single domain='w.qzcool.com'
[Mon Apr 23 15:51:26 CST 2018] Getting domain auth token for each domain
[Mon Apr 23 15:51:26 CST 2018] Getting webroot for domain='w.qzcool.com'
[Mon Apr 23 15:51:26 CST 2018] Getting new-authz for domain='w.qzcool.com'
[Mon Apr 23 15:51:28 CST 2018] The new-authz request is ok.
[Mon Apr 23 15:51:28 CST 2018] w.qzcool.com is already verified, skip http-01.
[Mon Apr 23 15:51:28 CST 2018] Verify finished, start to sign.
[Mon Apr 23 15:51:29 CST 2018] Cert success.

[Mon Apr 23 15:51:29 CST 2018] Your cert is in  /root/.acme.sh/w.qzcool.com/w.qzcool.com.cer
[Mon Apr 23 15:51:29 CST 2018] Your cert key is in  /root/.acme.sh/w.qzcool.com/w.qzcool.com.key
[Mon Apr 23 15:51:30 CST 2018] The intermediate CA cert is in  /root/.acme.sh/w.qzcool.com/ca.cer
[Mon Apr 23 15:51:30 CST 2018] And the full chain certs is there:  /root/.acme.sh/w.qzcool.com/fullchain.cer
[Mon Apr 23 15:51:30 CST 2018] Installing key to:/home/www/ssl/w.qzcool.com.key
[Mon Apr 23 15:51:30 CST 2018] Installing full chain to:/home/www/ssl/fullchain.cer
[Mon Apr 23 15:51:30 CST 2018] Run reload cmd: service nginx force-reload
[Mon Apr 23 15:51:30 CST 2018] Reload success
[Mon Apr 23 15:51:30 CST 2018] ===End cron===

```
