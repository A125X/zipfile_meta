from flask import Flask, render_template, request 
import crcmod  

app = Flask(__name__)  
@app.route('/', methods=['GET', 'POST']) 

def index(): 
    if request.method == 'POST': 
        file = request.files['file'] 
        crc = calculate_crc(file) 
        return f'The CRC of the file is {crc}' 
        
    return render_template('index.html')  
        
def calculate_crc(file): 
    crc = crcmod.predefined.Crc('crc-32') 

    while True: 
        data = file.read(1024) 
        if not data: 
            break 
        crc.update(data)

    return crc.hexdigest()
    
if __name__ == '__main__': 
    app.run(debug=True)