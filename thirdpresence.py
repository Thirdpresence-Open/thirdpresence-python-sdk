#!/usr/bin/env python
#Copyright 2012 ThirdPresence
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU Lesser General Public License for more details:
#
#<http://www.gnu.org/licenses/>.
'''
Python client library for the ThirdPresence Platform.

Simple usage example (note that you just need the auth_token):

> from thirdpresence import Thirdpresence
> tpr = Thirdpresence(auth_token)
> video_metadata_list = tpr.get_videos()
'''

import types
import requests # install by: "pip install requests"
import json

ACTIONS = {
    # ACTION: [HTTP METHOD, URL NAMESPACE, VERSION]
    "getVideos": ["GET", "video", "10-09"],
    "getVideoById": ["GET", "video", "10-09"],
    "getVideosByDesc": ["GET", "video", "10-09"],
    "getVideosByCategory": ["GET", "video", "10-09"],
    "getDeliveryStatus": ["GET", "video", "10-09"],
    "insertVideo": ["POST", "video", "10-09"],
    "deleteVideo": ["GET", "video", "10-09"],
    "updateVideoData": ["POST", "video", "10-09"],

    "listCategories": ["GET", "category", "10-09"],
    "addVideoCategory": ["GET", "category", "10-09"],
    "deleteCategory": ["GET", "category", "10-09"],
    "updateCategory": ["GET", "category", "10-09"],

    "addToken": ["GET", "auth", "04-10"],
    "removeToken": ["GET", "auth", "04-10"],

    "stitchVideos": ["POST", "ads", "06-11"],
}

class Thirdpresence(object):
    """A client for the ThirdPresence API.

    Complete API documentation available at:
    http://wiki.thirdpresence.com/index.php/API_Reference
    """
    def __init__(self, auth_token, host="api.thirdpresence.com",
                 protocol="http", forced_version=None,
                 path_prefix=None, logger=None):
        """
        @param auth_token: You get the auth_token after registering with
                           the service. Used for authentication.
        @param host: The host name for the Thirdpresence service.
        @param protocol: The protocol to use for the calls to the service.
                         Set it to 'https' if you want to use TLS.
        @param forced_version: Set this to a version number, if you want
                               to make all API calls through single API version.
        @param path_prefix: Additional path part to be added after URL host part
                            for every made request.
        @param logger: Logging Logger instance with methods like debug and info.
                       Pass logger instance for verbose output.
        """
        self.auth_token = auth_token
        self.host = host
        self.protocol = protocol
        self.forced_version = forced_version
        self.path_prefix = path_prefix
        self.logger = logger

    def _make_req(self, action, params=None, data=None):
        '''Makes a HTTP request into the ThirdPresence API.
        '''
        assert action in ACTIONS, "Invalid action: {0}".format(action)
        if params:
            assert isinstance(params, dict)
        else:
            params = {}

        method, namespace, version = ACTIONS[action]
        if self.forced_version:
            version = self.forced_version

        if method == "GET":
            func = requests.get
        elif method == "POST":
            func = requests.post
        else:
            assert False, \
                "Invalid HTTP method in actions table: {0}".format(method)

        the_path = ""
        if self.path_prefix:
            the_path += self.path_prefix.strip("/") + "/"
        the_path += "{0}/{1}".format(version, namespace)
        the_url = "{0}://{1}/{2}/".format(self.protocol, self.host, the_path)

        params["Action"] = action
        params["authToken"] = self.auth_token
        params["version"] = version

        headers = {}

        request_data = None
        if data and isinstance(data, (dict, list)):
            request_data = json.dumps(data)
            headers['content-type'] = 'application/json'
        elif data and isinstance(data, types.StringTypes):
            request_data = data
        elif data:
            assert False, "Invalid data given of type: {0}".format(type(data))

        if self.logger:
            data_len = 0
            if request_data:
                data_len = len(request_data)
            self.logger.info("Making request: {0} {1} params={2} headers={3} data_len={4}".format(
                                 method, the_url, params, headers, data_len))

        r = func(the_url, params=params, headers=headers, data=request_data)

        # pylint: disable-msg=E1103
        if self.logger:
            self.logger.info("Response: status_code={0}, reason={1}, headers={2}, json_data=\n{3}".format(
                                 r.status_code, r.reason, r.headers, r.json))

        self._validate_status(r.status_code, r.reason, r.json)
        return r.status_code, r.reason, r.headers, r.json

    def _validate_status(self, status_code, reason=None, json_data=None):
        '''Checks the HTTP status code and throws an exception if
        the status is not OK.
        '''
        if status_code >= 200 and status_code < 300:

            if json_data and isinstance(json_data, dict) \
                   and str(json_data.get("errorresponse")).lower() == "true":
                internal_error_code = int(json_data["code"])
                err_message = str(json_data["message"])
                if internal_error_code not in INTERNAL_ERROR_CODES:
                    raise ThirdpresenceAPIError("Unknown internal error. "\
                        "Code {0}. Message:".format(internal_error_code,
                                                    err_message))
                else:
                    exception = INTERNAL_ERROR_CODES[internal_error_code]
                    raise exception("{0}: {1}".format(internal_error_code,
                                                      err_message))

            else:
                pass # HTTP code 2XX, meaning this is OK non-error response.

        elif status_code == 404:
            raise ResourceNotFoundError(str(reason))

        elif status_code >= 500 and status_code < 600:
            raise InternalServerError(str(reason))

        else:
            raise ThirdpresenceAPIError(
                "HTTP status: {0}, reason: {1}".format(status_code, reason))

    def _optional_params_dict(self, param1, value1, param2, value2,
                                 typecast_func):
        '''This method gives a params dict with one of the given params.
        Commonly used pattern in ThirdPresence API is to ask for
        two parameters for which only one of them must be given.
        '''
        if value1:
            params = {param1: typecast_func(value1)}
        elif value2:
            params = {param2: typecast_func(value2)}
        else:
            assert False, "Give either {0} or {1}".format(param1, param2)
        return params

    def get_videos(self, item_count=0):
        '''Gets the latest videos of an account.

        @param item_count: The amount of items to return
        @return List of video metadata in JSON format.
        '''
        params = {"itemCount": item_count}
        _, _, _, json_data = self._make_req("getVideos", params)
        return json_data

    def get_video_by_id(self, video_id, provider_id=None):
        '''Gets the metadata of a video by the given id.
        You must give either video_id or provider_id, but not both.

        @param video_id: The ID of a video object.
        @param provider_id: The ID of a provider for a video.
        @return The metadata of a video in JSON format.
        '''
        params = self._optional_params_dict("videoId", video_id,
                                            "providerId", provider_id, int)
        _, _, _, json_data = self._make_req("getVideoById", params)
        return json_data

    def get_videos_by_desc(self, text):
        '''Gets a list of metadata if the given text appears in
        the video description.

        @param text: Search string for video description.
        @return List of video metadata in JSON format.
        '''
        assert isinstance(text, types.StringTypes) and len(text) < 256, \
               "Invalid or no search text given"
        params = {"text": text}
        _, _, _, json_data = self._make_req("getVideosByDesc", params)
        return json_data

    def get_videos_by_category(self, category_id, provider_id=None):
        '''Gets a list of metadata for all videos in given category.
        You must give either category_id or provider_id, but not both.

        @param category_id: The ID of a video category.
        @param provider_id: The ID of a provider for a video.
        @return List video metadata in JSON format.
        '''
        params = self._optional_params_dict("categoryId", category_id,
                                            "providerId", provider_id, int)
        _, _, _, json_data = self._make_req("getVideosByCategory", params)
        return json_data

    def get_delivery_status(self, video_id, provider_id=None):
        '''Gets the status of a video by video or provider id.
        You must give either video_id or provider_id, but not both.

        Returned status is one of the following values:
        ACTIVE
        PROCESSING
        INACTIVE
        ERROR
        REMOVED

        @param video_id: The ID of a video category.
        @param provider_id: The ID of a provider for a video.
        @return List video metadata in JSON format.
        '''
        params = self._optional_params_dict("videoId", video_id,
                                            "providerId", provider_id, int)
        _, _, _, json_data = self._make_req("getDeliveryStatus", params)
        return json_data

    def insert_video(self, video_metadata):
        '''Inserts a video into the user's account.
        You must pass the video metadata as a dictionary and it will
        be encoded as JSON payload into the HTTP request.

        Example video metadata dict:
        {
            "name": "James Sanders provoca",
            "synopsis": False,
            "position": 0,
            "expiretime": "10.03.2012 02:17:08",
            "description": "Some description",
            "sourceurl": "http://somehost\/EXAMPLE.mp4",
            "categoryid": 1179
        }

        @param video_metadata: A dictionary with the video metadata.
        @return The metadata of the added video in JSON format.
        '''
        _, _, _, json_data = \
                self._make_req("insertVideo", None, video_metadata)
        return json_data

    def delete_video(self, video_id, provider_id=None):
        '''Deletes a video from the user's account by the given id.
        You must give either video_id or provider_id, but not both.

        @param video_id: The ID of a video object.
        @param provider_id: The ID of a provider for a video.
        @return True, if the video was deleted, and None otherwise.
        '''
        params = self._optional_params_dict("videoId", video_id,
                                            "providerId", provider_id, int)
        _, _, _, json_data = self._make_req("deleteVideo", params)
        return json_data

    def update_video_data(self, video_metadata):
        '''Updates video metadata.
        You must pass the video metadata as a dictionary and it will
        be encoded as JSON payload into the HTTP request.

        @param video_metadata: A dictionary with the video metadata.
        @return The metadata of the added video in JSON format.
        '''
        _, _, _, json_data = \
                self._make_req("updateVideoData", None, video_metadata)
        return json_data

    def list_categories(self):
        '''Gets the categories for an account.

        @return List of category metadata in JSON format.
        '''
        _, _, _, json_data = self._make_req("listCategories")
        return json_data

    def add_video_category(self, name, provider_id=None, source_url=None):
        '''Adds a new video category with the given content.
        The source_url must point to a collection of videos, e.g.
        in ThirdPresence's own FTP or customer's own RSS. See:
        http://wiki.thirdpresence.com/index.php/Uploading_content_using_RSS

        @param name: The name of the new category.
        @param provider_id: Customer's own ID, the provider_id for videos.
        @param source_url: Source for the video feed. See the comment above.
        @return Added category metadata in JSON format.
        '''
        params = {"name": name}
        if provider_id:
            params["providerId"] = provider_id
        if source_url:
            params["sourceurl"] = source_url
        _, _, _, json_data = self._make_req("addVideoCategory", params)
        return json_data

    def delete_category(self, category_id, delete_content, provider_id=None):
        '''Deletes a video category with the given category_id.
        If the delete_content is True, then all the content in this
        category will be deleted also. If delete_content is False,
        then all the content will be moved to the default category.

        @param category_id: The ID of a video category.
        @param delete_content: True or False, i.e. whether to delete
                               also the content in the deleted category.
        @param provider_id: The provider_id for videos.
        @return Simple message stating whether the content was deleted.
        '''
        params = {"categoryId": category_id, "deleteContent": delete_content}
        if provider_id:
            params["providerId"] = provider_id
        _, _, _, json_data = self._make_req("deleteCategory", params)
        return json_data

    def update_category(self, category_id, name=None, provider_id=None,
                        source_url=None):
        '''Updates a video category with the given metadata.
        The source_url must point to a collection of videos, e.g.
        in ThirdPresence's own FTP or customer's own RSS. See:
        http://wiki.thirdpresence.com/index.php/Uploading_content_using_RSS

        @param category_id: The ID of the video category that will be updated.
        @param name: The new name for the category.
        @param provider_id: Customer's own ID, the provider_id for videos.
        @param source_url: Source for the video feed. See the comment above.
        @return Added category metadata in JSON format.
        '''
        params = {"categoryId": category_id}
        if name:
            params["name"] = name
        if provider_id:
            params["providerId"] = provider_id
        if source_url:
            params["sourceurl"] = source_url
        _, _, _, json_data = self._make_req("updateCategory", params)
        return json_data

    def add_token(self, video_id, content_auth_token, provider_id=None):
        '''Adds an authorization token for a video.

        @param video_id: The ID of a video object.
        @param content_auth_token: Authentication token as a string.
        @param provider_id: The ID of a provider for a video.
        '''
        assert isinstance(content_auth_token, types.StringTypes) \
                   and len(content_auth_token) < 256, \
               "Invalid authentication token given."
        params = self._optional_params_dict("videoId", video_id,
                                            "providerId", provider_id, int)
        params["contentAAToken"] = content_auth_token
        _, _, _, json_data = self._make_req("addToken", params)
        return json_data

    def remove_token(self, video_id, content_auth_token, provider_id=None):
        '''Remove an authorization token for a video.

        @param video_id: The ID of a video object.
        @param content_auth_token: Authentication token as a string.
        @param provider_id: The ID of a provider for a video.
        '''
        assert isinstance(content_auth_token, types.StringTypes) \
                   and len(content_auth_token) < 256, \
               "Invalid authentication token given."
        params = self._optional_params_dict("videoId", video_id,
                                            "providerId", provider_id, int)
        params["contentAAToken"] = content_auth_token
        _, _, _, json_data = self._make_req("removeToken", params)
        return json_data

    def stitch_videos(self, video_metadata):
        '''Concatenates two videos based on the given metadata.
        Mainly used for adding a preroll advertisement to a video.
        Notice that the sourceurl and adurl are video_ids already
        existing in the ThirdPresence service.

        You must pass the video metadata as a dictionary and it will
        be encoded as JSON payload into the HTTP request.

        Example video metadata dict:
        {
            "name": "James Sanders provoca with preroll",
            "synopsis": False,
            "position": 0,
            "expiretime": "10.03.2012 02:17:08",
            "description": "Some description",
            "sourceurl": "300001",
            "adurl": "300002",
            "categoryid": 1179
        }

        @param video_metadata: A dictionary with the video metadata.
        '''
        _, _, _, json_data = \
                self._make_req("stitchVideos", None, video_metadata)
        return json_data


class ThirdpresenceAPIError(StandardError):
    '''All errors thrown by the Thirdpresence SDK are extended from
    this error class.'''
    pass

# Thrown if returned HTTP code is 404.
class ResourceNotFoundError(ThirdpresenceAPIError):
    pass

# Thrown if returned HTTP code starts with 500.
class InternalServerError(ThirdpresenceAPIError):
    pass

class ObjectNotFoundError(ThirdpresenceAPIError):
    pass

class ObjectReferenceError(ThirdpresenceAPIError):
    pass

class InputParseError(ThirdpresenceAPIError):
    pass

# ThirdPresence API returns ErrorItem JSON object with HTTP code 200,
# if the service can process the request but has logical problems processing it.
INTERNAL_ERROR_CODES = {
    # Category with same name or reference id already exists.
    100: ObjectReferenceError,

    # Content category id must be a number.
    101: InputParseError,

    # Content category not empty. Cannot delete.
    102: ObjectReferenceError,

    # Content category could not be deleted.
    103: ObjectReferenceError,

    # No valid reference to category.
    104: InputParseError,

    # VideoId must be a number.
    200: InputParseError,

    # No valid reference to video.
    201: ObjectReferenceError,

    # Content could not be deleted.
    202: ObjectReferenceError,

    # Content could not be created. Reference id already in use.
    203: ObjectReferenceError,

    # No sourceurl for video.
    204: InputParseError,

    # Account has no category where to insert video.
    205: ObjectReferenceError,

    # Content could not be created.
    206: ObjectReferenceError,

    # Could not parse JSON object.
    301: InputParseError,

    # Could not found content item.
    404: ObjectNotFoundError,
}
