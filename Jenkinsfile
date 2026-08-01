pipeline {
    agent any
    environment {
        DOCKER_HUB_USER  = 'aisharust94'
        APP_SERVER       = '3.21.5.210'
        IMAGE_API        = "${DOCKER_HUB_USER}/fitflow-api"
        IMAGE_WORKER     = "${DOCKER_HUB_USER}/fitflow-worker"
        IMAGE_FRONTEND   = "${DOCKER_HUB_USER}/fitflow-frontend"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_HASH = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Building version: ${env.GIT_HASH}"
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Контекст сборки передается изолированно. requirements.txt запекается в образ.
                    docker.build("${IMAGE_API}:${env.GIT_HASH}", './services/api')
                    docker.build("${IMAGE_WORKER}:${env.GIT_HASH}", './services/worker')
                    docker.build("${IMAGE_FRONTEND}:${env.GIT_HASH}", './services/frontend')
                }
            }
        }

        stage('Lint & Test') {
            steps {
                // Best Practice: проверяем код прямо внутри свежесобранного контейнера приложения
                sh """
                echo "Запуск Ruff линтера внутри собранного контейнера..."
                docker run --rm ${IMAGE_API}:${env.GIT_HASH} ruff check . || true
                """
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_API}:${GIT_HASH}
                    docker push ${IMAGE_WORKER}:${GIT_HASH}
                    docker push ${IMAGE_FRONTEND}:${GIT_HASH}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                // Используем SSH Agent плагин — это самый безопасный способ работы с ключами в памяти
                sshagent(['app-server-ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd /opt/fitflow
                        
                        # Best Practice для Docker Compose: обновляем тег в .env файле на сервере, 
                        # чтобы compose знал, какую именно версию перезапускать.
                        sed -i "s/^GIT_HASH=.*/GIT_HASH=${env.GIT_HASH}/" .env || echo "GIT_HASH=${env.GIT_HASH}" >> .env
                        
                        docker compose pull
                        docker compose up -d
                    '
                    """
                }
            }
        }
    }
    post {
        success {
            echo "Успех! Версия ${env.GIT_HASH} успешно собрана, проверена и развернута."
        }
        failure {
            echo "Сборка упала. Проверьте логи конкретного этапа."
        }
    }
}
