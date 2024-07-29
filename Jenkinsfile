pipeline {
    agent any    
    
    stages {
        environment {
            // Definir las variables de entorno que se necesiten
            ROBOT_NAME = 'Robot_'
            URL_ROBOT = 'https://robotsparebinindustries.com/#/robot-order'
            URL_ORDERS = 'https://robotsparebinindustries.com/orders.csv'
        }
        stage('Checkout') {
            steps {
                // Checkout del repositorio Git
                checkout([$class: 'GitSCM', branches: [[name: '*/pruebas']], userRemoteConfigs: [[url: 'https://github.com/aliSg98/robot.git']]])
            }
        }
        
        stage('Setup') {
            steps {
                bat 'python --version'
            }
        }
        
        stage('Run main.py') {
            steps {
                script {
                    // Ejecutar el script
                    bat 'python main.py'
                }
            }
        }
    }
}