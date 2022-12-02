"""FalconPy exceptions.

 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |   CROWDSTRIKE FALCON    |::.. . |    FalconPy
`-------'                         `-------'

OAuth2 API - Customer SDK

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""
from typing import Dict, Union, Optional, List
from .._result import Result


class SDKError(Exception):
    """Base class for all errors generated by the SDK."""

    _headers: Dict[str, Optional[Union[str, int, float]]] = {}
    _code: int = 500
    _message: str = "An unexpected error has occurred."
    warning: bool = False

    def __init__(self,
                 code: int = None,
                 message: str = None,
                 headers: dict = None
                 ):
        """Construct an instance of the class."""
        self.code = self._code
        self.message = self._message
        self.headers = self._headers
        if isinstance(code, int):
            self.code = code
        if message:
            self.message = message
        if isinstance(headers, dict):
            self.headers = headers
        super().__init__(self.message)

    @property
    def result(self) -> Dict[str, Dict[str, List[str]]]:
        """Return the error result using the Result object class."""
        _body = {"errors": [{"message": f"{self.message}", "code": self.code}], "resources": []}
        return Result()(self.code, self.headers, _body)

    @property
    def simple(self) -> str:
        """Generate a simple version of the error message that includes the error code."""
        return f"ERROR: [{self.code}] {self.message}"


class RegionSelectError(SDKError):
    """Error for a region autoselection failure."""

    _code = 403
    _message = "Region autodiscovery failure. (GovCloud does not support this feature)"


class InvalidMethod(SDKError):
    """An invalid HTTP method was specified."""

    _message = "Invalid HTTP method specified."
    _code = 405


class InvalidOperation(SDKError):
    """An invalid operation was specified."""

    _message = "Invalid API operation specified."
    # That command doesn't exist. Perhaps a nice cup of tea instead?
    _code = 418


class InvalidBaseURL(SDKError):
    """The base URL specified is invalid or does not exist."""

    _message = "Invalid base URL address specified."
    _code = 400


class FunctionalityNotImplemented(SDKError):
    """This functionality is not yet implemented."""

    _message = "This functionality is not implemented"
    _code = 501


class TokenNotSpecified(SDKError):
    """A token was not provided to the revoke operation."""

    _message = "The token_value keyword is required to use this operation."
    _code = 400


class KeywordsOnly(SDKError):
    """Keyword arguments are required to use this method."""

    # I'd prefer to define this as a 400, but this has produced
    # 500's in all previous versions, so we will maintain that
    # status moving forward.
    _message = "Keyword arguments are required to use this method."


class InvalidCredentials(SDKError):
    """Invalid credentials have been specified."""

    _message = "Invalid API credentials provided."
    _code = 403


class CannotRevokeToken(SDKError):
    """Unable to revoke the token specified."""

    _message = "Unable to revoke specified token."
    # Probably an authentication error, but will fall back to a 500 if we don't know.


class PayloadValidationError(SDKError):
    """Payload validation has failed."""

    _message = "Validation failed. Please check your payloads and try this request again."
    _code = 400

    def __init__(self, msg: str = None, code: int = None):
        """Construct an instance of the exception, setting the message and code."""
        if msg:
            self._message = msg
        if isinstance(code, int):
            self._code = code
        super().__init__()


class FeatureNotSupportedByPythonVersion(SDKError):
    """This feature is not supported by your version of Python."""

    _message = "This feature is not supported by your current version of Python."
    _code = 426


class APIError(SDKError):
    """Generic error received back from the API."""

    _message = "An unexpected error has occurred. Please check your payloads and try again."
