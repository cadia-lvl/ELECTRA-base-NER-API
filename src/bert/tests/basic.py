import requests
import json

LOC="/predict"
LOC="/process/service"

Input = ["Ólíklegir kostir byggðir á ágiskunum eða órökstuddri óskhyggju verða oftar en ekki að púðurskotum.",\
	"Ásgeir Gunnarsson, Jón og Friðrik eru allir fæddir 2 desember, 1995",\
	"Ég keypti 200 lítra af mjólk úr bónus.",\
	'100 prósent af heiminum er blár.',\
	'Jón er 20. Ásta er 22.']
for inp in Input:
		print("INP:",inp)
		r = requests.post("http://localhost:8080"+LOC, json={'type':'text','content':inp});
		print(r.text)
		json.loads(r.text)


print("#### ERROR ####")
Input = [{}, {'type':'text'}, {'type':'text', 'content':""}]
for inp in Input:
		print("INP:",inp)
		r = requests.post("http://localhost:8080"+LOC, json=inp);
		print(r.text)
		json.loads(r.text)

