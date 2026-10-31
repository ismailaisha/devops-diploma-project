pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 45, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    environment {
        DOCKER_HUB_USER = 'aisharust94'
        APP_SERVER = '10.0.1.10'
        APP_USER = 'devops'

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
                deleteDir()
                checkout scm

                script {
                    def commit = sh(
                        script: 'git rev-parse --short=12 HEAD',
                        returnStdout: true
                    ).trim()

                    env.RELEASE_TAG = "${commit}-${env.BUILD_NUMBER}"
                }

                echo "Версия приложения: ${env.RELEASE_TAG}"
            }
        }

        stage('Build images') {
            steps {
                // Git не хранит пустые каталоги, но Dockerfile
                // frontend может использовать их в COPY.
                sh '''
                    set -eu
                    mkdir -p services/frontend/css \
                             services/frontend/js \
                             services/frontend/pages
                '''

                script {
                    docker.build(
                        "${IMAGE_API}:${env.RELEASE_TAG}",
                        './services/api'
                    )

                    docker.build(
                        "${IMAGE_WORKER}:${env.RELEASE_TAG}",
                        './services/worker'
                    )

                    docker.build(
                        "${IMAGE_FRONTEND}:${env.RELEASE_TAG}",
                        './services/frontend'
                    )
                }
            }
        }

        stage('Push images') {
            steps {
                script {
                    docker.withRegistry(
                        'https://index.docker.io/v1/',
                        'dockerhub-credentials'
                    ) {
                        docker.image(
                            "${IMAGE_API}:${env.RELEASE_TAG}"
                        ).push()

                        docker.image(
                            "${IMAGE_WORKER}:${env.RELEASE_TAG}"
                        ).push()

                        docker.image(
                            "${IMAGE_FRONTEND}:${env.RELEASE_TAG}"
                        ).push()
                    }
                }
            }
        }

        stage('Deploy Compose') {
            steps {
                sshagent(credentials: ['app-server-ssh']) {
                    sh '''
                        set -eu

                        install -d -m 700 "$HOME/.ssh"

                        scp \
                            -o BatchMode=yes \
                            -o ConnectTimeout=10 \
                            -o StrictHostKeyChecking=accept-new \
                            docker-compose.yml \
                            "${APP_USER}@${APP_SERVER}:/opt/fitflow/docker-compose.candidate.yml"

                        ssh \
                            -o BatchMode=yes \
                            -o ConnectTimeout=10 \
                            -o StrictHostKeyChecking=accept-new \
                            "${APP_USER}@${APP_SERVER}" \
                            "sudo -n bash -s -- '$RELEASE_TAG'" <<'REMOTE'
set -eu

cd /opt/fitflow
release_tag="$1"

# Проверяем значение перед записью в .env.
if ! [[ "$release_tag" =~ ^[0-9a-f]{12,40}-[0-9]+$ ]]; then
    echo "Invalid release tag"
    exit 1
fi

# Файл с секретами должен быть создан Ansible заранее.
test -s .env

# Эти значения имеют приоритет над тегами из .env.
export API_TAG="$release_tag"
export WORKER_TAG="$release_tag"
export FRONTEND_TAG="$release_tag"

# Проверяем новую конфигурацию без вывода секретов.
docker compose \
    --project-name fitflow \
    --env-file .env \
    -f docker-compose.candidate.yml \
    config --quiet

# Сначала скачиваем все образы.
# До завершения скачивания контейнеры не обновляются.
docker compose \
    --project-name fitflow \
    --env-file .env \
    -f docker-compose.candidate.yml \
    pull redis api worker frontend

# Обновляем только теги, сохраняя остальные настройки.
umask 077
env_tmp="$(mktemp /opt/fitflow/.env.XXXXXX)"
trap 'rm -f "$env_tmp"' EXIT

sed \
    '/^API_TAG=/d; /^WORKER_TAG=/d; /^FRONTEND_TAG=/d' \
    .env > "$env_tmp"

printf '\\nAPI_TAG=%s\\nWORKER_TAG=%s\\nFRONTEND_TAG=%s\\n' \
    "$release_tag" \
    "$release_tag" \
    "$release_tag" >> "$env_tmp"

chmod 600 "$env_tmp"
chown root:root "$env_tmp"
mv -f "$env_tmp" .env

install -o devops -g devops -m 0644 \
    docker-compose.candidate.yml docker-compose.yml

rm -f docker-compose.candidate.yml

docker compose \
    --project-name fitflow \
    --env-file .env \
    up -d --no-build --wait --wait-timeout 180

docker compose \
    --project-name fitflow \
    --env-file .env \
    ps
REMOTE
                    '''
                }
            }
        }

        stage('Verify HTTP') {
            steps {
                sh '''
                    set -eu

                    curl \
                        --noproxy '*' \
                        --fail \
                        --silent \
                        --show-error \
                        --connect-timeout 5 \
                        --max-time 15 \
                        "http://${APP_SERVER}/health"
                '''
            }
        }
    }

    post {
        success {
            echo "Версия ${env.RELEASE_TAG} успешно развернута."
        }

        failure {
            echo 'Сборка или деплой завершились ошибкой. Открой первый упавший этап в Console Output.'
        }
    }
}