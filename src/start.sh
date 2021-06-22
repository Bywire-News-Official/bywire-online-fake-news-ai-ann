export FLASK_APP=Main
export FLASK_ENV=development

#nohup python3 -m flask run --eager-loading --host='0.0.0.0' --port='5055' > nohup.out
#python3 -m cProfile -o profile.prof Main.py --eager-loading --host='0.0.0.0' --port='5000' 
python3 Main.py
