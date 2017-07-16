from flask import Flask, render_template, request

import urllib2
import json
import requests



app = Flask("MyApp")

@app.route('/about', methods=["GET","POST"])
def contact():
	form_data = request.form	
	return render_template('about.html', form_data=form_data)

	
	
@app.route('/index', methods=['GET', 'POST'])
def index():
	errors = []
	results = {}
	if request.method == "POST":
		text = request.form['text']
		print(text)
	#return render_template('hello.html')
		print request.form['text']
	#request.form['text'] = input(text)
		# Configure API access
		apiKey = '52cf70da793e41e98ee0c37840095c84'
		sentimentUri = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
		keyPhrasesUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
		languageUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/languages'

		# Ask the user for a text
		print('Enter a text (or leave blank for default text)')
		sampleText = text
		if (sampleText == ''):
			sampleText = 'We are having so much fun thanks to the Code First Girls summer course. Hope you enjoy this tool!'


		# Prepare headers
		headers = {}
		headers['Ocp-Apim-Subscription-Key'] = apiKey
		headers['Content-Type'] = 'application/json'
		headers['Accept'] = 'application/json'

		# Detect language
		postData1 = json.dumps({"documents":[{"id":"1", "text":sampleText}]}).encode('utf-8')
		request1 = urllib2.Request(languageUri, postData1, headers)
		response1 = urllib2.urlopen(request1)
		response1json = json.loads(response1.read().decode('utf-8'))
		language = response1json['documents'][0]['detectedLanguages'][0]['iso6391Name'] # Sample json: {'errors': [], 'documents': [{'id': '1', 'detectedLanguages': [{'name': 'English', 'score': 1.0, 'iso6391Name': 'en'}]}]}
 
		# Determine sentiment
		postData2 = json.dumps({"documents":[{"id":"1", "language":language, "text":sampleText}]}).encode('utf-8')
		request2 = urllib2.Request(sentimentUri, postData2, headers)
		response2 = urllib2.urlopen(request2)
		response2json = json.loads(response2.read().decode('utf-8'))
		sentiment = response2json['documents'][0]['score'] # Sample json: {'errors': [], 'documents': [{'id': '1', 'score': 0.946106320818458}]}
 
		# Determine key phrases
		postData3 = postData2
		request3 = urllib2.Request(keyPhrasesUri, postData3, headers)
		response3 = urllib2.urlopen(request3)
		response3json = json.loads(response3.read().decode('utf-8'))
		keyPhrases = response3json['documents'][0]['keyPhrases'] # Sample json: {'documents': [{'keyPhrases': ['Azure'], 'id': '1'}], 'errors': []}


		#Display results
		print('Text: %s' % sampleText)
		print('Language: %s' % language)
		print('Sentiment: %f' % sentiment)
		print('Key phrases: %s' % keyPhrases)

		

		return render_template('index.html', sentiment=sentiment)
	return render_template('index.html')
	#print ["sentiment"]	


app.run(debug=True, port=int(os.environ.get("PORT", 5000), host='0.0.0.0')
