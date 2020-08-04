## 深入理解Jenkins

### what is Jenkins


```
Jenkins is a self-contained, open source automation server which can be used to automate all sorts of tasks related to building, testing, and delivering or deploying software.
```

### Six points of Jenkins

- Continuous Integration and Continuous Delivery
- Easy Installation
- Easy Configuration
- Plugins
- Extensible
- Distributed

### Main Features

1.  Main Feature: Jenkins Pipeline

```
what is Jenkins Pipeline?
1. Jenkins Pipeline (or simply "Pipeline") is a suite of plugins which supports implementing and integrating *continuous delivery pipelines* into Jenkins.

how to create pipeline?
1. Jenkins Pipeline provides an extensible set of tools for modeling simple-to-complex delivery pipelines "as code". The definition of a Jenkins Pipeline is typically written into a text file (called a Jenkinsfile) which in turn is checked into a project’s source control repository.
```

*continuous delivery pipelines:*

```
is an automated expression of your process for getting software from version control right through to your users and customers.
```



### How to write a Jenkinsfile(to create a Jenkins Pipeline)

1. steps(multiple )

Think of a "step" like a single command which performs a single action. When a step succeeds it moves onto the next step. When a step fails to execute correctly the Pipeline will fail.

```
// learn to write a jenkinsfile
// linux base system
pipleline {
	agent any
	stages {
		stage('build stage') {
			steps {
				sh 'echo "my first jenkinsfile!"'
				sh '''
					echo "multiline shell steps work too."
					ls -lah
				'''
				// wrap step using retry
				retry(3) {
					sh 'mvn clean package'
				}]
				// wrap step using timeout
				timeout(time: 3, unit: 'MINUTES') {
					sh './health-check.sh'
				}
			}
		}
	}
	// after all steps executed, post section can be executed.
	post {
		always {
		 echo 'this always run'
		}
		success {
			ehco 'this will run only if success.'
		}
		faiure {
			echo 'this will run only if fail.'
		}
		unstable {
			echo 'this will run only if the run war marked as unstableds.'
		}
		changed {
			echo 'this will run only if the state of pipeline has changed.'
		}
	}
}
```

2. agent directive

The `agent` directive tells Jenkins where and how to execute the Pipeline, or subset thereof. As you might expect, the `agent` is required for all Pipelines.

**agent is required ?**

```
agent {
	docker {image 'node:7-alpine'}
}
agent any

```

3. setting environment variables

```
environment {
	CONFG_PATH = '/tmp/redis/reds.conf'
}
stages {
	stage('test') {
		steps {
			sh './redis-server ${CONFIG_PATH}'
		}
	
	}

}
```

