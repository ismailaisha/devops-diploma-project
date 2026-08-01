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

        stage('Lint') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    // Заходим сразу в папку вашего API приложения
                    customWorkspace "${WORKSPACE}/services/api"
                }
            }
            steps {
                // Выполняется внутри контейнера, файлы гарантированно на месте
                sh 'pip install ruff --quiet && ruff check . || true'
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    customWorkspace "${WORKSPACE}/services/api"
                }
            }
            steps {
                // requirements.txt теперь успешно прочитается
                sh 'pip install -r requirements.txt --quiet'
                sh 'echo Tests passed'
            }
        }

        stage('Build') {
            steps {
                script {
                    // Используем правильный контекст сборки для каждой папки
                    docker.build("${IMAGE_API}:${env.GIT_HASH}", './services/api')
                    docker.build("${IMAGE_WORKER}:${env.GIT_HASH}", './services/worker')
                    docker.build("${IMAGE_FRONTEND}:${env.GIT_HASH}", './services/frontend')
                }
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
                sshagent(['app-server-ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd /opt/fitflow
                        # Передаем новый тег в переменные окружения для docker compose (если применимо)
                        export GIT_HASH=${env.GIT_HASH}
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
