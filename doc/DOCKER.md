# docker 相关操作
> 2018-03-30

>Docker —— 从入门到实践 https://yeasy.gitbooks.io/docker_practice/content/compose/wordpress.html

### alpine 相关操作

进入alpine容器,由于alpine没有自带命令行,所以使用sh运行容器,然后用attach进入容器:

```
docker run -itd <image_id> sh

docker attach <container_id>

#如果从这个 stdin 中 exit，不会导致容器的停止。这就是为什么推荐大家使用 docker exec 的原因。
docker exec -it <container_id> /bin/sh

docker exec -it 368dda0964a6 /bin/sh
```

###  linux终端中输入sh命令后无法退出

```
ctrl-d或者exit

```

### alpine python3 无法安装lxml

Dockerfile 安装 requirements.txt前执行
```
RUN apk add --update --no-cache g++ gcc libxslt-dev==1.1.29-r1
```

运行:
```
docker run -d -p 5000:5000 --name myhouse -v /Users/fred/PycharmProjects/house/upload:/code/upload house
```

### docker 打包

```
docker build -t house .
```