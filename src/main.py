import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Enterprise, Schedule, Space, Equipment, Spacetype, Brand
from create_database import init_database

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_database()
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/enterprises', methods=['GET', 'POST'])
def handle_enterprises():
    if request.method == 'GET':
        enterprises = Enterprise.query.all()
        enterprises = list(map(lambda x: x.serialize(), enterprises))
        return jsonify(enterprises), 200    
    if request.method == 'POST':
        body = request.get_json()
        enterprise = Enterprise(
            name=body['name'], 
            last_name=body['last_name'], 
            email=body['email'], 
            password=body['password'], 
            cif=body['cif'], 
            phone=body['phone'], 
            tot_hours=body['tot_hours']
            )
        db.session.add(enterprise)
        db.session.commit()
        return "Enterprise correctly created", 200
    return "Invalid Method", 404

@app.route('/enterprise/<int:id>', methods=['GET', 'PUT'])
def handle_enterprise(id):
    if request.method == 'GET':
        enterprise = Enterprise.query.filter_by(id=id)
        enterprise = list(map(lambda x: x.serialize(), enterprise))
        return jsonify(enterprise), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "name" in body:
            update.name = body["name"]
        if "last_name" in body:
            update.last_name = body["last_name"]
        if "email" in body:
            update.email = body["email"]
        if "password" in body:
            update.password = body["password"]
        if "cif" in body:
            update.cif = body["cif"]
        if "phone" in body:
            update.phone = body["phone"]
        if "tot_hours" in body:
            update.tot_hours = body["tot_hours"]
        db.session.commit()
        return "Enterprise correctly edited", 200
    return "Invalid Method", 404

@app.route('/brands', methods=['GET', 'POST'])
def handle_brands():
    if request.method == 'GET':
        brands = Brand.query.all()
        brands = list(map(lambda x: x.serialize(), brands))
        return jsonify(brands), 200 
    if request.method == 'POST':
        body = request.get_json()
        brand = Brand(
            name=body['name'], 
            description=body['description'],    
            logo=body['logo'],
            enterprise_id=body['enterprise_id']
            )
        db.session.add(brand)
        db.session.commit()
        return "Brand correctly created", 200
    return "Invalid Method", 404

@app.route('/brand/<int:id>', methods=['GET', 'PUT'])
def handle_brand(id):
    if request.method == 'GET':
        brand = Brand.query.filter_by(id=id)
        brand = list(map(lambda x: x.serialize(), brand))
        return jsonify(brand), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "name" in body:
            update.name = body["name"]
        if "description" in body:
            update.description = body["description"]
        if "logo" in body:
            update.logo = body["logo"]      
        db.session.commit()
        return "Brand correctly edited", 200
    return "Invalid Method", 404

@app.route('/schedules', methods=['GET', 'POST'])
def handle_schedules():
    if request.method == 'GET':
        schedules = Schedule.query.all()
        schedules = list(map(lambda x: x.serialize(), schedules))
        return jsonify(schedules), 200
    if request.method == 'POST':
        body = request.get_json()
        schedule = Schedule(
            date=body['date'], 
            hour_start=body['hour_start'],       
            hour_end=body['hour_end'],
            enterprise_id=body['enterprise_id'],
            space_id=body['space_id']
            )
        db.session.add(schedule)
        db.session.commit()
        return "Schedule correctly created", 200
    return "Invalid Method", 404  

@app.route('/schedule/<int:id>', methods=['GET', 'PUT'])
def handle_schedule(id):
    if request.method == 'GET':
        schedule = Schedule.query.filter_by(id=id)
        schedule = list(map(lambda x: x.serialize(), schedule))
        return jsonify(schedule), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "name" in body:
            update.name = body["name"]
        if "hour_start" in body:
            update.hour_start = body["hour_start"]
        if "hour_end" in body:
            update.hour_end = body["hour_end"]
        db.session.commit()
        return "Schedule correctly edited", 200
    return "Invalid Method", 404

@app.route('/spaces', methods=['GET', 'POST'])
def handle_spaces():
    if request.method == 'GET':
        schedules = Space.query.all()
        schedules = list(map(lambda x: x.serialize(), schedules))
        return jsonify(schedules), 200
    if request.method == 'POST':
        body = request.get_json()
        space = Space(
            name=body['name'],
            spacetype_id=body['spacetype_id']
            )
        db.session.add(space)
        db.session.commit()
        return "Space correctly created", 200
    return "Invalid Method", 404 

@app.route('/space/<int:id>', methods=['GET', 'PUT'])
def handle_space(id):
    if request.method == 'GET':
        space = Space.query.filter_by(id=id)
        space = list(map(lambda x: x.serialize(), space))
        return jsonify(space), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "name" in body:
            update.name = body["name"]
        db.session.commit()
        return "Space correctly edited", 200
    return "Invalid Method", 404

@app.route('/spacetypes', methods=['GET', 'POST'])
def handle_spacetypes():
    if request.method == 'GET':
        spacetype = Spacetype.query.all()
        spacetype = list(map(lambda x: x.serialize(), spacetype))
        return jsonify(spacetype), 200
    if request.method == 'POST':
        body = request.get_json()
        spacetype = Spacetype(
            description=body['description']
            )
        db.session.add(spacetype)
        db.session.commit()
        return "Spacetype correctly created", 200
    return "Invalid Method", 404 

@app.route('/spacetype/<int:id>', methods=['GET', 'PUT'])
def handle_spacetype(id):
    if request.method == 'GET':
        spacetype = Spacetype.query.filter_by(id=id)
        spacetype = list(map(lambda x: x.serialize(), spacetype))
        return jsonify(spacetype), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "description" in body:
            update.description = body["description"]
        db.session.commit()
        return "Spacetype correctly edited", 200
    return "Invalid Method", 404

@app.route('/equipments', methods=['GET', 'POST'])
def handle_equipments():
    if request.method == 'GET':
        equipments = Equipment.query.all()
        equipments = list(map(lambda x: x.serialize(), equipments))
        return jsonify(equipments), 200
    if request.method == 'POST':
        body = request.get_json()
        equipment = Equipment(
            quantity=body['quantity'],
            name=body['name'],
            description=body['description'],
            space_id=body['space_id']
            )
        db.session.add(equipment)
        db.session.commit()
        return "Equipments correctly created", 200
    return "Invalid Method", 404

@app.route('/equipment/<int:id>', methods=['GET', 'PUT'])
def handle_equipment(id):
    if request.method == 'GET':
        equipments = Equipments.query.filter_by(id=id)
        equipments = list(map(lambda x: x.serialize(), equipments))
        return jsonify(equipments), 200
    if request.method == 'PUT':
        body = request.get_json().items()
        update = Enterprise.query.get(id)
        if update is None:
            raise APIException('Enterprise not found', status_code=404)
        if "description" in body:
            update.description = body["description"]
        if "name" in body:
            update.name = body["name"]
        if "quantity" in body:
            update.quantity = body["quantity"]
        db.session.commit()
        return "Equipments correctly edited", 200
    return "Invalid Method", 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
