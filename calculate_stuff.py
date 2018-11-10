import json

def fair_price_for_ADR(file):
    with open(file) as f:
        index = 0
        for line in f:
            data = [int(line[0]) for line in f]
    #print("The average value is ", sum(data)/len(data))

def remove_chars():
    with open('book_buy_prices_for_ADR.txt', 'w') as openfile:
        data = json.loads(openfile)
        json.dumps(data, separators=(',',':'))
        print(data)

    
def main():
    #fair_price_for_ADR('book_buy_prices_for_ADR.txt')
    remove_chars()

if __name__ == "__main__":
    main()
