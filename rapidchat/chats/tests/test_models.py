import pytest
from django.contrib.auth import get_user_model

from rapidchat.chats.models import Conversation, Message

User = get_user_model()


@pytest.mark.django_db
def test_conversation_model():
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    conversation.join(user1)
    conversation.join(user2)

    assert conversation.get_online_count() == 2
    assert user1 in conversation.online.all()
    assert user2 in conversation.online.all()

    conversation.leave(user1)
    assert conversation.get_online_count() == 1
    assert user1 not in conversation.online.all()


@pytest.mark.django_db
def test_adding_existing_user_to_conversation():
    user1 = User.objects.create_user(username="user1", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    conversation.join(user1)

    # Try to add the same user again
    conversation.join(user1)
    assert conversation.get_online_count() == 1


@pytest.mark.django_db
def test_removing_nonexisting_user_from_conversation():
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    conversation.join(user1)

    # Get the count before trying to remove a user who's not in the conversation
    count_before = conversation.get_online_count()
    conversation.leave(user2)
    count_after = conversation.get_online_count()

    assert count_before == count_after


@pytest.mark.django_db
def test_conversation_str_method():
    user1 = User.objects.create_user(username="user1", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    conversation.join(user1)

    assert str(conversation) == "Test Conversation (1)"


@pytest.mark.django_db
def test_message_model():
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    message = Message.objects.create(conversation=conversation, from_user=user1, to_user=user2, content="Hello World")

    assert message in Message.objects.all()
    assert str(message) == f"From {user1.username} to {user2.username}: {message.content} [{message.timestamp}]"


@pytest.mark.django_db
def test_message_default_read_field():
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    message = Message.objects.create(conversation=conversation, from_user=user1, to_user=user2, content="Hello World")

    assert message.read is False


@pytest.mark.django_db
def test_message_str_method():
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    conversation = Conversation.objects.create(name="Test Conversation")
    message = Message.objects.create(conversation=conversation, from_user=user1, to_user=user2, content="Hello World")

    assert str(message) == f"From {user1.username} to {user2.username}: {message.content} [{message.timestamp}]"
