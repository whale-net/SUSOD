.\env\Scripts\activate

$env:FLASK_APP='SUSOD'
$env:FLASK_DEBUG='True'
py -m flask run --host 0.0.0.0 --port 8000 

