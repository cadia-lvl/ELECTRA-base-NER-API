import requests


r = requests.post("http://0.0.0.0:5000/predict", json={'text':'Ólíklegir kostir byggðir á ágiskunum eða órökstuddri óskhyggju verða oftar en ekki að púðurskotum.'});
print(r.text)


r = requests.post("http://0.0.0.0:5000/predict", json={'text':'Ég keypti 200 lítra af mjólk úr bónus.'});
print(r.text)


r = requests.post("http://0.0.0.0:5000/predict", json={'text':'100 prósent af heiminum er blár.'});
print(r.text)
