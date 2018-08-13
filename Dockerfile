FROM python:2.7.15-slim

LABEL terraform_compliance.version="0.3.0"
LABEL author="Emre Erkunt <emre.erkunt@gmail.com>"
LABEL source="https://github.com/eerkunt/terraform-compliance"

RUN  apt-get update && \
     apt-get install -y git && \
     pip install terraform-compliance && \
     pip uninstall -y radish radish-bdd && \
     pip install radish radish-bdd && \
     rm -rf /var/lib/apt/lists/* && \
     mkdir -p /target

WORKDIR /target
ENTRYPOINT ["terraform-compliance"]
