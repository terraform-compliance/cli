FROM python:3.7.3-slim

LABEL terraform_compliance.version="__VERSION__"
LABEL author="Emre Erkunt <emre.erkunt@gmail.com>"
LABEL source="https://github.com/eerkunt/terraform-compliance"

RUN  apt-get update && \
     apt-get install -y git && \
     pip install 'terraform-compliance==__VERSION__' && \
     pip uninstall -y radish radish-bdd && \
     pip install radish radish-bdd && \
     rm -rf /var/lib/apt/lists/* && \
     mkdir -p /target

WORKDIR /target
ENTRYPOINT ["terraform-compliance"]
