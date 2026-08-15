pipeline { 
    agent any 
    environment { 
        DOCKER_HUB_USER = 'aisharust94' 
        APP_SERVER = '10.0.1.127' 
        IMAGE_API = 'aisharust94/fitflow-api' 
        IMAGE_WORKER = 'aisharust94/fitflow-worker' 
        IMAGE_FRONTEND = 'aisharust94/fitflow-frontend' 
    } 
    triggers { 
        githubPush() 
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
                sh """ 
                    docker build -t ${env.IMAGE_API}:${env.GIT_HASH} ./services/api
                    docker build -t ${env.IMAGE_WORKER}:${env.GIT_HASH} ./services/worker
                    docker build -t ${env.IMAGE_FRONTEND}:${env.GIT_HASH} ./services/frontend
                """
            } 
        } 
        stage('Lint & Test') { 
            steps { 
                sh """ 
                    echo "Запуск Ruff линтера внутри собранного контейнера..." 
                    docker run --rm ${env.IMAGE_API}:${env.GIT_HASH} ruff check .
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
                    sh """ 
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin 
                        
                        # 1. Отправка хэшей коммитов для стабильного Docker Compose в облаке
                        docker push ${env.IMAGE_API}:${env.GIT_HASH} 
                        docker push ${env.IMAGE_WORKER}:${env.GIT_HASH} 
                        docker push ${env.IMAGE_FRONTEND}:${env.GIT_HASH} 
                        
                        # 2. Наклеивание скользящего тега latest поверх текущей сборки
                        docker tag ${env.IMAGE_API}:${env.GIT_HASH} ${env.IMAGE_API}:latest
                        docker tag ${env.IMAGE_WORKER}:${env.GIT_HASH} ${env.IMAGE_WORKER}:latest
                        docker tag ${env.IMAGE_FRONTEND}:${env.GIT_HASH} ${env.IMAGE_FRONTEND}:latest
                        
                        # 3. Отправка тега latest на Docker Hub для тестов Kubernetes
                        docker push ${env.IMAGE_API}:latest
                        docker push ${env.IMAGE_WORKER}:latest
                        docker push ${env.IMAGE_FRONTEND}:latest
                    """ 
                } 
            } 
        } 
        stage('Deploy') { 
            steps { 
                sshagent(['app-server-ssh']) { 
                    sh """ 
                        ssh -o StrictHostKeyChecking=no ubuntu@${env.APP_SERVER} ' 
                            cd /opt/fitflow 
                            sed -i "s/^GIT_HASH=.*/GIT_HASH=${env.GIT_HASH}/" .env || echo "GIT_HASH=${env.GIT_HASH}" >> .env 
                            docker compose pull 
                            docker compose up -d ' 
                    """ 
                } 
            } 
        } 
    } 
    post { 
        success { 
            echo "Успех! Версия ${env.GIT_HASH} успешно собрана, проверена и развернута с тегом latest." 
        } 
        failure { 
            echo "Сборка упала. Проверьте логи конкретного этапа." 
        } 
    } 
}
