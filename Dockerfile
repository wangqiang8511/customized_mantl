FROM centos:7

ENV TERRAFORM_VERSION 0.5.3
ENV TERRAFORM_STATE_ROOT /state

RUN mkdir -p /tmp/terraform/ && \
    cd /tmp/terraform/ && \
    curl -SLO https://dl.bintray.com/mitchellh/terraform/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    cd /usr/local/bin/ && \
    yum install -y unzip && \
    unzip /tmp/terraform/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    rm -rf /tmp/terraform/ && \
    yum remove -y unzip && \
    yum -y clean all

# install all dependencies
COPY requirements.txt /mi/
RUN yum install -y epel-release
RUN yum install -y python-pip python-crypto openssl openssh-clients && \
    pip install -U -r /mi/requirements.txt

# load microservices-infrastructure and default setup
COPY . /mi/

# load user custom setup
ONBUILD COPY ssl/ /mi/ssl/
ONBUILD COPY security.yml /mi/security.yml
ONBUILD COPY terraform.yml /mi/terraform.yml
ONBUILD COPY *.tf /mi/

RUN mkdir -p /state
VOLUME /state /ssh

WORKDIR /mi
CMD ["/mi/docker_launch.sh"]
