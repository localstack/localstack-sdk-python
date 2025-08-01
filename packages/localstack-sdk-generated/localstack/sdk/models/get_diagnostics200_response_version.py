# coding: utf-8

"""
    LocalStack REST API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 4.7.0
    Contact: info@localstack.cloud
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from localstack.sdk.models.get_diagnostics200_response_version_host import GetDiagnostics200ResponseVersionHost
from localstack.sdk.models.get_diagnostics200_response_version_image_version import GetDiagnostics200ResponseVersionImageVersion
from localstack.sdk.models.get_diagnostics200_response_version_localstack_version import GetDiagnostics200ResponseVersionLocalstackVersion
from typing import Optional, Set
from typing_extensions import Self

class GetDiagnostics200ResponseVersion(BaseModel):
    """
    GetDiagnostics200ResponseVersion
    """ # noqa: E501
    host: GetDiagnostics200ResponseVersionHost
    image_version: GetDiagnostics200ResponseVersionImageVersion = Field(alias="image-version")
    localstack_version: GetDiagnostics200ResponseVersionLocalstackVersion = Field(alias="localstack-version")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["host", "image-version", "localstack-version"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GetDiagnostics200ResponseVersion from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * Fields in `self.additional_properties` are added to the output dict.
        """
        excluded_fields: Set[str] = set([
            "additional_properties",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of host
        if self.host:
            _dict['host'] = self.host.to_dict()
        # override the default output from pydantic by calling `to_dict()` of image_version
        if self.image_version:
            _dict['image-version'] = self.image_version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of localstack_version
        if self.localstack_version:
            _dict['localstack-version'] = self.localstack_version.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetDiagnostics200ResponseVersion from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "host": GetDiagnostics200ResponseVersionHost.from_dict(obj["host"]) if obj.get("host") is not None else None,
            "image-version": GetDiagnostics200ResponseVersionImageVersion.from_dict(obj["image-version"]) if obj.get("image-version") is not None else None,
            "localstack-version": GetDiagnostics200ResponseVersionLocalstackVersion.from_dict(obj["localstack-version"]) if obj.get("localstack-version") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


