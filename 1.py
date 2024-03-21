
import jsonlines
import json

lis1=[]
with jsonlines.open('train.jsonl') as reader:

    for obj in reader:
        lis1.append(obj)

print(len(lis1))