# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, List, Optional, Union

from src.model.checksum import Checksum
from src.model.file import File, FileType
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import append_parsed_field_or_log_error, \
    raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error, parse_field_or_log_error
from src.parser.json.license_expression_parser import LicenseExpressionParser
from src.parser.logger import Logger


class FileParser:
    logger: Logger
    checksum_parser: ChecksumParser
    license_expression_parser: LicenseExpressionParser

    def __init__(self):
        self.logger = Logger()
        self.checksum_parser = ChecksumParser()
        self.license_expression_parser = LicenseExpressionParser()

    def parse_files(self, file_dict_list) -> List[File]:
        file_list = []
        for file_dict in file_dict_list:
            file_list = append_parsed_field_or_log_error(list_to_append_to=file_list,
                                                         logger=self.logger, field=file_dict,
                                                         method_to_parse=self.parse_file)
        raise_parsing_error_if_logger_has_messages(self.logger)
        return file_list

    def parse_file(self, file_dict: Dict) -> Optional[File]:
        logger = Logger()
        name: str = file_dict.get("fileName")
        spdx_id: str = file_dict.get("SPDXID")
        checksums_list: List[Dict] = file_dict.get("checksums")

        checksums: List[Checksum] = parse_field_or_log_error(logger=logger, field=checksums_list,
                                                             parsing_method=self.checksum_parser.parse_checksums)

        attribution_texts: Optional[str] = file_dict.get("attributionTexts")
        comment: Optional[str] = file_dict.get("comment")
        copyright_text: Optional[str] = file_dict.get("copyrightText")
        file_contributors: List[str] = file_dict.get("fileContributors")
        file_types: List[FileType] = parse_field_or_log_error(logger=logger, field=file_dict.get("fileTypes"),
                                                              parsing_method=self.parse_file_types, optional=True)

        license_comments: Optional[str] = file_dict.get("licenseComments")

        license_concluded: Optional[Union[
            LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger=logger, field=file_dict.get("licenseConcluded"),
            parsing_method=self.license_expression_parser.parse_license_expression, optional=True)

        license_info_in_files: Optional[
            Union[List[
                LicenseExpression], SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger=logger, field=file_dict.get("licenseInfoInFiles"),
            parsing_method=self.license_expression_parser.parse_license_expression, optional=True)
        notice_text: Optional[str] = file_dict.get("noticeText")
        raise_parsing_error_if_logger_has_messages(logger, f"file {name}")

        file = construct_or_raise_parsing_error(File, dict(name=name, spdx_id=spdx_id, checksums=checksums,
                                                           attribution_texts=attribution_texts,
                                                           comment=comment, copyright_text=copyright_text,
                                                           file_type=file_types, contributors=file_contributors,
                                                           license_comment=license_comments,
                                                           concluded_license=license_concluded,
                                                           license_info_in_file=license_info_in_files,
                                                           notice=notice_text)
                                                )
        return file

    @staticmethod
    def parse_file_types(file_types_list: List[str]) -> List[FileType]:
        logger = Logger()
        file_types = []
        for file_type in file_types_list:
            try:
                file_type = FileType[file_type]
            except KeyError:
                logger.append(f"FileType {file_type} is not valid.")
                continue
            file_types.append(file_type)
        raise_parsing_error_if_logger_has_messages(logger, "file_types")
        return file_types