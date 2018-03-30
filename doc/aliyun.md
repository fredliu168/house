
# 阿里云服务器部署

登录到服务器

ssh -t root@106.14.206.112 -p 22

1.安装docker

apt install docker.io

2.安装mysql

创建文件夹

mkdir /home/docker_v/mysql/data

docker pull mysql:5.7.21

安装mysql

docker run --name fred-mysql -p 3306:3306 -v /home/docker_v/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=fred123456 -d mysql:5.7.21
