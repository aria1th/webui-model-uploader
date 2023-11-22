# contains the test function for the API endpoints

def test(address:str):
    """
    Test the API endpoints for the given address
    """
    import requests
    import json
    import os
    from urllib.parse import urljoin
    from pathlib import Path
    import time
    import threading
    # test "/models/query_hash_sd_all" endpoint, sending multiple requests at very short intervals
    print("Testing POST /models/query_hash_sd_all endpoint")
    # post empty request
    # test 10 times
    results = []
    for i in range(10):
        # send 10 requests at 0.1 seconds interval at thread, then join
        time.sleep(0.1)
        thread = threading.Thread(target=lambda: results.append(requests.post(urljoin(address, "/models/query_hash_sd_all"), json={}).json()))
        thread.start()
        thread.join()
    # check results
    for responses in results:
        # status code should be 200
        assert responses['status'] == 200
    
    # In construction