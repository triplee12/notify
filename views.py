from  flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from http_status import HttpStatus
from models import orm, NotificationCategory, NotificationCategorySchema, Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError

service_blueprint = Blueprint('service', __name__)
notification_category_schema = NotificationCategorySchema()
notification_schema = NotificationSchema()
service = Api(service_blueprint)


class NotificationResource(Resource):
    def get(self, id):
        notification = Notification.query.get_or_404(id)
        dumped_notification = notification_schema.dump(notification).data
        return dumped_notification
    
    def patch(self, id):
        notification = Notification.query.get_or_404(id)
        notification_dict = request.get_json(force=True)
        if 'message' in notification_dict and notification_dict['message'] is not None:
            notification.message = notification_dict['message']
        if 'ttl' in notification_dict and notification_dict['ttl'] is not None:
            notification.duration = notification_dict['duration']
        if 'displayed_times' in notification_dict and notification_dict['displayed_times'] is not None:
            notification.displayed_times = notification_dict['display_times']
        if 'displayed_once' in notification_dict and notification_dict['displayed_once'] is not None:
            notification.displayed_once = notification_dict['displayed_once']
        dumped_notification, dump_errors = notification_schema.dump(notification.message)
        if dump_errors:
            return dump_errors, HttpStatus.bad_request_400.value
        validate_errors = notification_schema.validate(dumped_notification)
        if validate_errors:
            return validate_errors, HttpStatus.bad_request_400.value
        try:
            notification.update()
            return self.get(id)
        except SQLAlchemyError as err:
            orm.session.rollback()
            response = {'error': str(err)}
            return response, HttpStatus.bad_request_400.value
    
    def delete(self, id):
        notification = Notification.query.get_or_404(id)
        try:
            delete = notification.delete(notification)
            response = make_response()
            return response, HttpStatus.no_content_204.value
        except SQLAlchemyError as err:
            orm.session.rollback()
            response = {'error': str(err)}
            return response, HttpStatus.unauthorized_401.value
