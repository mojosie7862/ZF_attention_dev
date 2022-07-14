from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_slide(presentation_id, page_id):
    """
    Creates the Presentation the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': '1',
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            }
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(f"Created slide with ID:"
              f"{(create_slide_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

    return response


if __name__ == '__main__':
    # Put the presentation_id, Page_id of slides whose list needs
    # to be submitted.
    create_slide("12SQU9Ik-ShXecJoMtT-LlNwEPiFR7AadnxV2KiBXCnE", "My4ndpage")