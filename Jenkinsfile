pipeline {
    agent any
    
    stages {
    stage('Checkout') {
        steps {
            script {
                git branch: 'main', credentialsId: 'meu-git', url: 'https://github.com/thelua/imdb-view.git'
            }
        }
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
                    withAWS(region:'us-east-1', credentials: 'my-aws') {
                        s3Upload(bucket: 'jt-dataeng-luamaia', file: 'resultado/top_100_atores.csv')
                    }
                }
            }
        }
    }
}
