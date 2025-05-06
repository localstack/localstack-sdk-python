#!/bin/bash

# Use the latest spec by default
SPEC_URL="https://raw.githubusercontent.com/localstack/openapi/refs/heads/main/openapi/emulators/localstack-spec-latest.yml"

if [ -n "$1" ]; then
  SPEC_URL="https://github.com/localstack/openapi/releases/download/v$1/localstack-spec.yml"
fi

# Check if the URL is valid
if ! wget --spider -q "$SPEC_URL"; then
    echo "Spec URL seems not accessible: $SPEC_URL"
    exit 1
fi

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli:v7.10.0 generate \
    -i "$SPEC_URL" \
    --skip-validate-spec \
    -g python \
    -o /local//packages/localstack-sdk-generated \
    --global-property models,apis,supportingFiles \
    -p packageName=localstack.sdk \
    --template-dir /local/packages/localstack-sdk-generated/templates \
    --global-property apiTests=false,modelTests=false \
    --global-property apiDocs=false,modelDocs=False
