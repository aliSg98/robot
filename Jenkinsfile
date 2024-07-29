pipeline {
    agent any
    stages {
        stage('Checkout') {
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