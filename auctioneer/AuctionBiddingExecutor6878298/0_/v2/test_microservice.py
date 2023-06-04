from .microservice import func
import json
import requests

def test_output_type():
    """
    Test that the output of the microservice is of type 'object'
    """
    input_dict = {
        'auction_id': 123,
        'item_name': 'Test Item',
        'minimum_bid': 10,
        'start_time': 1630454400,  # September 1, 2021 12:00:00 AM UTC
        'end_time': 1630458000,  # September 1, 2021 1:00:00 AM UTC
        'bids': [{'user_id': 1, 'bid_amount': 15}]
    }
    input_json_dict_string = json.dumps(input_dict)
    output = func(input_json_dict_string)
    assert isinstance(output, object)