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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class LocalstackStackinfoGet200Response(BaseModel):
    """
    LocalstackStackinfoGet200Response
    """ # noqa: E501
    api_key: StrictStr
    duration_in_seconds: StrictInt
    is_ci: StrictBool
    is_docker: StrictBool
    number_of_api_calls_error: StrictInt
    number_of_api_calls_success: StrictInt
    number_of_services: StrictInt
    server_time_utc: StrictStr
    session_id: StrictStr
    system: StrictStr
    top_user_agent: StrictStr
    version: StrictStr
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["api_key", "duration_in_seconds", "is_ci", "is_docker", "number_of_api_calls_error", "number_of_api_calls_success", "number_of_services", "server_time_utc", "session_id", "system", "top_user_agent", "version"]

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
        """Create an instance of LocalstackStackinfoGet200Response from a JSON string"""
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
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of LocalstackStackinfoGet200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "api_key": obj.get("api_key"),
            "duration_in_seconds": obj.get("duration_in_seconds"),
            "is_ci": obj.get("is_ci"),
            "is_docker": obj.get("is_docker"),
            "number_of_api_calls_error": obj.get("number_of_api_calls_error"),
            "number_of_api_calls_success": obj.get("number_of_api_calls_success"),
            "number_of_services": obj.get("number_of_services"),
            "server_time_utc": obj.get("server_time_utc"),
            "session_id": obj.get("session_id"),
            "system": obj.get("system"),
            "top_user_agent": obj.get("top_user_agent"),
            "version": obj.get("version")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


