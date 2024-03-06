pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        S3_BUCKET_NAME = 'jt-dataeng-luamaia'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-pst', url: 'https://github.com/thelua/imdb-view.git'
            }
        }

        stage('Executar main.py') {
            steps {
                script {
                    sh 'python3 main.py'
                }
            }
        }

        stage('Deploy para o S3') {
            steps {
                script {
                    withAWS(region: env.AWS_DEFAULT_REGION, credentials: 'my_aws') {
                        sh "aws s3 sync resultado/top_100_atores.csv s3://${env.S3_BUCKET_NAME}/"
                    }
                }
            }
        }
    }
}
