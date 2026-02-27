pipeline {
    agent any

    environment {
        IMAGE_NAME = "scarxlynx/ml-model:latest"
        CONTAINER_NAME = "wine_test_container"
        PORT = "8000"
    }

    stages {

        // -----------------------------
        // Stage 1: Pull Image
        // -----------------------------
        stage('Pull Image') {
            steps {
                sh '''
                echo "Pulling Docker image..."
                docker pull $IMAGE_NAME
                '''
            }
        }

        // -----------------------------
        // Stage 2: Run Container
        // -----------------------------
        stage('Run Container') {
            steps {
                sh '''
                echo "Starting container..."
                docker run -d --name $CONTAINER_NAME -p $PORT:$PORT $IMAGE_NAME
                '''
            }
        }

        // -----------------------------
        // Stage 3: Wait for Service
        // -----------------------------
        stage('Wait for Service Readiness') {
            steps {
                sh '''
                echo "Waiting for API to be ready..."

                for i in {1..15}
                do
                    sleep 2
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/health || true)

                    if [ "$STATUS" = "200" ]; then
                        echo "Service is ready!"
                        exit 0
                    fi
                done

                echo "Service did not start in time."
                exit 1
                '''
            }
        }

        // -----------------------------
        // Stage 4: Valid Inference Test
        // -----------------------------
        stage('Send Valid Inference Request') {
            steps {
                sh '''
                echo "Sending valid request..."

                RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST http://localhost:$PORT/predict \
                    -H "Content-Type: application/json" \
                    -d @tests/valid_input.json)

                BODY=$(echo "$RESPONSE" | head -n 1)
                STATUS=$(echo "$RESPONSE" | tail -n 1)

                echo "Status Code: $STATUS"
                echo "Response Body: $BODY"

                if [ "$STATUS" != "200" ]; then
                    echo "Valid request failed!"
                    exit 1
                fi

                echo "$BODY" | grep -q "prediction" || { echo "Prediction field missing!"; exit 1; }

                echo "$BODY" | grep -E -q '[0-9]' || { echo "Prediction is not numeric!"; exit 1; }

                echo "Valid inference test passed."
                '''
            }
        }

        // -----------------------------
        // Stage 5: Invalid Request Test
        // -----------------------------
        stage('Send Invalid Request') {
            steps {
                sh '''
                echo "Sending invalid request..."

                RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST http://localhost:$PORT/predict \
                    -H "Content-Type: application/json" \
                    -d @tests/invalid_input.json)

                BODY=$(echo "$RESPONSE" | head -n 1)
                STATUS=$(echo "$RESPONSE" | tail -n 1)

                echo "Status Code: $STATUS"
                echo "Response Body: $BODY"

                if [ "$STATUS" = "200" ]; then
                    echo "Invalid request unexpectedly succeeded!"
                    exit 1
                fi

                echo "$BODY" | grep -qi "error\\|detail" || { echo "No meaningful error message!"; exit 1; }

                echo "Invalid request test passed."
                '''
            }
        }

        // -----------------------------
        // Stage 6: Stop Container
        // -----------------------------
        stage('Stop Container') {
            steps {
                sh '''
                echo "Stopping and removing container..."
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }
    }

    // -----------------------------
    // Stage 7: Final Result
    // -----------------------------
    post {
        success {
            echo "All validation tests passed. Pipeline SUCCESS. 2022BCS0028"
        }
        failure {
            echo "Pipeline FAILED due to validation error. 2022BCS0028"
        }
        always {
            sh '''
            echo "Ensuring container cleanup..."
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            '''
        }
    }
}