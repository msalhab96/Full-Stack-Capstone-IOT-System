import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Device, Measures
from Authentication import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
    return response

  @app.route('/')
  def index():
    return jsonify({
      "Success": True
    }), 200

  @app.route('/devices/<int:id>', methods=['GET'])
  def get_device(id):
    target_device = Device.query.filter_by(id=id).one_or_none()
    if target_device:
      return jsonify({
        "Success": True, 
        "DeviceData": target_device.format()
        }), 200
    else:
      abort(404)

  @app.route('/devices/list', methods=["GET"])
  @requires_auth('get:list') # for admin and user
  def list_devices(payload):
    all_devices = [device.format() for device in Device.query.all()]
    return jsonify({
      "Success": True,
      "Devices": all_devices
    }), 200

  @app.route('/device/<int:id>', methods=["DELETE"])
  @requires_auth('delete:device') # admin only
  def delete_device(payload, id):
    target_device = Device.query.filter_by(id=id).one_or_none()
    if target_device:
      try:
        target_device.delete()
      except:
        abort(404)
      return jsonify({
        "Success": True, 
        "Message": f"Device {id} deleted!"
        }), 200
    else:
      abort(404)

  @app.route('/status/change', methods=["PATCH"])
  @requires_auth('patch:device')
  def change_status(payload):
    changes = request.get_json()
    if not (("id" in changes) and ("status" in changes)):
      abort(400)
    id = changes["id"]
    target_device = Device.query.filter_by(id=id).one_or_none()
    if target_device:
      target_device.status = changes["status"]
      target_device.update()
      return jsonify({
        "Success": True, 
        "Message": f"Device {id} updated!"
        }), 200
    else:
      abort(404)

  @app.route('/add/measure', methods=["POST"])
  @requires_auth('post:measure')
  def add_measure(payload):
    data = request.get_json()
    is_time_in = "time" in data
    is_value_in = "value" in data
    is_rank_in = "rank" in data
    is_device_in = "device" in data
    is_valid = is_time_in and is_value_in and is_rank_in and is_device_in
    if is_valid:
      temp_measure = Measures(
        Value = data['value'], 
        Rank = data['rank'],
        DateTime = data['time'],
        DeviceId = data['device']
        )
      temp_measure.insert()
      return jsonify({
        "Success": True, 
        "Message": "measure added!"
        }), 200
    else:
      abort(404)

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "Message": "Resource Not Found!"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "Success": False,
          "message": 'Bad Request'
      }), 400

  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "Success": False,
          "Message": 'Unathorized Access'
      }), 401

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "Success": False,
          "Message": "Unprocessable"
      }), 422

  @app.errorhandler(500)
  def not_found(error):
      return jsonify({
          "success": False,
          "Message": "Server Error!"
      }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "Success": False,
          "Message": error.error['description']
      }), error.status_code

  return app

app = create_app()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)