# LocalStack Python SDK
[![PyPI version](https://img.shields.io/pypi/v/localstack-sdk-python)](https://pypi.org/project/localstack-sdk-python/)
[![Integration Tests](https://github.com/localstack/localstack-sdk-python/actions/workflows/test.yml/badge.svg)](https://github.com/localstack/localstack-sdk-python/actions/workflows/test.yml)

This is the Python SDK for LocalStack.
LocalStack offers a number of developer endpoints (see [docs](https://docs.localstack.cloud/references/internal-endpoints/)).
This SDK provides a programmatic and easy way to interact with them.

> [!WARNING]
> This project is still in a preview phase and will be subject to fast and breaking changes.

### Project Structure

This project is composed by two Python packages:

- `packages/localstack-sdk-generated`: generated from the LocalStack's OpenAPI specs with [openapi-generator](https://github.com/OpenAPITools/openapi-generator).
The LocalStack's OpenAPI specs are available in [localstack/openapi](https://github.com/localstack/openapi).
This package is not meant to be manually modified, as it needs to be generated every time from the specs.
- `localstack-sdk-python`: the user-facing SDK that consumed `localstack-sdk-generated` as its main dependency.

### Installation

You can install the LocalStack Python SDK with `pip`:

```shell
pip install localstack-sdk-python
```

#### From Source

This project uses [uv](https://github.com/astral-sh/uv) as a package manager.
On a Unix system, you can install `uv` with the standalone installer:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once `uv` is installed, you can install the project from source with:

```shell
make install
```

To run the integration test suite:

```shell
make test
```

Note that LocalStack Pro (with the same version as the SDK) should be running in the background to execute the test.

### Quickstart

To get started with our SDK, check out the [official documentation on https://docs.localstack.cloud](https://docs.localstack.cloud/user-guide/tools/localstack-sdk/python/). 
You'll find comprehensive guides and detailed code samples that demonstrate how to use the various features provided
by the SDK.
