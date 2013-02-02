def main():
	print "Main function"
	if True:
		test = 'test'
	def inner(item):
		print {"item": "I am an inner function with "+item }
	other(test, inner)

def other(stuff, item):
	print item(stuff)

main()