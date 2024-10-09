#!/bin/bash

version=$(cat VERSION)

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli:v7.9.0 generate \
    -i /local/openapi.yaml \
    --skip-validate-spec \
    -g python \
    -o /local//packages/localstack-sdk-generated \
    --global-property models,apis,supportingFiles \
    -p packageName=localstack.sdk \
    -p packageVersion=$version \
    --template-dir /local/packages/localstack-sdk-generated/templates \
    --global-property apiTests=false,modelTests=false \
    --global-property apiDocs=false,modelDocs=False
