#!/usr/bin/env groovy

pipeline {
  agent any

  options {
    timeout(time: 30, unit: 'MINUTES')
  }

  triggers {
    cron('H 4 * * *')
  }

  stages {
    stage('Build and push CTT Agent Base image') {
      steps {
        script {
          dockerImage = docker.build("radonconsortium/radon-ctt-agent:base")
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium') {
            dockerImage.push("base")
          }
        }
      }
    }
  }
}
