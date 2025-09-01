import requests
import logging

logger = logging.getLogger(__name__)

def call_external_api(
    method,
    url,
    headers=None,
    params=None,
    data=None,
    json=None,
    timeout=10,
    raise_for_status=True,
):
    """
    Generic function to call an external API.

    Args:
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
        url (str): The full API URL.
        headers (dict, optional): Headers to include in the request.
        params (dict, optional): Query parameters.
        data (dict, optional): Form data for POST/PUT.
        json (dict, optional): JSON data for POST/PUT.
        timeout (int, optional): Timeout in seconds. Default is 10.
        raise_for_status (bool): Whether to raise for HTTP errors.

    Returns:
        dict or str: Parsed JSON response or raw text.

    Raises:
        requests.RequestException: For any request-related issues.
    """
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
        )
        if raise_for_status:
            response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return response.text

    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        raise
