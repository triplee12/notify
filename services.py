from datetime import datetime
from pytz import utc
from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from models import NotificationModel
from http_status import HttpStatus


class NotificationManager(object):
    """Notification manager."""

    last_id = 0
    def __init__(self) -> None:
        self.notifications = {}

    def insert_notification(self, notification):
        """Inserts a notification"""
        self.__class__.last_id += 1
        notification.id = self.__class__.last_id
        self.notifications[self.__class__.last_id] = notification

    def get_notifications(self):
        return self.notifications

    def get_notification_by_id(self, id):
        return self.notifications[id]

    def delete_notification(self, id):
        del self.notifications[id]


notification_fields = {
    'id': fields.Integer,
    'uri': fields.Url('notification_endpoint'),
    'message': fields.String,
    'ttl': fields.Integer,
    'creation_date': fields.DateTime,
    'notification_category': fields.String,
    'displayed_times': fields.Integer,
    'displayed_once': fields.Boolean
}

notification_manager = NotificationManager()


class Notification(Resource):
    """Notification resource"""

    def abort_if_notification_not_found(self, id):
        if id not in notification_manager.notifications:
            abort(
                HttpStatus.not_found_404.value,
                message=f"Notification {0} doesn't exist".format(id)
            )

    @marshal_with(notification_fields)
    def get(self, id):
        self.abort_if_notification_not_found(id)
        return notification_manager.get_notification_by_id(id=id)

    def delete(self, id):
        self.abort_if_notification_not_found(id)
        notification_manager.delete_notification(id=id)
        return '', HttpStatus.no_content_204.value

    @marshal_with(notification_fields)
    def patch(self, id):
        self.abort_if_notification_not_found(id)
        notification = notification_manager.get_notification_by_id(id=id)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('ttl', type=int)
        parser.add_argument('displayed_times', type=int)
        parser.add_argument('displayed_once', type=bool)
        args = parser.parse_args()
        print(args)
        if 'message' in args and args['message'] is not None:
            notification.message = args['message']
        if 'ttl' in args and args['ttl'] is not None:
            notification.ttl = args['ttl']
        if 'displayed_times' in args and args['displayed_times'] is not None:
            notification.displayed_times = args['displayed_times']
        if 'displayed_once' in args and args['displayed_once'] is not None:
            notification.displayed_once = args['displayed_once']
        return notification


class NotificationList(Resource):
    """Notification list"""

    @marshal_with(notification_fields)
    def get(self):
        return [v for v in notification_manager.notifications.values()]

    @marshal_with(notification_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True, help='Message cannot be blank!')
        parser.add_argument('ttl', type=int, required=True, help='Time to live cannot be blank!')
        parser.add_argument('notification_category', type=str, required=True, help='Notification category cannot be blank!')
        args = parser.parse_args()
        notification = NotificationModel(
            message=args['message'],
            ttl=args['ttl'],
            creation_date=datetime.now(utc),
            notification_category=args['notification_category']
        )
        notification_manager.insert_notification(notification=notification)
        return notification, HttpStatus.created_201.value


app = Flask(__name__)
service = Api(app)
service.add_resource(NotificationList, '/service/notifications/')
service.add_resource(Notification, '/service/notifications/<int:id>', endpoint='notification_endpoint')

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    debug =True
    app.run(host=host, port=port, debug=debug)
