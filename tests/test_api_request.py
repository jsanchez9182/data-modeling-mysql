import requests
from bookmodeling.api_request import BookRequest
import pytest
from freezegun import freeze_time

class ValidMockResponse:
    status_code = 200
    text = (
        """{
            "kind": "books#volumes",
            "totalItems": 1000000,
            "items": [
                {
                    "kind": "books#volume",
                    "id": "Pv1eUCKdP-QC",
                    "etag": "o8VGNaGxQPQ",
                    "selfLink": "https://www.googleapis.com/books/v1/volumes/Pv1eUCKdP-QC",
                    "volumeInfo": {
                        "title": "Caring for Cut Flowers",
                        "authors": [
                            "Rod Jones"
                        ],
                        "publisher": "Landlinks Press",
                        "publishedDate": "2001",
                        "description": "Caring for Cut Flowers shows florists and growers how to make cut flowers last longer. While proper postharvest techniques will not magically transform poor quality flowers into first class material, a few basic, inexpensive techniques can maximise the vase life of good quality material.",
                        "industryIdentifiers": [
                            {
                                "type": "ISBN_10",
                                "identifier": "0643066314"
                            },
                            {
                                "type": "ISBN_13",
                                "identifier": "9780643066311"
                            }
                        ],
                        "readingModes": {
                            "text": false,
                            "image": true
                        },
                        "pageCount": 204,
                        "printType": "BOOK",
                        "categories": [
                            "Gardening"
                        ],
                        "maturityRating": "NOT_MATURE",
                        "allowAnonLogging": false,
                        "contentVersion": "0.4.5.0.preview.1",
                        "panelizationSummary": {
                            "containsEpubBubbles": false,
                            "containsImageBubbles": false
                        },
                        "imageLinks": {
                            "smallThumbnail": "http://books.google.com/books/content?id=Pv1eUCKdP-QC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                            "thumbnail": "http://books.google.com/books/content?id=Pv1eUCKdP-QC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
                        },
                        "language": "en",
                        "previewLink": "http://books.google.com/books?id=Pv1eUCKdP-QC&pg=PA11&dq=flowers&hl=&cd=7&source=gbs_api",
                        "infoLink": "http://books.google.com/books?id=Pv1eUCKdP-QC&dq=flowers&hl=&source=gbs_api",
                        "canonicalVolumeLink": "https://books.google.com/books/about/Caring_for_Cut_Flowers.html?hl=&id=Pv1eUCKdP-QC"
                    },
                    "saleInfo": {
                        "country": "US",
                        "saleability": "NOT_FOR_SALE",
                        "isEbook": false
                    },
                    "accessInfo": {
                        "country": "US",
                        "viewability": "PARTIAL",
                        "embeddable": true,
                        "publicDomain": false,
                        "textToSpeechPermission": "ALLOWED",
                        "epub": {
                            "isAvailable": false
                        },
                        "pdf": {
                            "isAvailable": true,
                            "acsTokenLink": "http://books.google.com/books/download/Caring_for_Cut_Flowers-sample-pdf.acsm?id=Pv1eUCKdP-QC&format=pdf&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                        },
                        "webReaderLink": "http://play.google.com/books/reader?id=Pv1eUCKdP-QC&hl=&source=gbs_api",
                        "accessViewStatus": "SAMPLE",
                        "quoteSharingAllowed": false
                    },
                    "searchInfo": {
                        "textSnippet": "... \u003cb\u003eflower\u003c/b\u003e food . Commercial \u003cb\u003eflower\u003c/b\u003e preservatives contain sugar at a concentration of between 1 and 2 % , which is the best level for most cut \u003cb\u003eflowers\u003c/b\u003e . Using a \u003cb\u003eflower\u003c/b\u003e preservative in the shop and encouraging your customers to use it as&nbsp;..."
                    }
                },
                {
                    "kind": "books#volume",
                    "id": "2XtWDhgljvkC",
                    "etag": "7sHF2Y2OlSI",
                    "selfLink": "https://www.googleapis.com/books/v1/volumes/2XtWDhgljvkC",
                    "volumeInfo": {
                        "title": "A Dictionary of Sexual Language and Imagery in Shakespearean and Stuart Literature",
                        "subtitle": "Three Volume Set Volume I A-F Volume II G-P Volume III Q-Z",
                        "authors": [
                            "Gordon Williams"
                        ],
                        "publisher": "A&C Black",
                        "publishedDate": "2001-09-13",
                        "description": "Providing an alphabetical listing of sexual language and locution in 16th and 17th-century English, this book draws especially on the more immediate literary modes: the theatre, broadside ballads, newsbooks and pamphlets. The aim is to assist the reader of Shakespearean and Stuart literature to identify metaphors and elucidate meanings; and more broadly, to chart, through illustrative quotation, shifting and recurrent linguistic patterns. Linguistic habit is closely bound up with the ideas and assumptions of a period, and the figurative language of sexuality across this period is highly illuminating of socio-cultural change as well as linguistic development. Thus the entries offer as much to those concerned with social history and the history of ideas as to the reader of Shakespeare or Dryden.",
                        "industryIdentifiers": [
                            {
                                "type": "ISBN_13",
                                "identifier": "9780485113938"
                            },
                            {
                                "type": "ISBN_10",
                                "identifier": "0485113937"
                            }
                        ],
                        "readingModes": {
                            "text": false,
                            "image": true
                        },
                        "pageCount": 1650,
                        "printType": "BOOK",
                        "categories": [
                            "Literary Criticism"
                        ],
                        "averageRating": 5,
                        "ratingsCount": 2,
                        "maturityRating": "MATURE",
                        "allowAnonLogging": false,
                        "contentVersion": "0.4.1.0.preview.1",
                        "panelizationSummary": {
                            "containsEpubBubbles": false,
                            "containsImageBubbles": false
                        },
                        "imageLinks": {
                            "smallThumbnail": "http://books.google.com/books/content?id=2XtWDhgljvkC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                            "thumbnail": "http://books.google.com/books/content?id=2XtWDhgljvkC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
                        },
                        "language": "en",
                        "previewLink": "http://books.google.com/books?id=2XtWDhgljvkC&pg=PA518&dq=flowers&hl=&cd=26&source=gbs_api",
                        "infoLink": "http://books.google.com/books?id=2XtWDhgljvkC&dq=flowers&hl=&source=gbs_api",
                        "canonicalVolumeLink": "https://books.google.com/books/about/A_Dictionary_of_Sexual_Language_and_Imag.html?hl=&id=2XtWDhgljvkC"
                    },
                    "saleInfo": {
                        "country": "US",
                        "saleability": "NOT_FOR_SALE",
                        "isEbook": false
                    },
                    "accessInfo": {
                        "country": "US",
                        "viewability": "PARTIAL",
                        "embeddable": true,
                        "publicDomain": false,
                        "textToSpeechPermission": "ALLOWED",
                        "epub": {
                            "isAvailable": false
                        },
                        "pdf": {
                            "isAvailable": true,
                            "acsTokenLink": "http://books.google.com/books/download/A_Dictionary_of_Sexual_Language_and_Imag-sample-pdf.acsm?id=2XtWDhgljvkC&format=pdf&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                        },
                        "webReaderLink": "http://play.google.com/books/reader?id=2XtWDhgljvkC&hl=&source=gbs_api",
                        "accessViewStatus": "SAMPLE",
                        "quoteSharingAllowed": false
                    },
                    "searchInfo": {
                        "textSnippet": "... \u003cb\u003eflowers\u003c/b\u003e &#39; . In &#39; Hasty Bridegroom &#39; ( 1674-81 ; Farmer V.59 ) , the man urges : &#39; let me be to that Garden a Key , That the \u003cb\u003eFlowers\u003c/b\u003e of Virgins incloses &#39; . 3. pl . , menses ( OED from c.1400 ) . Jacquart and Thomasset 71 quote from&nbsp;..."
                    }
                }
            ]
        }"""
    )



def mock_valid_response(url, params):
    return ValidMockResponse


def tmp_output_path(tmp_path):
    pass


@pytest.fixture()
def book_request():
    return BookRequest('flowers', 0, 1, 2)


@pytest.fixture()
def valid_book_request(monkeypatch, book_request):
    monkeypatch.setattr(requests, 'get', mock_valid_response)
    # monkeypatch.setattr(BookRequest, 'get_output_path', tmp_output_path)

    return book_request


class TestBookRequest:
    def test_get_response(self, valid_book_request):
        response = valid_book_request.get_response()

        assert 200 == response.status_code


    @freeze_time('2025-06-05')
    def test_get_output_path(self, valid_book_request):

        assert 'raw_data/flowers/2025-06-05/start_index_0.json' == valid_book_request.get_output_path()

