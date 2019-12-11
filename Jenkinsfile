pipeline {
    agent any
    stages {
        stage('Instalar dependencias') {
            steps {
                sh '/usr/bin/env python3 -m venv venv'
                sh '. venv/bin/activate'
                sh '/usr/bin/env python3 -m pip install -r requirements.txt'
            }
        }
	stage('Testar') {
            steps {
                sh '/usr/bin/env python3 manage.py test'
            }
	}
        stage('Empacotar') {
            steps {
                script{
                    sh "rm -rf venv"

		    echo "${env.BUILD_TAG}"

                    def artifactFolder = "/var/lib/jenkins/artifacts"
                    def fullFileName = "${env.BUILD_TAG}.tar.gz"
                    def applicationZip = "${artifactFolder}/${fullFileName}"
                    
                    sh "tar -czvf ${applicationZip} ."
                }
            }
        }
        stage('Transferir para host') {
            steps {
                sh "scp -o StrictHostKeyChecking=no /var/lib/jenkins/artifacts/${env.BUILD_TAG}.tar.gz mastertech@${env.HOST}:/home/mastertech/"
            }
        }
        stage('Desempacotar') {
            steps {
                sh "ssh -t mastertech@${env.HOST} tar -xzf /home/mastertech/${env.BUILD_TAG}.tar.gz"
            }
        }
        stage('Publicar') {
            steps {
                sh "scp -o StrictHostKeyChecking=no /var/lib/jenkins/artifacts/${env.BUILD_TAG}.tar.gz mastertech@${env.HOST}:/home/mastertech/"
                sh "ssh -t mastertech@${env.HOST} /usr/bin/env python3 -m pip install -r requirements.txt --user"
	        sh "ssh -t mastertech@${env.HOST} JENKINS_NODE_COOKIE=dontKillMe sh start_django.sh ${env.PORT}"
	        sh "ssh -t mastertech@${env.HOST} rm ${env.BUILD_TAG}.tar.gz"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
