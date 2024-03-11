pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/thelua/imdb-view.git'
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
                        s3Upload(bucket: 'jt-dataeng-luamaia', file: 'resultado/top_100_atores.csv')
                    }
                }
            }
        }
    }
}
