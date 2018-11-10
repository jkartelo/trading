#f = open('book_buy_prices_for_ADR.txt')
#for word in f.read().split(","):
#    print(word.replace("[", " ").replace("]", " ").replace)

#f = open('book_buy_prices_for_ADR.txt',"r") #opens file with name of "test.txt"
#myList = []
#for line in f:
#    myList.append(line)
#    print line
#print(myList)

with open('book_buy_prices_for_ADR.txt', 'r') as data:
  plaintext = data.read()

plaintext = plaintext.replace(',', '').replace('[',' ').replace(']',' ')
print plaintext

text_file = open("Output.txt", "w")
text_file.write(plaintext)
text_file.close()

counter=0
sum=0
min=100000
with open("Output.txt", 'r') as data:
  for x in data.read().split():
      x = int(x)
      if int(x) > 3000:
          sum = sum + x
          counter = counter + 1
          if min > x:
              min = x
          print(x)

print ("bla bla", sum/counter)
print min

