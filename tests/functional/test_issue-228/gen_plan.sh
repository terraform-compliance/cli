#! /bin/bash

set -eo pipefail

docker run --rm -v $(pwd):/app -w /app hashicorp/terraform:light init
docker run --rm -v $(pwd):/app -w /app hashicorp/terraform:light plan --out plan.out
docker run --rm -v $(pwd):/app -w /app hashicorp/terraform:light show --json plan.out | jq > plan.out.json 