from flask import request
from flask_restful import Resource
from ... import db
from ...models import Profile, ProfileSchema

profiles_schema = ProfileSchema(many=True) 
profile_schema = ProfileSchema()

class ProfileResource(Resource):
    '''
    Defining API endpoints for the profile
    '''
    def get(self):
        profiles = Profile.query.all()
        profiles = profiles_schema.dump(profiles)
        return {
            'success': True,
            'data': profiles
        }, 200
    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'success': False,
                'message': 'No input data provided'
            }, 400
        

        # Validate and deserialize data
        try:
            data = profile_schema.load(json_data)
        except Exception as e:
            return {
                'success': False,
                'message': 'Unable to process data',
                'error': e
            }, 422

        profile = Profile(**data)
        profile.save_profile()

        result = profile_schema.dump(profile)
        return {
            'success': True,
            'message': Successfully added Profile,
            'data': result
        }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'success': False,
                'message': 'No Input data provided'
            }, 400

        # Validate and deserialze the json data
        try:
            data = profile_schema.load(json_data)
        except Exception as e:
            return {
                'success': False,
                'message': 'Unable to process data',
                'error' e
            }, 422

        # Search for the specific profile in db
        profile = Profile.query.filter_by(id = data['id']).first()
        if not profile:
            return {
                'success': False,
                'message': 'Profile does not exist in the database'
            }, 400
        
        profile.username = profile['username']
        profile.country = profile['country']
        profile.facebook = profile['facebook']
        profile.twitter = profile['twitter']
        profile.google = profile['google']
        profile.is_active = profile['is_active']
        profile.is_verified = profile['is_verified']
        profile.remember_token = profile['remember_token']

        db.session.commit()

        result = profile_schema.dump(profile)
        
        return {
            'success': True,
            'message': 'Successfully updated profile',
            'data': result
        }, 200


    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                'success': False,
                'message': 'No input data provided'
            }, 400

        try:
            data = profile_schema.load(json_data)
        except Exception as e:
            return {
                'success': False,
                'message': 'Unable to process data',
                'error': e
            }, 422

        profile = Profile.query.filter_by(id = data['id']).delete()
        db.session.commit()

        result = profile_schema.dump(profile)

        return {
            'success': True,
            'message': 'Successfully deleted profile',
            'data': result
        }, 200