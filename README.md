# LocalStack Python SDK
[![PyPI version](https://img.shields.io/pypi/v/localstack-sdk-python)](https://pypi.org/project/localstack-sdk-python/)

This is the Python SDK for LocalStack.
LocalStack offers a number of developer endpoints (see [docs](https://docs.localstack.cloud/references/internal-endpoints/)).
This SDK provides a programmatic and easy way to interact with them.

> [!WARNING]
> This project is still in a preview phase and will be subject to fast and breaking changes.

### Project Structure

This project follows the following structure:

- `packages/localstack-sdk-generated` is a Python project generated from the OpenAPI specs with [openapi-generator](https://github.com/OpenAPITools/openapi-generator).
LocalStack's OpenAPI specs are available in the [openapi repository](https://github.com/localstack/openapi).
- `localstack-sdk-python` is the main project that has `localstack-sdk-generated` as the main dependency.

Developers are not supposed to modify at all `localstack-sdk-generated`.
The code needs to be re-generated from specs every time using the `generate.sh` script in the `bin` folder.

This project uses [uv](https://github.com/astral-sh/uv) as package/project manager.

### Install & Run

You can simply run `make install-dev` to install the two packages and the needed dependencies.
`make test` runs the test suite.
Note that LocalStack (pro) should be running in the background to execute the test.
