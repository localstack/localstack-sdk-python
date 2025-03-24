#!/bin/bash

LATEST_SPEC="https://raw.githubusercontent.com/localstack/openapi/refs/heads/main/openapi/emulators/localstack-spec-latest.yml"
SPEC_URL="${1:-$LATEST_SPEC}"

# Check if the URL is valid
if ! wget --spider -q "$SPEC_URL"; then
    echo "Spec URL seems not accessible: $SPEC_URL"
    exit 1
fi

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli:v7.10.0 generate \
    -i "$LATEST_SPEC" \
    --skip-validate-spec \
    -g python \
    -o /local//packages/localstack-sdk-generated \
    --global-property models,apis,supportingFiles \
    -p packageName=localstack.sdk \
    --template-dir /local/packages/localstack-sdk-generated/templates \
    --global-property apiTests=false,modelTests=false \
    --global-property apiDocs=false,modelDocs=False
