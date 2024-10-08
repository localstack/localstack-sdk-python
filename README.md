# LocalStack Python SDK

This repository is a PoC for generating a Python SDK for the LocalStack public endpoint.

### Generate the spec

The first step is to generate the `openapi.yaml` spec.
We have a script in `scripts/create_spec.py`
- [ ] todo: fix the script; make sure it also fetches ext spec;
`localstack-core` and `localstack-ext` are part of the dev dependencies for this very step.

### Generate the code
We use openapi-generator from `openapitools`.
To run the generation, run `./bin/generate.sh`.
The script uses the docker image of the CLI and use the `openapi.yaml` file as input.
By default, the generator creates a bunch of files, but the most important things are:
- `api` package: with the all APIs categorized by tags;
- `models` package: with the methods derived from the components or the inline specs;
- [ ] the code from the inline components is much uglier, but we can overwrite some naming with come config (or move to components).

The python generator by default creates 3 functions for each path:
- a normal function (the name is taken from the `operationId` in the specs) just with the validated response payload;
- a function suffixed by `without_preloaded_content`: where the JSON responses are not validated;
- a function suffixed by `with_http_info` which also returns the response header and status.

The code in these `api` files (but also in any other generated artifacts), can be modified by providing custom mustache templates.
[These](https://github.com/OpenAPITools/openapi-generator/tree/master/modules/openapi-generator/src/main/resources/python) are the
default for Python.
Templates are not super immediate, but looking at them and at the generated code you can do it.
For instance, I deleted the `without_preloaded_content` and `with_http_info` generated functions.

### Supporting files
The generated code uses some supporting files, i.e., some utilities that are responsible of making the actual HTTP calls,
validating and parsing the responses.
I just checked in this code and take it as granted, but I am pretty sure we can come up with some simpler code and avoid
to generate this part (would move out from `generated`).
- [ ] see if I can write my own api client and all the necessary supporting code.

### TODO
- [ ] understand if this can be viable at all;
- [ ] devise a way to update the spec automatically and regenerate every time the code in `generated`;
- much more...fill this list up