### DevOps的工具链使用实践

#### 开发阶段

- Spring Boot 2.1.6
- MyBatis
- Rest API
- Maven

#### UT测试阶段

- Docker(数据库)
- Junit

#### 开发环境部署(ita,itb)

- Jenkins实现自动部署

  - Jenkinsfile(pipeline Jenkinsfile )

  ```groovy
  #!groovy
  
  def version() {
      def matcher = readFile('pom.xml') =~ '<version>(.+)</version>'
      matcher ? matcher[0][1] : null
  }
  
  // n6-build_slaveで処理実行
  node ('n6-build_slave'){
  
    def mvn = tool 'maven3.6.1'
  
  		// settings.xmlの置き換え
    		stage ('Set Environment'){
    		    sh """
    		    mkdir -p /home/jenkins/.m2
    		    cp /tmp/mvnsetting/setting*.xml /home/jenkins/.m2/
    		    ls -la /home/jenkins/.m2/
    		    """
    		}
  
  
  		// ソースコードの取得
  	    stage ('Get Source Code'){
              try{
                  checkout scm
              }catch(err){
                  throw err
              }
      	}
  
  
  		// コンパイル
      	stage ('Compile'){
              try{
                  v=version()
                  if(v){
                      echo "Building version ${v}"
                  }
              	sh"mvn clean compile -U"
          	}catch(err){
              	throw err
              }
          }
  
  
  		// 単体テスト
          stage ('Unit Test'){
              try{
          	//	sh"mvn test"
          	}catch(err){
              	throw err
              }
      	}
  
  
  		// パッケージング
      	stage ('Build & Package'){
              try{
                  sh"mvn clean package -DskipTests -X"
          	}catch(err){
              	throw err
              }
      	}
  
  
  		// Nexus3への配置
      	stage ('Deploy to nexus'){
              try{
          		sh "mvn deploy -DskipTests"
          	}catch(err){
              	throw err
              }
      	}
  
  }
  
  
  ```

  

  

- Docker(数据库，SoupUI API测试工具)

  - Postgresql

    - Dockerfile

    ```dockerfile
    FROM postgres:10.8-alpine
    
    # set timezone
    ENV TZ='Asia/Tokyo'
    
    ENV LANG ja_JP.UTF-8
    ENV POSTGRES_DB sampledb
    ENV POSTGRES_PASSWORD postgrespass
    COPY ./ddl/ /docker-entrypoint-initdb.d/
    
    EXPOSE 5432
    ```

    - DB初始化脚本

  - Soup UI API测试工具

    - Dockerfile

    ```dockerfile
    # This Dockerfile depends on a base images defined in Dockerfile.soap
    FROM example-registry.com:4000/soapui:5.5.0-ciels
    
    # for docker
    ENV DOCKER_GROUP_GID 994
    # for jenkins
    ARG user=jenkins
    ARG group=jenkins
    
    ARG JENKINS_AGENT_HOME=/home/${user}
    ENV JENKINS_AGENT_HOME ${JENKINS_AGENT_HOME}
    RUN groupadd -g ${gid} ${group} \
        && useradd -d "${JENKINS_AGENT_HOME}" -u "${uid}" -g "${gid}" -m -s /bin/bash "${user}"
    
    # add a user 'jenkins'  to a group 'docker'
    RUN groupadd -o -g ${DOCKER_GROUP_GID} docker
    RUN usermod -g docker jenkins
    
    # prepare for test
    RUN mkdir -p /soapui && mkdir -p /soapui/test && chmod -R a+wx /soapui
    COPY tc /soapui/test
    RUN chmod -R 755 /soapui/test/
    WORKDIR /soapui
    
    EXPOSE 8081
    
    ```

    

  - docker-compose.yml

  ```yaml
  version: "2"
  services:
    db:
      image: ${DB_IMAGE}:${DB_TAG}
      container_name: test-db-${APP_NAME}
      volumes:
        - "db-data:/var/lib/postgresql/data"
        - "./db/ddl:/docker-entrypoint-initdb.d"
      ports:
        - "${DB_PORT}:5432"
    pgadmin4:
      image: dpage/pgadmin4
      container_name: pgadmin4-${APP_NAME}
      environment:
        PGADMIN_DEFAULT_EMAIL: xxx
        PGADMIN_DEFAULT_PASSWORD: xxx
      ports:
        - "${PGADMIN_PORT}:80"
      volumes:
        - "pgadmin4-data:/var/lib/pgadmin"            
      depends_on:
        - db
    app:
      image: ${AP_IMAGE}:${AP_TAG}
      container_name: prototype-${APP_NAME}
      ports:
        - "${AP_PORT}:8080"
      env_file:
        - app/app.env
      command: /opt/jboss/wildfly/bin/standalone.sh -b "0.0.0.0" -bmanagement "0.0.0.0" 
      depends_on:
        - db
      volumes:
        - ./logs/prototype:/opt/jboss/logs/
    test:
      build: soap
      container_name: soapui-${APP_NAME}
      ports:
        - "${SP_PORT}:${SP_PORT}"
      depends_on:
        - app
  volumes:
    db-data:
      driver: local
    pgadmin4-data:
      driver: local
  
  ```

  

#### 生产环境部署

- Jenkins实现自动部署
