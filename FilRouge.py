from flask import Flask,request,Response,send_from_directory
import filetype, json, base64,logging, boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route('/v1/convert', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
     if 'file' not in request.files:
            return 'No file part'
     obj = {}
     file = request.files['file']
     file_header=file.read(262)
     content=file_header +file.read()
     kind= filetype.guess(file_header)
     print(content)
     if kind is not None:
       ext=kind.extension
       mime= kind.mime
       obj['encoding']="Base64"
       content = base64.b64encode(content)
     else:
       ext='txt'
       mime= 'application/text'
       
     obj['name'] = file.filename
     obj['taille']= len(content)
     obj['extension']=ext
     obj['Mime']=mime
     try:
       obj['body']=content.decode() 
     except:
        return 'File format not supported'
     #Enregistrement du fichier dans S3
     file.seek(0)     
     try:
        s3=boto3.client('s3')
        response=s3.upload_fileobj(file, "romy.s3.bucket",file.filename)
     except Exception as e:
        logging.error(e)
     ## Fin enregistrement dans S3
    return  obj
@app.route('/v1/recover',methods=['GET','POST'])   
def return_file():
    if request.method =='POST':
     if 'file' not in request.files:
        return 'No file part'
     file=request.files['file']
     dict=json.loads(file.read())
     # orgfile=open(dict['name'],"wb")
     # orgfile.write(base64.b64decode(dict['body']))
    return Response(base64.b64decode(dict['body']),mimetype=dict['Mime'])
@app.route('/', methods=['GET'])
def serve_portal():
    if request.method== 'POST':
       return 'unsupported Method POST'
    return send_from_directory('./', 'index.html')