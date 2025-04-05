provider "aws" {
    region = "eu-west-3"
}

terraform {
    backend "s3" {
        bucket = "financeguy-tf-state-ew3"
        key    = "tf.tfstate"
        region = "eu-west-3"
    }
}

data "aws_security_group" "jenkins_sg" {
    name = "jenkins-sg"
}

resource "aws_instance" "jenkins_server" {
    ami             = "ami-08461dc8cd9e834e0"
    instance_type   = "t3.medium"
    key_name        = "aws_ssh_key"

    vpc_security_group_ids = [data.aws_security_group.jenkins_sg.id]

    tags = {
        Name = "Jenkins-Server"
    }

user_data = <<-EOF
        #!/bin/bash
        set -e
        exec > /var/log/user-data.log 2>&1  # Capture des logs dans /var/log/user-data.log

        echo "Mise à jour du système..."
        dnf update -y

        echo "Installation des dépendances..."
        dnf install -y git java-17-amazon-corretto wget

        echo "Installation de Jenkins..."
        wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
        rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key || true
        dnf install -y jenkins --nogpgcheck
        systemctl enable --now jenkins
        systemctl status jenkins --no-pager || echo "Jenkins ne démarre pas correctement"

        echo "Installation de containerd..."
        dnf install -y containerd
        systemctl enable --now containerd
        systemctl status containerd --no-pager || echo "containerd ne démarre pas correctement"

        echo "Installation de K3s..."
        curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--container-runtime-endpoint unix:///run/containerd/containerd.sock" sh -
        
        echo "Configuration des permissions pour K3s..."
        chmod 644 /etc/rancher/k3s/k3s.yaml
        chown ec2-user:ec2-user /etc/rancher/k3s/k3s.yaml

        echo "Attente avant la vérification des nœuds..."
        sleep 30

        echo "Vérification des nœuds K3s..."
        kubectl get nodes || echo "kubectl ne répond pas"

        echo "Installation terminée avec succès !"
    EOF
}
