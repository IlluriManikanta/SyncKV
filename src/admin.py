from flask import request, jsonify
from globals import view


# put_view():
#     read json input from the request 

#     if the input doesn't contain view:
#         return an error message with status 400 - bad request

#     clear global list of nodes

#     for each node in new view list:
#         aad node to global view list

#     return a message saying view successfully updated with code 200
    
def put_view():
    data = request.get_json()
    new_view = data.get("view")
    if not new_view:
        return jsonify({"Error": "No view provided"}), 400

    view.clear()
    view.extend(new_view)
    return jsonify({"Message": "View successfully updated"}), 200



# get_view():
#     return global view list in a json response with code 200

def get_view():
    return jsonify({"View": view}), 200