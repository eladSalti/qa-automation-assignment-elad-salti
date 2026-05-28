from __future__ import annotations
from typing import Any
import pytest
from src.api import JsonPlaceholderClient

EXPECTED_POSTS_COUNT = 100
VALID_POST_ID = 1
INVALID_POST_ID = 99_999
SUCCESSFUL_DELETE_STATUS_CODES = (200, 204)


@pytest.mark.api
def test_get_posts_returns_list_with_expected_schema(api_client: JsonPlaceholderClient):
    response = api_client.get_posts()

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    posts = response.json()
    assert isinstance(posts, list), (
        f"Expected GET /posts response body to be a list, "
        f"but got {type(posts).__name__}: {posts}"
    )
    assert len(posts) == EXPECTED_POSTS_COUNT, (
        f"Expected GET /posts to return exactly {EXPECTED_POSTS_COUNT} posts "
        f"for JSONPlaceholder, "
        f"but got {len(posts)}"
    )
    _assert_post_schema(posts[0])


@pytest.mark.api
def test_get_post_by_id_status_codes(api_client: JsonPlaceholderClient):
    valid_response = api_client.get_post(VALID_POST_ID)
    invalid_response = api_client.get_post(INVALID_POST_ID)

    assert (
        valid_response.status_code == 200
    ), f"Expected 200, got {valid_response.status_code}"
    _assert_post_schema(valid_response.json())
    assert invalid_response.status_code == 404, (
        f"Expected GET /posts/{INVALID_POST_ID} to return 404 Not Found, "
        f"but got {invalid_response.status_code}. Response body: {invalid_response.text}"
    )


@pytest.mark.api
def test_create_post_echoes_payload_and_generates_id(api_client: JsonPlaceholderClient):
    payload = {
        "userId": VALID_POST_ID,
        "title": "Production-grade automation",
        "body": "A clean API test should validate behavior, not implementation.",
    }

    response = api_client.create_post(payload)
    response_body = response.json()

    assert response.status_code == 201, (
        f"Expected POST /posts to return 201 Created, "
        f"but got {response.status_code}. Response body: {response.text}"
    )

    _assert_payload_echoed(response_body, payload, fields=("userId", "title", "body"))

    assert "id" in response_body, (
        f"Expected created post response to include generated 'id'. "
        f"Response body: {response_body}"
    )

    assert isinstance(response_body["id"], int), (
        f"Expected generated id to be int, "
        f"but got {type(response_body['id']).__name__}: {response_body['id']}"
    )


@pytest.mark.api
def test_update_and_delete_post(api_client: JsonPlaceholderClient):
    payload = {
        "id": VALID_POST_ID,
        "userId": VALID_POST_ID,
        "title": "Updated title",
        "body": "Updated body",
    }

    update_response = api_client.update_post(VALID_POST_ID, payload)
    updated_post = update_response.json()
    delete_response = api_client.delete_post(VALID_POST_ID)

    assert update_response.status_code == 200, (
        f"Expected PUT /posts/{VALID_POST_ID} to return 200 OK, "
        f"but got {update_response.status_code}. Response body: {update_response.text}"
    )

    _assert_payload_echoed(
        updated_post,
        payload,
        fields=("id", "userId", "title", "body"),
    )

    assert delete_response.status_code in SUCCESSFUL_DELETE_STATUS_CODES, (
        f"Expected DELETE /posts/{VALID_POST_ID} to return one of "
        f"{SUCCESSFUL_DELETE_STATUS_CODES}, "
        f"but got {delete_response.status_code}. Response body: {delete_response.text}"
    )


def _assert_post_schema(post: dict[str, Any]) -> None:
    assert isinstance(
        post, dict
    ), f"Expected post item to be a dict, but got {type(post).__name__}: {post}"

    expected_keys = {
        "userId": int,
        "id": int,
        "title": str,
        "body": str,
    }

    for key, expected_type in expected_keys.items():
        assert (
            key in post
        ), f"Expected post item to include key '{key}', but it was missing. Post: {post}"
        assert isinstance(post[key], expected_type), (
            f"Expected post['{key}'] to be {expected_type.__name__}, "
            f"but got {type(post[key]).__name__}: {post[key]}"
        )


def _assert_payload_echoed(response_body: dict[str, Any], payload: dict[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        assert field in response_body, (
            f"Expected response to include field '{field}'. "
            f"Response body: {response_body}"
        )
        assert response_body[field] == payload[field], (
            f"Expected response field '{field}' to echo payload value "
            f"{payload[field]!r}, but got {response_body[field]!r}"
        )
