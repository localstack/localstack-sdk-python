#!/bin/bash

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i /local/openapi.yaml \
    --skip-validate-spec \
    -g python \
    -o /local/localstack-sdk-generated \
    --global-property models,apis,supportingFiles \
    -p packageName=localstack \
    --template-dir /local/localstack-sdk-generated/templates \
    --global-property apiTests=false,modelTests=false \
    --global-property apiDocs=false,modelDocs=False
