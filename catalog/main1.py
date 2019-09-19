from flask import Flask

app=Flask(__name__) #name defines project

@app.route("/info/details")
def demo():
	return "hello details"
if __name__=='__main__': #to run server automatically
	app.run(debug=True)