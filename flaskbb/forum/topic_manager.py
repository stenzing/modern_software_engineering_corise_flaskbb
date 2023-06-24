# CoRise TODO: implement a class for managing topics with in a forum
from flask import flash
from flask_babelplus import lazy_gettext as _
from flask_allows import Permission

from flaskbb.utils.requirements import CanDeleteTopic, Has, IsAtleastModeratorInForum

class ModeratorMissingException(Exception):
    pass

class TopicManager(object):
    def __init__(self, user, forum, topic) -> None:
        self._user = user
        self._forum = forum
        self._topic = topic

    def set_locking(self, is_reverse ):
        try:
            self._check_moderator()
        except ModeratorMissingException:
            return False
        else:
            return self._set_field("locked",is_reverse)

    def set_important(self, is_reverse ):
        try:
            self._check_moderator()
        except ModeratorMissingException:
            return False
        else:
            return self._set_field("important",is_reverse)
    
    def unhide(self):
        try:
            self._check_moderator()
        except ModeratorMissingException:
            return False
        else:
            if not Permission(Has("makehidden")):
                flash(
                    _("You do not have the permissions to unhide these topics."),
                    "danger",
                )
                return False

            modified_topics = 0
            for topic in self._topic:
                if not topic.hidden:
                    continue
                modified_topics += 1
                topic.unhide()
            return modified_topics

    def hide(self):
        try:
            self._check_moderator()
        except ModeratorMissingException:
            return False
        else:
            if not Permission(Has("makehidden")):
                flash(
                    _("You do not have the permissions to hide these topics."),
                    "danger",
                )
                return False

            modified_topics = 0
            for topic in self._topic:
                if topic.hidden:
                    continue
                modified_topics += 1
                topic.hide(self._user)

            return modified_topics

    def move_topic(self, new_forum):
        return new_forum.move_topics_to(self._topic)

    def delete(self ):
        try:
            self._check_moderator()
        except ModeratorMissingException:
            return False
        else:
            if not Permission(CanDeleteTopic):
                flash(
                    _("You do not have the permissions to delete these topics."),
                    "danger",
                )
                return False
            modified_topics = 0
            for topic in self._topic:
                modified_topics += 1
                topic.delete()
            return modified_topics
    
    def _check_moderator(self):
        
        if not Permission(IsAtleastModeratorInForum(forum=self._topic[0].forum)):
            flash(
                _("You do not have the permissions to execute this action."),
                "danger",
            )
            raise ModeratorMissingException()
        
    def _set_field(self, action, reverse):
        
        modified_topics = 0
        for topic in self._topic:
            if getattr(topic, action) and not reverse:
                continue

            setattr(topic, action, not reverse)
            modified_topics += 1
            topic.save()

        return modified_topics