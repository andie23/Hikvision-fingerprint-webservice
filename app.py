from flask import Flask, request
import fp_module as fp
import json

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_fp_hex():
    try:
        return str({"fp_hash": str(__scan_image_hash())})
    except Exception as error:
        return str({ "error" : error }), 500

@app.route('/match', methods=['POST'])
def match_fp_to_hex_template():
    import imagehash
    threshold = 10
    try:
        is_match = False
        data = json.loads(request.data)
        scanned_hash = __scan_image_hash()
        template_hash = imagehash.hex_to_hash(data["fp_hash"])
        diff = template_hash - scanned_hash
        if diff <= threshold:
            is_match = True
        return str({ "is_match": is_match })
    except Exception as error:
        return str({ "error" : error }), 500

def __scan_image_hash():
    _fp = fp.start_detection_flow()
    fp.save_temp_image(_fp['raw'], _fp['size'])
    image_hash = fp.get_temp_image_hash()
    fp.close_device()
    return image_hash

if __name__ == '__main__':
    app.run()
