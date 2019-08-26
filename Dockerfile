FROM python:3.7.3-slim

ARG VERSION
ARG LATEST_TERRAFORM_VERSION

LABEL terraform_compliance.version="${VERSION}"
LABEL author="Emre Erkunt <emre.erkunt@gmail.com>"
LABEL source="https://github.com/eerkunt/terraform-compliance"

ENV TERRAFORM_VERSION=${LATEST_TERRAFORM_VERSION}

RUN  apt-get update && \
     apt-get install -y git curl unzip && \
     curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip --output terraform_linux_amd64.zip && \
     unzip terraform_linux_amd64.zip -d /usr/bin && \
     pip install 'terraform-compliance==__VERSION__' && \
     pip uninstall -y radish radish-bdd && \
     pip install radish radish-bdd && \
     rm -rf /var/lib/apt/lists/* && \
     mkdir -p /target

WORKDIR /target
ENTRYPOINT ["terraform-compliance"]
