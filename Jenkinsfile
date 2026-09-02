pipeline { 
    agent any 
    environment { 
        DOCKER_HUB_USER = 'aisharust94' 
        APP_SERVER = '10.0.1.127' 
        IMAGE_API = "${DOCKER_HUB_USER}/fitflow-api" 
        IMAGE_WORKER = "${DOCKER_HUB_USER}/fitflow-worker" 
        IMAGE_FRONTEND = "${DOCKER_HUB_USER}/fitflow-frontend" 
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
                // Запускаем официальный контейнер Ruff, монтируя в него папку с кодом бэкенда 
                sh """ 
                    echo "Запуск официального контейнера Ruff для проверки кода API..." 
                    docker run --rm -v \$(pwd)/services/api:/apps pipelinecomponents/ruff ruff check /apps 
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
                        
                        # 1. Отправляем оригинальные хэши коммитов для вашего стабильного Docker Compose
                        docker push ${IMAGE_API}:${GIT_HASH} 
                        docker push ${IMAGE_WORKER}:${GIT_HASH} 
                        docker push ${IMAGE_FRONTEND}:${GIT_HASH} 
                        
                        # 2. Навешиваем скользящие теги latest прямо в локальном кэше Дженкинса
                        docker tag ${IMAGE_API}:${GIT_HASH} ${IMAGE_API}:latest
                        docker tag ${IMAGE_WORKER}:${GIT_HASH} ${IMAGE_WORKER}:latest
                        docker tag ${IMAGE_FRONTEND}:${GIT_HASH} ${IMAGE_FRONTEND}:latest
                        
                        # 3. Отправляем теги latest на Docker Hub для автоматического запуска Kubernetes
                        docker push ${IMAGE_API}:latest
                        docker push ${IMAGE_WORKER}:latest
                        docker push ${IMAGE_FRONTEND}:latest
                    ''' 
                } 
            } 
        } 
        stage('Deploy') {
            steps {
                sshagent(['app-server-ssh']) {
                sh """
                        scp -o StrictHostKeyChecking=no \
                        docker-compose.yml \
                        ubuntu@${APP_SERVER}:/opt/fitflow/docker-compose.yml.tmp

                        ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd /opt/fitflow

                        mv docker-compose.yml.tmp docker-compose.yml

                        sed -i "/^GIT_HASH=/d" .env
                        echo "GIT_HASH=${env.GIT_HASH}" >> .env

                        echo "Deploying version: ${env.GIT_HASH}"

                        GIT_HASH=${env.GIT_HASH} docker compose config
                        GIT_HASH=${env.GIT_HASH} docker compose pull
                        GIT_HASH=${env.GIT_HASH} docker compose up -d
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
