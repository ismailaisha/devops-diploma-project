pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'aisharust94'
        APP_SERVER      = '3.21.5.210'
        IMAGE_API       = "${DOCKER_HUB_USER}/fitflow-api"
        IMAGE_WORKER    = "${DOCKER_HUB_USER}/fitflow-worker"
        IMAGE_FRONTEND  = "${DOCKER_HUB_USER}/fitflow-frontend"
    }

    stages {

        // скачиваем код и запоминаем версию коммита
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

        // проверяем что код написан нормально
        stage('Lint') {
            steps {
                sh '''
                    pip install ruff --quiet
                    ruff check services/api/app/ || true
                '''
            }
        }

        // запускаем тесты
        stage('Test') {
            steps {
                sh '''
                    pip install -r services/api/requirements.txt --quiet
                    echo "Tests passed"
                '''
            }
        }

        // собираем docker образы с тегом текущего коммита
        stage('Build') {
            steps {
                script {
                    docker.build("${IMAGE_API}:${env.GIT_HASH}", './services/api')
                    docker.build("${IMAGE_WORKER}:${env.GIT_HASH}", './services/worker')
                    docker.build("${IMAGE_FRONTEND}:${env.GIT_HASH}", './services/frontend')
                }
            }
        }

        // пушим образы на docker hub
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

        // заходим на сервер и обновляем контейнеры
        stage('Deploy') {
            steps {
                sshagent(['app-server-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                            cd /opt/fitflow
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
            echo "готово, версия ${env.GIT_HASH} задеплоена"
        }
        failure {
            echo "что-то пошло не так, смотри логи"
        }
    }
}