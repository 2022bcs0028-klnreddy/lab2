pipeline {
    agent any

    environment {
        IMAGE_NAME = "ml-model"
        CONTAINER_NAME = "ml-test-container"
        PORT = "8000"
    }

    stages {

        stage('Print Student Info') {
            steps {
                sh '''
                echo "======================================"
                echo "Name: RALLAPALLI V S B HARSHITH"
                echo "Roll No: 2022BCS0042"
                echo "======================================"
                '''
            }
        }

        stage('Cleanup Old Container') {
            steps {
                sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                -p 8000:8000 \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}
                '''
            }
        }

       stage('Wait for API Readiness') {
    steps {
        script {
            // Wait 10 seconds for FastAPI to start
            sleep(time: 10, unit: 'SECONDS')

            timeout(time: 60, unit: 'SECONDS') {
                waitUntil {
                    def status = sh(
                        script: "curl -s -o /dev/null -w \"%{http_code}\" http://host.docker.internal:8000/health",
                        returnStdout: true
                    ).trim()

                    echo "Health Check Status: ${status}"
                    return (status == "200")
                }
            }
        }
    }
}

        stage('Send Valid Inference Request') {
            steps {
                sh '''
                curl -s -X POST http://host.docker.internal:8000/predict \
                -H "Content-Type: application/json" \
                -d @valid_input.json
                '''
            }
        }

        stage('Send Invalid Request') {
            steps {
                sh '''
                curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://host.docker.internal:8000/predict \
                -H "Content-Type: application/json" \
                -d @invalid_input.json
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker stop ${CONTAINER_NAME} || true
            docker rm ${CONTAINER_NAME} || true
            '''
        }
    }
}