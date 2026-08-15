pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'aisharust94'
        APP_SERVER      = '10.0.1.127'
        IMAGE_API       = "${DOCKER_HUB_USER}/fitflow-api"
        IMAGE_WORKER    = "${DOCKER_HUB_USER}/fitflow-worker"
        IMAGE_FRONTEND  = "${DOCKER_HUB_USER}/fitflow-frontend"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                // Скачиваем код из репозитория
                checkout scm
                script {
                    // Вырезаем короткий хэш коммита для тегирования образов
                    env.GIT_HASH = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Собираем версию проекта: ${env.GIT_HASH}"
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Изолированная сборка трех образов на основе их локальных Dockerfile
                    docker.build("${IMAGE_API}:${env.GIT_HASH}", './services/api')
                    docker.build("${IMAGE_WORKER}:${env.GIT_HASH}", './services/worker')
                    docker.build("${IMAGE_FRONTEND}:${env.GIT_HASH}", './services/frontend')
                }
            }
        }

        stage('Lint & Test') {
            steps {
                // Строгая проверка кода линтером Ruff БЕЗ || true.
                // Если в коде есть критические синтаксические ошибки — пайплайн упадет и защитит сервер.
                sh """
                echo "Запуск строгого Ruff линтера внутри собранного контейнера API..."
                docker run --rm ${IMAGE_API}:${env.GIT_HASH} ruff check .
                """
            }
        }

        stage('Push') {
            steps {
                // Безопасная авторизация на Docker Hub через секретные ключи Jenkins
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
                // Подключаемся к серверу приложений в AWS через SSH-плагин
                sshagent(['app-server-ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd /opt/fitflow
                        
                        # Обновляем переменную хэша в файле .env на сервере
                        sed -i "s/^GIT_HASH=.*/GIT_HASH=${env.GIT_HASH}/" .env || echo "GIT_HASH=${env.GIT_HASH}" >> .env
                        
                        # Скачиваем новые образы с Docker Hub по чертежу docker-compose.yml
                        docker compose pull
                        
                        # Перезапускаем контейнеры в облаке AWS
                        docker compose up -d
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Успех! Версия ${env.GIT_HASH} успешно собрана, проверена линтером и развернута в AWS."
        }
        failure {
            echo "Сборка упала! Деплой заблокирован. Проверьте логи этапа Lint & Test или авторизации."
        }
    }
}
