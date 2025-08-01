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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from localstack.sdk.models.ses_destination import SESDestination
from localstack.sdk.models.ses_sent_email_body import SesSentEmailBody
from typing import Optional, Set
from typing_extensions import Self

class SesSentEmail(BaseModel):
    """
    SesSentEmail
    """ # noqa: E501
    body: Optional[SesSentEmailBody] = Field(default=None, alias="Body")
    destination: Optional[SESDestination] = Field(default=None, alias="Destination")
    id: StrictStr = Field(alias="Id")
    raw_data: Optional[StrictStr] = Field(default=None, alias="RawData")
    region: StrictStr = Field(alias="Region")
    source: StrictStr = Field(alias="Source")
    subject: Optional[StrictStr] = Field(default=None, alias="Subject")
    template: Optional[StrictStr] = Field(default=None, alias="Template")
    template_data: Optional[StrictStr] = Field(default=None, alias="TemplateData")
    timestamp: StrictStr = Field(alias="Timestamp")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["Body", "Destination", "Id", "RawData", "Region", "Source", "Subject", "Template", "TemplateData", "Timestamp"]

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
        """Create an instance of SesSentEmail from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of body
        if self.body:
            _dict['Body'] = self.body.to_dict()
        # override the default output from pydantic by calling `to_dict()` of destination
        if self.destination:
            _dict['Destination'] = self.destination.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SesSentEmail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "Body": SesSentEmailBody.from_dict(obj["Body"]) if obj.get("Body") is not None else None,
            "Destination": SESDestination.from_dict(obj["Destination"]) if obj.get("Destination") is not None else None,
            "Id": obj.get("Id"),
            "RawData": obj.get("RawData"),
            "Region": obj.get("Region"),
            "Source": obj.get("Source"),
            "Subject": obj.get("Subject"),
            "Template": obj.get("Template"),
            "TemplateData": obj.get("TemplateData"),
            "Timestamp": obj.get("Timestamp")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


