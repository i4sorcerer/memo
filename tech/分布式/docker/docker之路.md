## docker之路（入门与实践）

### 什么是docker

docker产生的背景

- 开发和运维因为环境的不同而导致的矛盾
- 代码，系统，环境，配置等封装成镜像Image --》运维
- docker中images是只读的，并且是分层次的。比如tomcat镜像，是在linux操作系统层(centos image)，jdk(jdk8 image)层之上才可以构建成功的。

### 为什么要使用docker

- docker是DevOps中很重要的一环

### docker的八大应用场景

1. **Simplifying Configuration 简化配置**
2. **Code Pipeline Management 流水线（Jenkins，CI/CD，K8S）**
3. Developer Productivity 开发生产率
4. App isolation 应用隔离
5. Server consolidation 服务器整合
6. Debugging capabilities 可调式
7. Multi-tenancy 多重租赁技术
8. Rapid Deployment 快速部署

### docker与传统VM技术主要区别

- 最大区别：VM image中本身带有操作系统(操作系统内核)，而docker image是不带操作系统（系统内核），而是通过docker共用宿主机的操作系统内核资源。

### docker数据卷 data volume

- 就是相当于挂在一个U盘
- 可以解决容器持久化以及容器间数据共享问题
- 数据容器卷：可以通过docker创建一个卷，别的容器通过这个容器卷进行挂载
  - 创建容器卷：docker run -it --name n0 -v /tmp/data:/shara/data centos
  - 挂载容器卷：docker run -it --name n1 --volumes-from n0 centos
  - 主要应用场景：日志收集和存储
  - 只有当所有依赖此容器卷的container已经删除了之后，docker才会将其删除，意思是，n0被删除之后，n1依然可以正常访问容器卷

### docker命令

- 帮助命令
- 镜像命令
- 容器命令

### dockerfile文件

- 是用来构建镜像的构建文件：dockerfile->(build)docker镜像->(run)docker容器进程（运行镜像文件）
- 语法关键字（所有关键字大写）
  - FROM 基础镜像，相当于java中import
  - MAINTANER 镜像的维护者，姓名和邮件
  - RUN 镜像构建时执行的命令
  - WORKDIR 设置工作目录
  - EXPOSE 当前容器对外暴露的端口
  - ENV 设置环境变量
  - ADD 将宿主机中文件copy至容器，并可以自动解压压缩文件
    - 不安装其他软件zip文件自动解压不了，tar.gz可以自动解压
  - COPY  从宿主机复制文件到容器
  - VOLUME  设置容器数据卷(将主机的数据卷或者文件挂载到容器中)
  - CMD 指定容器启动过程中需要执行的命令
    - 注意点：多条CMD命令，只哟经最后一条生效。
    - 会被docker run 后的参数替换 尽量少用
  - ENTRYPOINT 指定容器启动过程中需要执行的命令
    - 会把docker run 后的命令追加进来
### [docker compose](https://www.runoob.com/docker/docker-compose.html)
- Compose 是用于定义和运行多容器 Docker 应用程序的工具。通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。
然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。

- 使用docker compose的三个步骤
1. 使用 Dockerfile 定义应用程序的环境。
2. 使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
3. 最后，执行 docker-compose up 命令来启动并运行整个应用程序。

### docker的网络

1. 单机方式
   - Bridge Network
   - Host Network
   - None Network

2. 多机方式
   - overlay network
