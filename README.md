Thirdpresence-Python-SDK
========================

Python SDK for the Thirdpresence API.

Thirdpresence HTTP API can be found from:
http://wiki.thirdpresence.com/index.php/API_Reference

You need the authentication token given by ThirdPresence when you
registered for the ThirdPresence service. The token is available
in your management console in the API tab. Log into the console from:
http://console.thirdpresence.com

Following examples can be run as they are in the Python prompt.
Python versions 2.6.x and 2.7.x are supported.


Getting Help on Module:
-----------------------

    from thirdpresence import Thirdpresence
    help(Thirdpresence)

    Help on class Thirdpresence in module thirdpresence:
    
    class Thirdpresence(__builtin__.object)
     |  A client for the ThirdPresence API.
     |
     |  Complete API documentation available at:
     |  http://wiki.thirdpresence.com/index.php/API_Reference
     |
     |  Methods defined here:
     |
     |  __init__(self, auth_token, host='api.thirdpresence.com', protocol='http', fo
    rced_version=None)
     |      @param auth_token: You get the auth_token after registering with
     |                         the service. Used for authentication.
     |      @param host: The host name for the Thirdpresence service.
     |      @param protocol: The protocol to use for the calls to the service.
     |                       Set it to 'https' if you want to use TLS.
     |      @param forced_version: Set this to a version number, if you want
     |                             to make all API calls through single API version.
     |
     |  add_token(self, video_id, content_auth_token, provider_id=None)
     |      Adds an authorization token for a video.
     |
     |      @param video_id: The ID of a video object.
     |      @param content_auth_token: Authentication token as a string.
     |      @param provider_id: The ID of a provider for a video.
     |      @return TODO: what is returned?
     |
     |  add_video_category(self, name, provider_id=None, source_url=None)
     |      Adds a new video category with the given content.
     |      The source_url must point to a collection of videos, e.g.
     |      in ThirdPresence's own FTP or customer's own RSS. See:
     |      http://wiki.thirdpresence.com/index.php/Uploading_content_using_RSS
     |
     |      @param name: The name of the new category.
     |      @param provider_id: Customer's own ID, the provider_id for videos.
     |      @param source_url: Source for the video feed. See the comment above.
     |      @return Added category metadata in JSON format.
     |
     |  create_new_sub_account(self, account_name, password, callback=None)
     |      Creates a new sub-account for a reseller account.
     |      
     |      Created name for new account will be the reseller account prefixed
     |      by the new given account name.
     |      
     |      @param account_name: The name for the new sub-account.
     |      @param password: Password for the new account console and statistics.
     |      @param callback: Callback URL to be called when a new updated video
     |                       for the account becomes available.
     |      @return: Newly created account metadata in JSON format.
     |  
     |  delete_category(self, category_id, delete_content, provider_id=None)
     |      Deletes a video category with the given category_id.
     |      If the delete_content is True, then all the content in this
     |      category will be deleted also. If delete_content is False,
     |      then all the content will be moved to the default category.
     |
     |      @param category_id: The ID of a video category.
     |      @param delete_content: True or False, i.e. whether to delete
     |                             also the content in the deleted category.
     |      @param provider_id: The provider_id for videos.
     |      @return Simple message stating whether the content was deleted.
     |
     |  delete_video(self, video_id, provider_id=None)
     |      Deletes a video from the user's account by the given id.
     |      You must give either video_id or provider_id, but not both.
     |
     |      @param video_id: The ID of a video object.
     |      @param provider_id: The ID of a provider for a video.
     |      @return True, if the video was deleted, and None otherwise.
     |
     |  get_delivery_status(self, video_id, provider_id=None)
     |      Gets the status of a video by video or provider id.
     |      You must give either video_id or provider_id, but not both.
     |
     |      Returned status is one of the following values:
     |      ACTIVE
     |      PROCESSING
     |      INACTIVE
     |      ERROR
     |      REMOVED
     |
     |      @param video_id: The ID of a video category.
     |      @param provider_id: The ID of a provider for a video.
     |      @return List video metadata in JSON format.
     |
     |  get_video_by_id(self, video_id, provider_id=None)
     |      Gets the metadata of a video by the given id.
     |      You must give either video_id or provider_id, but not both.
     |
     |      @param video_id: The ID of a video object.
     |      @param provider_id: The ID of a provider for a video.
     |      @return The metadata of a video in JSON format.
     |
     |  get_videos(self, item_count=0)
     |      Gets the latest videos of an account.
     |
     |      @param item_count: The amount of items to return
     |      @return List of video metadata in JSON format.
     |
     |  get_videos_by_category(self, category_id, provider_id=None)
     |      Gets a list of metadata for all videos in given category.
     |      You must give either category_id or provider_id, but not both.
     |
     |      @param category_id: The ID of a video category.
     |      @param provider_id: The ID of a provider for a video.
     |      @return List video metadata in JSON format.
     |
     |  get_videos_by_desc(self, text)
     |      Gets a list of metadata if the given text appears in
     |      the video description.
     |
     |      @param text: Search string for video description.
     |      @return List of video metadata in JSON format.
     |
     |  insert_video(self, video_metadata)
     |      Inserts a video into the user's account.
     |      You must pass the video metadata as a dictionary and it will
     |      be encoded as JSON payload into the HTTP request.
     |
     |      Example video metadata dict:
     |      {
     |          "name": "James Sanders provoca",
     |          "synopsis": False,
     |          "position": 0,
     |          "expiretime": "10.03.2012 02:17:08",
     |          "description": "Some description",
     |          "sourceurl": "http://somehost\/EXAMPLE.mp4",
     |          "categoryid": 1179
     |      }
     |
     |      @param video_metadata: A dictionary with the video metadata.
     |      @return The metadata of the added video in JSON format.
     |
     |  list_categories(self)
     |      Gets the categories for an account.
     |
     |      @return List of category metadata in JSON format.
     |
     |  list_sub_accounts(self)
     |      List existing sub-accounts for a reseller account.
     |      @return: A list of reseller sub-accounts in JSON format.
     |  
     |  remove_token(self, video_id, content_auth_token, provider_id=None)
     |      Remove an authorization token for a video.
     |
     |      @param video_id: The ID of a video object.
     |      @param content_auth_token: Authentication token as a string.
     |      @param provider_id: The ID of a provider for a video.
     |      @return TODO: what is returned?
     |
     |  stitch_videos(self, video_metadata)
     |      Concatenates two videos based on the given metadata.
     |      Mainly used for adding a preroll advertisement to a video.
     |      Notice that the sourceurl and adurl are video_ids already
     |      existing in the ThirdPresence service.
     |
     |      You must pass the video metadata as a dictionary and it will
     |      be encoded as JSON payload into the HTTP request.
     |
     |      Example video metadata dict:
     |      {
     |          "name": "James Sanders provoca with preroll",
     |          "synopsis": False,
     |          "position": 0,
     |          "expiretime": "10.03.2012 02:17:08",
     |          "description": "Some description",
     |          "sourceurl": "300001",
     |          "adurl": "300002",
     |          "categoryid": 1179
     |      }
     |
     |      @param video_metadata: A dictionary with the video metadata.
     |      @return TODO: what is returned?
     |
     |  update_category(self, category_id, name=None, provider_id=None, source_url=N
    one)
     |      Updates a video category with the given metadata.
     |      The source_url must point to a collection of videos, e.g.
     |      in ThirdPresence's own FTP or customer's own RSS. See:
     |      http://wiki.thirdpresence.com/index.php/Uploading_content_using_RSS
     |
     |      @param category_id: The ID of the video category that will be updated.
     |      @param name: The new name for the category.
     |      @param provider_id: Customer's own ID, the provider_id for videos.
     |      @param source_url: Source for the video feed. See the comment above.
     |      @return Added category metadata in JSON format.
     |
     |  update_video_data(self, video_metadata)
     |      Updates video metadata.
     |      You must pass the video metadata as a dictionary and it will
     |      be encoded as JSON payload into the HTTP request.
     |
     |      @param video_metadata: A dictionary with the video metadata.
     |      @return The metadata of the added video in JSON format.
     |


Example for Listing Videos:
---------------------------

    from thirdpresence import Thirdpresence
    x = Thirdpresence(auth_token)
    x.get_videos()


Example for Adding a Video:
---------------------------

    from thirdpresence import Thirdpresence
    x = Thirdpresence(auth_token)
    video_metadata = {
        'description': 'Some Description',
        'name': 'Big Bunny',
        'position': 0,
        'sourceurl': 'https://some_host/bigbunny.avi',
        'synopsis': False,
        'categoryid': 2168
    }
    x.insert_video(video_metadata)


Error Handling:
---------------

Thirdpresence SDK raises Python errors that are all inherited from a
class called ThirdpresenceAPIError, which is inherited from Python
StandardError.

You can make calls to the Thirdpresence service through the SDK and
catch separately all the errors thrown by the service, and let
through all other exceptions.

Example:

    from thirdpresence import Thirdpresence
    try:
        x = Thirdpresence(auth_token)
        x.get_video_by_id(12345)
    except ThirdpresenceAPIError as e:
        print "Thirdpresence service threw an error: {0}".format(e)

