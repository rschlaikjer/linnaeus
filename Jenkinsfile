node {

    def app

    stage('Clone repository') {
        checkout scm
        sh "git rev-parse origin/${sha1} > .commit"
    }

    stage('Build image') {
        app = docker.build("linnaeus")
    }

    stage('Push image') {
        def commit = readFile('.commit').trim()
        docker.withRegistry('http://docker-registry:5000') {
            app.push("${commit}")
            app.push("${sha1}")
            app.push("latest")
        }

        sh "docker image prune -fa --filter 'until=240h'"
    }

    stage('Kubernetes Deploy') {
        def commit = readFile('.commit').trim()
        sh "docker run --rm lachlanevenson/k8s-kubectl:v1.7.8 \
        --server=http://192.168.0.1:8080 \
        --username=default \
        set image deployment/linnaeus-deployment \
        linnaeus=docker-registry:5000/linnaeus:${commit}"

        sh "docker run --rm lachlanevenson/k8s-kubectl:v1.7.8 \
        --server=http://192.168.0.1:8080 \
        --username=default \
        rollout status deployment/linnaeus-deployment"
    }

}

