# LocalStack Python SDK

This is the Python SDK for LocalStack.
LocalStack offers a number of developer endpoints (see [docs](https://docs.localstack.cloud/references/internal-endpoints/)).
This SDK provides a programmatic and easy way to interact with them.

> [!WARNING]
> This project is still in a preview phase, and will be subject to fast and breaking changes.

### Project Structure

This project follows the following structure:

- `packages/localstack-sdk-generated` is a python project generated from the OpenAPI specs with [openapi-generator](https://github.com/OpenAPITools/openapi-generator).
- `localstack-sdk-python` is the main project that has `localstack-sdk-generated` has the main dependency.

Developers are not supposed to modify at all `localstack-sdk-generated`.
The code needs to be every time re-generated from specs using the `generate.sh` script in the `bin` folder.

This project uses [uv](https://github.com/astral-sh/uv) as package/project manager.

### Install & Run

You can simply run `make install-dev` to install the two packages and the needed dependencies.
`make test` runs the test suite.
Note that LocalStack (pro) should be running in the background to execute the test.
