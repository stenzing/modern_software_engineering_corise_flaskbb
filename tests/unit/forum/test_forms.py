import pytest
from werkzeug.datastructures import MultiDict
from flaskbb.forum import forms
from flaskbb.forum.models import Forum
from flaskbb.user.models import Group

pytestmark = pytest.mark.usefixtures("post_request_context", "default_settings")

###################################################################
# CoRise TODO: add unit tests below that test the functionality of
# the `SpecialTopicForm`

class TestSpecialTopicForm(object):

    def test_submit_special_topic_created_with_prefix(self, Fred, database, category):
        with database.session.no_autoflush:
            forum = Forum(title="no guest", category=category)
            forum.groups = Group.query.filter(Group.guest == False).all()
            forum.save()
        data = MultiDict(
            {
                "submit": True,
                "title": "Tests topic",
                "content": "nothing special",
            }
        )
        form = forms.SpecialTopicForm(formdata=data, meta={"csrf": False})
        topic = form.save(Fred, forum)
        assert topic.title == "Special Topic Tests topic"
        assert topic.id 
        assert topic.forum_id == forum.id
        assert topic.posts[0].content == "nothing special"
        

###################################################################