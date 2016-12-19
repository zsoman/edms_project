#!/usr/bin/env python
"""This file contains the implementation of :py:class:Review and :py:class:ReviewManager classes.
"""

# Imports -----------------------------------------------------------------------------------------------------------
import logging
from datetime import datetime

from messenger.messenger import save_message

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanley - Training 360 Project"
__credits__ = __author__
__version__ = "1.0.0"
__maintainer__ = __author__
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

NOT_SENT = 'not_sent'
SENT = 'sent'
RESPONSE_TRUE = True
RESPONSE_FALSE = False
EVALUATION_TRUE = True
EVALUATION_FALSE = False
module_logger = logging.getLogger('repository.documents')


class Review(object):
    """
    Represents the review of :py:class:Document objects.

    The :py:class:Review object is defined by: :py:attr:submission, :py:attr:review_request_1,
    :py:attr:review_request_2, :py:attr:review_response_1, :py:attr:review_response_2 and :py:attr:evaluation_result
     attributes.
    """

    def __init__(self):
        """
        Initialisation of a new :py:class:Review object.

        """
        self._submission = NOT_SENT
        self._review_request_1 = NOT_SENT
        self._review_request_2 = NOT_SENT
        self._review_response_1 = NOT_SENT
        self._review_response_2 = NOT_SENT
        self._evaluation_result = NOT_SENT

    @property
    def submission(self):
        """
        The property of the :py:attr:_submission attribute.

        :return: The submission of the :py:class:Repository object :py:attr:_submission.
        """
        return self._submission

    @submission.setter
    def submission(self, value):
        """
        The setter of the :py:attr:_submission.

        :param value: New submission.
        :exception AttributeError is raised if the :py:attr:_submission attribute is not :py:const:NOT_SENT or
        :py:const:SENT.
        :return:
        """
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_submission method!")

    @property
    def review_request_1(self):
        """
        The property of the :py:attr:_review_request_1 attribute.

        :return: The review_request_1 of the :py:class:Repository object :py:attr:_review_request_1.
        """
        return self._review_request_1

    @review_request_1.setter
    def review_request_1(self, value):
        """
        The setter of the :py:attr:_review_request_1.

        :param value: New review_request_1.
        :exception AttributeError is raised if the :py:attr:_review_request_1 attribute is not :py:const:NOT_SENT or
        :py:const:SENT.
        :return:
        """
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_request_1 method!")

    @property
    def review_request_2(self):
        """
        The property of the :py:attr:_review_request_2 attribute.

        :return: The review_request_2 of the :py:class:Repository object :py:attr:_review_request_2.
        """
        return self._review_request_2

    @review_request_2.setter
    def review_request_2(self, value):
        """
        The setter of the :py:attr:_review_request_2.

        :param value: New review_request_2.
        :exception AttributeError is raised if the :py:attr:_review_request_2 attribute is not :py:const:NOT_SENT or
        :py:const:SENT.
        :return:
        """
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_request_2 method!")

    @property
    def review_response_1(self):
        """
        The property of the :py:attr:_review_response_1 attribute.

        :return: The review_response_1 of the :py:class:Repository object :py:attr:_review_response_1.
        """
        return self._review_response_1

    @review_response_1.setter
    def review_response_1(self, value):
        """
        The setter of the :py:attr:_review_response_1.

        :param value: New review_response_1.
        :exception AttributeError is raised if the :py:attr:_review_response_1 attribute is not :py:const:RESPONSE_TRUE
        or :py:const:RESPONSE_FALSE.
        :return:
        """
        if value in [RESPONSE_TRUE, RESPONSE_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_response_1 method!")

    @property
    def review_response_2(self):
        """
        The property of the :py:attr:_review_response_2 attribute.

        :return: The review_response_2 of the :py:class:Repository object :py:attr:_review_response_2.
        """
        return self._review_response_2

    @review_response_2.setter
    def review_response_2(self, value):
        """
        The setter of the :py:attr:_review_response_2.

        :param value: New review_response_2.
        :exception AttributeError is raised if the :py:attr:_review_response_2 attribute is not :py:const:RESPONSE_TRUE
        or :py:const:RESPONSE_FALSE.
        :return:
        """
        if value in [RESPONSE_TRUE, RESPONSE_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_response_2 method!")

    @property
    def evaluation_result(self):
        """
        The property of the :py:attr:_evaluation_result attribute.

        :return: The evaluation_result of the :py:class:Repository object :py:attr:_evaluation_result.
        """
        return self._evaluation_result

    @evaluation_result.setter
    def evaluation_result(self, value):
        """
        The setter of the :py:attr:_evaluation_result.

        :param value: New evaluation_result.
        :exception AttributeError is raised if the :py:attr:_evaluation_result attribute is not
        :py:const:EVALUATION_TRUE or :py:const:EVALUATION_FALSE.
        :return:
        """
        if value in [EVALUATION_TRUE, EVALUATION_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_evaluation_result method!")

    def set_submission(self, submission_message, author = None, admin = None, date = datetime.utcnow().date()):
        """
        Sets the :py:attr:_submission to SENT.

        :param submission_message: The message of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the submission is not valid, because of various reasons.
        :return:
        """
        if self.review_request_1 == NOT_SENT and self.review_request_2 == NOT_SENT \
                and self.review_response_1 == NOT_SENT and self.review_response_2 == NOT_SENT \
                and self.evaluation_result == NOT_SENT:
            self._submission = SENT
            if author and admin:
                save_message(author, admin, date, submission_message)
        else:
            raise ValueError("Submission request can't be sent!")

    def set_review_request_1(self, review_request_nessage, author = None, admin = None,
                             date = datetime.utcnow().date()):
        """
        Sets the :py:attr:_review_request_1 to SENT.

        :param review_request_nessage: The message of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the review request is not valid, because of various reasons.
        :return:
        """
        if self.submission == SENT and self.review_request_1 == NOT_SENT:
            self._review_request_1 = SENT
            if author and admin:
                save_message(author, admin, date, review_request_nessage)
        else:
            raise ValueError("Review request can't be sent until a submission is not placed!")

    def set_review_request_2(self, review_request_nessage, author = None, admin = None,
                             date = datetime.utcnow().date()):
        """
        Sets the :py:attr:_review_request_2 to SENT.

        :param review_request_nessage: The message of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the review request is not valid, because of various reasons.
        :return:
        """
        if self.submission == SENT and self.review_request_2 == NOT_SENT and self.review_request_1 == SENT:
            self._review_request_2 = SENT
            if author and admin:
                save_message(author, admin, date, review_request_nessage)
        else:
            raise ValueError("Review request can't be sent until a submission is not placed!")

    def set_review_response_1(self, review_response, author = None, admin = None, date = datetime.utcnow().date()):
        """
        Sets the :py:attr:_review_response_1 to :py:const:RESPONSE_TRUE if the ``review_response`` is TRUE and
        to :py:const:RESPONSE_FALSE if the ``review_response`` is FALSE.

        :param review_response: The response of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the review response is not valid, because of various reasons.
        :return:
        """
        if self.review_request_1 == SENT and self.review_request_2 == SENT:
            if review_response:
                self._review_response_1 = RESPONSE_TRUE
            else:
                self._review_response_1 = RESPONSE_FALSE
            if author and admin:
                save_message(author, admin, date, review_response)
        else:
            raise ValueError("Review response can't be set until a review is not sent!")

    def set_review_response_2(self, review_response, author = None, admin = None, date = datetime.utcnow().date()):
        """
        Sets the :py:attr:review_request_2 to :py:const:RESPONSE_TRUE if the ``review_response`` is TRUE and
        to :py:const:RESPONSE_FALSE if the ``review_response`` is FALSE.

        :param review_response: The response of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the review response is not valid, because of various reasons.
        :return:
        """
        if self.review_request_2 == SENT and self.review_response_1 in [RESPONSE_TRUE, RESPONSE_FALSE]:
            if review_response:
                self._review_response_2 = RESPONSE_TRUE
            else:
                self._review_response_2 = RESPONSE_FALSE
            if author and admin:
                save_message(author, admin, date, review_response)
        else:
            raise ValueError("Review response can't be set until a review is not sent!")

    def set_evaluation_result(self, evaluation_response, author = None, admin = None, date = datetime.utcnow().date()):
        """
        Sets the :py:attr:_evaluation_result to :py:const:EVALUATION_TRUE if the :py:attr:review_request_1 is
        :py:const:RESPONSE_TRUE and the :py:attr:review_request_2 is :py:const:RESPONSE_TRUE and to
        to :py:const:EVALUATION_FALSE if one of the review request is to :py:const:RESPONSE_FALSE.

        :param evaluation_response: The response of the :py:class:Review object.
        :param author: The author(s) (:py:class:User) of the :py:class:Document and the requester of the
        :py:class:Review object, the default value is None.
        :param admin: The admin(s) (:py:class:User) of the :py:class:Project and the administrator(s) of the
        :py:class:Review object, the default value is None.
        :param date: The :py:class:Review object's date, the default value is datetime.utcnow().date().
        :exception ValueError if the evaluation response is not valid, because of various reasons.
        :return:
        """
        if self.review_response_1 in [RESPONSE_TRUE, RESPONSE_FALSE] and \
                        self.review_response_2 in [RESPONSE_TRUE, RESPONSE_FALSE]:
            if self.review_request_1 == RESPONSE_TRUE and self.review_request_2 == RESPONSE_TRUE:
                self._evaluation_result = EVALUATION_TRUE
            else:
                self._evaluation_result = EVALUATION_FALSE
            if author and admin:
                save_message(author, admin, date, evaluation_response)
        else:
            raise ValueError("Review response can't be set until a review is not sent!")


class ReviewManager(object):
    """
    Represents the review manager of :py:class:Review objects.

    The :py:class:ReviewManager object is defined by: location, :py:class:UserManager object and
    :py:class:DocumentManager object.
    """

    def __init__(self, review_manager_path, user_manager, document_manager):
        self._location = review_manager_path
        self._user_manager = user_manager
        self._document_manager = document_manager

    def select_document(self, submission_id):
        pass
        # TODO

    def submit_document(self, _author_id, _manager_id, submission_id):
        pass
        # TODO

    def save_review(self):
        pass
        # TODO

    def send_reviewing_request_1(self, _manager_id, _reviewer_1_id, request_1_id):
        pass
        # TODO

    def send_reviewing_request_2(self, _manager_id, _reviewer_2_id, request_2_id):
        pass
        # TODO

    def send_review_1(self, _reviewer_1_id, _manager_id, response_1_id):
        pass
        # TODO

    def send_review_2(self, _reviewer_2_id, _manager_id, response_2_id):
        pass
        # TODO

    def send_evaluation(self, _manager_id, _author_id, evaluation_result_id):
        pass
        # TODO
