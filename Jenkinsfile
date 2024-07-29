pipeline {
    agent any
    
    environment {
        // Definir las variables de entorno que se necesiten
        ENV_PATH = 'C:\\Users\\nasudre\\Desktop\\Robot\\ENV\\.env'
        LOG_PATH = 'C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\log.txt'
        XLSX_PATH = 'C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\Robot.xlsx'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout del repositorio Git
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/aliSg98/robot.git']]])
            }
        }
        
        stage('Setup') {
            steps {
                // Verificar la versión de Python
                sh 'python --version'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Instalar dependencias si es necesario
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Execute main.py') {
            steps {
                script {
                    // Ejecutar el script de Python
                    
                        python main.py
                
                }
            }
        }
    }
}