provider "aws" {
    region = "eu-north-1"
}

terraform {
    backend "s3" {
        bucket = "financeguy-tf-state"
        key = "tf.tfstate"
        region = "eu-north-1"
    }
}

resource "aws_instance" "jenkins_server" {
    ami = "ami-087fba4aa07ebd20f"
    instance_type = "t3.micro"
    key_name = "aws_ssh_key"

    tags = {
        Name = "Jenkins-Server"
    }
}