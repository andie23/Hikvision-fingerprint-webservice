from flask import Flask, request
import fp_module as fp
import json

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_fp_hex():
    try:
        _fp = __scan_image_hash()
        if _fp["error"]:
            return { "error": _fp["error"] } , _fp["code"]
        return { "fp_hash": str(_fp["hash"]) }, 200
    except Exception as error:
        return { "error" : error }, 500

@app.route('/match', methods=['POST'])
def match_fp_to_hex_template():
    import imagehash
    threshold = 10

    _fp = __scan_image_hash()

    if _fp["error"]:
        return { "error": _fp["error"] }, _fp["code"]
    
    collected_hash = _fp["hash"]
    samples = json.loads(request.data)["fp_samples"]
    
    for sample in samples:
        try:
            sample_hash = imagehash.hex_to_hash(sample)
            diff = sample_hash - collected_hash 
            if diff <= threshold:
                return { "is_match" : True }, 200
        except Exception as error:
            print(error)

    return { "is_match": False }, 404

def __scan_image_hash():
    response = {"error": False}
    _fp = fp.start_detection_flow()

    if _fp["error"]:
        return _fp

    fp.save_temp_image(_fp['raw'], _fp['size'])
    image_hash = fp.get_temp_image_hash()
    return { "error": None, "hash": image_hash }

def __response(payload, code):
    return json.dumps(payload), code

if __name__ == '__main__':
    app.run(host='0.0.0.0')
