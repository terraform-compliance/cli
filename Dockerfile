FROM python:3.7.10-slim

ARG VERSION
ARG LATEST_TERRAFORM_VERSION

ARG HASHICORP_PGP_KEY
ARG TARGET_ARCH='linux_amd64'

LABEL terraform_compliance.version="${VERSION}"
LABEL author="Emre Erkunt <emre.erkunt@gmail.com>"
LABEL source="https://github.com/eerkunt/terraform-compliance"

ENV TERRAFORM_VERSION=${LATEST_TERRAFORM_VERSION}
ENV TARGET_ARCH="${TARGET_ARCH}"
ENV HASHICORP_PGP_KEY="${HASHICORP_PGP_KEY}"

RUN  set -ex \
     && BUILD_DEPS='wget unzip gpg' \
     && RUN_DEPS='git' \
     && apt-get update \
     && apt-get install -y ${BUILD_DEPS} ${RUN_DEPS} \
     && TERRAFORM_FILE_NAME="terraform_${TERRAFORM_VERSION}_${TARGET_ARCH}.zip" \
     && SHA256SUM_FILE_NAME="terraform_${TERRAFORM_VERSION}_SHA256SUMS" \
     && SHA256SUM_SIG_FILE_NAME="terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig" \
     && SHA256SUM_FILE_NAME_FOR_ARCH="${SHA256SUM_FILE_NAME}.${TARGET_ARCH}" \
     && HASHICORP_PGP_KEY_FILE='hashicorp-pgp-key.pub' \
     && OLD_BASEDIR="$(pwd)" \
     && TMP_DIR=$(mktemp -d) \
     && cd "${TMP_DIR}" \
     && echo "${HASHICORP_PGP_KEY}" > "${HASHICORP_PGP_KEY_FILE}" \
     && wget -q "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${SHA256SUM_FILE_NAME}" \
     && wget -q "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${SHA256SUM_SIG_FILE_NAME}" \
     && gpg --import "${HASHICORP_PGP_KEY_FILE}" \
     && gpg --verify "${SHA256SUM_SIG_FILE_NAME}" "${SHA256SUM_FILE_NAME}" \
     && wget -q "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${TERRAFORM_FILE_NAME}" \
     && grep "${TERRAFORM_FILE_NAME}" "${SHA256SUM_FILE_NAME}" > "${SHA256SUM_FILE_NAME_FOR_ARCH}" \
     && ls -al . \
     && sha256sum -c "${SHA256SUM_FILE_NAME_FOR_ARCH}" \
     && unzip "${TERRAFORM_FILE_NAME}" \
     && install terraform /usr/bin/ \
     && cd "${OLD_BASEDIR}" \
     && unset OLD_BASEDIR \
     && rm -vrf ${TMP_DIR} \
     && pip install --upgrade pip \
     && pip install "terraform-compliance[faster_parsing]==${VERSION}" \
     && apt-get remove -y ${BUILD_DEPS} \
     && apt-get autoremove -y \
     && apt-get clean -y \
     && rm -rf /var/lib/apt/lists/* \
     && mkdir -p /target

RUN echo "Host *" >> /etc/ssh/ssh_config
RUN echo " StrictHostKeyChecking no" >> /etc/ssh/ssh_config

WORKDIR /target
ENTRYPOINT ["terraform-compliance"]
