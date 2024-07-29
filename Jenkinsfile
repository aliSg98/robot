pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/aliSg98/robot.git']])
            }
        }
        stage('Run Main') {
            steps {
                sh 'python main.py'
            }
        }
    }
}