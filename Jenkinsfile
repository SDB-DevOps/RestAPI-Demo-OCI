pipeline {
    agent any

    environment {
        OCI_REGISTRY = 'iad.ocir.io'
        OCI_NAMESPACE = '<your-tenancy-namespace>'
        OCI_REPO = 'python-api'
        OKE_CLUSTER_ID = '<cluster-ocid>'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/SDB-DevOps/RestAPI-Demo-OCI.git'
            }
        }

        stage('Build & Test') {
            steps {
                sh 'pip install -r app/requirements.txt'
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${OCI_REPO}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push to OCI Registry') {
            steps {
                script {
                    docker.withRegistry(
                        "https://${OCI_REGISTRY}",
                        'oci-registry-credential'
                    ) {
                        docker.image("${OCI_REPO}:${BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy to OKE') {
            steps {
                withCredentials([file(credentialsId: 'oci-kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        export KUBECONFIG=${KUBECONFIG}
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/python-api
                    """
                }
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    def LB_IP = sh(
                        script: "kubectl get svc python-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'",
                        returnStdout: true
                    ).trim()

                    sh "curl -s http://${LB_IP}/health | grep 'OK'"
                }
            }
        }
    }

    post {
        failure {
            slackSend channel: '#devops-alerts',
                message: "Build ${BUILD_NUMBER} failed: ${BUILD_URL}"
        }
        success {
            slackSend channel: '#deployments',
                message: "Successfully deployed build ${BUILD_NUMBER}: http://<your-endpoint>"
        }
    }
}