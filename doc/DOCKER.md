# docker 相关操作
> 2018-03-30

>Docker —— 从入门到实践 https://yeasy.gitbooks.io/docker_practice/content/compose/wordpress.html


1.查看终止状态的容器可以用 

```cmd 
docker container ls -a 

```


### alpine 相关操作

进入alpine容器,由于alpine没有自带命令行,所以使用sh运行容器,然后用attach进入容器:

```
docker run -itd <image_id> sh

docker attach <container_id>

#如果从这个 stdin 中 exit，不会导致容器的停止。这就是为什么推荐大家使用 docker exec 的原因。
docker exec -it <container_id> /bin/sh

docker exec -it 5a704de602cc /bin/sh
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

### 生成镜像打包
```
docker build -t dehua_house:v1 .
```

### 运行容器

```
docker run -d -p 5000:5000 --name myhouse --link=fred-mysql:db -v /Users/fredliu/Documents/PycharmProjects/house:/code -v /Users/fredliu/Documents/PycharmProjects/house/upload:/code/upload dehua_house:v1
```

### 推送到仓库

```cython
docker tag dehua_house:v1 fredliu168/dehua_house:v1

docker push fredliu168/dehua_house:v1
```


# 阿里云docker-compose 安装

```
sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

PATH=$PATH:/usr/local/bin/docker-compose

```




zip 命令： 
```
# zip test.zip test.txt 
```

它会将 test.txt 文件压缩为 test.zip ，当然也可以指定压缩包的目录，例如 /root/test.zip 
```
# unzip test.zip 
```

它会默认将文件解压到当前目录，如果要解压到指定目录，可以加上 -d 选项 
```
# unzip test.zip -d /root/ 
```

移动当前文件夹下的所有文件到上一级目录

命令：

mv * ../
