pipeline {
    agent any
    stages {
        stage('Git Repo') {
            steps {
                git 'https://github.com/aliSg98/robot.git'
            }
        }
        stage('Run Main') {
            steps {
                sh 'python main.py'
            }
        }
    }
}