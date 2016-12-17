from datetime import datetime

from messenger.messenger import save_message

NOT_SENT = 'not_sent'
SENT = 'sent'
RESPONSE_TRUE = True
RESPONSE_FALSE = False
EVALUATION_TRUE = True
EVALUATION_FALSE = False


class Review(object):
    def __init__(self):
        self._submission = NOT_SENT
        self._review_request_1 = NOT_SENT
        self._review_request_2 = NOT_SENT
        self._review_response_1 = NOT_SENT
        self._review_response_2 = NOT_SENT
        self._evaluation_result = NOT_SENT

    @property
    def submission(self):
        return self._submission

    @submission.setter
    def submission(self, value):
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_submission method!")

    @property
    def review_request_1(self):
        return self._review_request_1

    @review_request_1.setter
    def review_request_1(self, value):
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_request_1 method!")

    @property
    def review_request_2(self):
        return self._review_request_2

    @review_request_2.setter
    def review_request_2(self, value):
        if value in [NOT_SENT, SENT]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_request_2 method!")

    @property
    def review_response_1(self):
        return self._review_response_1

    @review_response_1.setter
    def review_response_1(self, value):
        if value in [RESPONSE_TRUE, RESPONSE_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_response_1 method!")

    @property
    def review_response_2(self):
        return self._review_response_2

    @review_response_2.setter
    def review_response_2(self, value):
        if value in [RESPONSE_TRUE, RESPONSE_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_review_response_2 method!")

    @property
    def evaluation_result(self):
        return self._evaluation_result

    @evaluation_result.setter
    def evaluation_result(self, value):
        if value in [EVALUATION_TRUE, EVALUATION_FALSE]:
            self.submission = value
        else:
            raise AttributeError("The submission can't be set just by the set_evaluation_result method!")

    def set_submission(self, submission_message, author = None, admin = None, date = datetime.now().date()):
        if self.review_request_1 == NOT_SENT and self.review_request_2 == NOT_SENT \
                and self.review_response_1 == NOT_SENT and self.review_response_2 == NOT_SENT \
                and self.evaluation_result == NOT_SENT:
            self._submission = SENT
            if author and admin:
                save_message(author, admin, date, submission_message)
        else:
            raise ValueError("Submission request can't be sent!")

    def set_review_request_1(self, review_request_nessage, author = None, admin = None, date = datetime.now().date()):
        if self.submission == SENT and self.review_request_1 == NOT_SENT:
            self._review_request_1 = SENT
            if author and admin:
                save_message(author, admin, date, review_request_nessage)
        else:
            raise ValueError("Review request can't be sent until a submission is not placed!")

    def set_review_request_2(self, review_request_nessage, author = None, admin = None, date = datetime.now().date()):
        if self.submission == SENT and self.review_request_2 == NOT_SENT and self.review_request_1 == SENT:
            self._review_request_2 = SENT
            if author and admin:
                save_message(author, admin, date, review_request_nessage)
        else:
            raise ValueError("Review request can't be sent until a submission is not placed!")

    def set_review_response_1(self, review_response, author = None, admin = None, date = datetime.now().date()):
        if self.review_request_1 == SENT and self.review_request_2 == SENT:
            if review_response:
                self._review_response_1 = RESPONSE_TRUE
            else:
                self._review_response_1 = RESPONSE_FALSE
            if author and admin:
                save_message(author, admin, date, review_response)
        else:
            raise ValueError("Review response can't be set until a review is not sent!")

    def set_review_response_2(self, review_response, author = None, admin = None, date = datetime.now().date()):
        if self.review_request_2 == SENT and self.review_response_1 in [RESPONSE_TRUE, RESPONSE_FALSE]:
            if review_response:
                self._review_response_2 = RESPONSE_TRUE
            else:
                self._review_response_2 = RESPONSE_FALSE
            if author and admin:
                save_message(author, admin, date, review_response)
        else:
            raise ValueError("Review response can't be set until a review is not sent!")

    def set_evaluation_result(self, evaluation_response, author = None, admin = None, date = datetime.now().date()):
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