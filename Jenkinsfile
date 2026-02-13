pipeline {
    agent any

    stages {

        stage('Print Student Info') {
            steps {
                sh '''
                echo "======================================"
                echo "Name: KARRI LAKSHMI NARASIMHA REDDY"
                echo "Roll No: 2022BCS0028"
                echo "======================================"
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Training Script') {
            steps {
                sh '''
                source venv/bin/activate
                python3 train.py
                '''
            }
        }

        stage('Print Completion Message') {
            steps {
                sh '''
                echo "======================================"
                echo "Model training completed successfully!"
                echo "Name: KARRI LAKSHMI NARASIMHA REDDY"
                echo "Roll No: 2022BCS0028"
                echo "======================================"
                '''
            }
        }
    }
}
