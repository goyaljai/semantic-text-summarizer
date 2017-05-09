from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import re, math
from collections import Counter
import math
from nltk.stem.porter import PorterStemmer   # using NLTK library
from nltk.corpus import stopwords
stemmer = PorterStemmer()
from bs4 import BeautifulSoup
import codecs
def get_cosine(vec1, vec2):
	'''cosine function and taiking the dot product of the 2 document vectors obtained and dividing with         
	their magnitude.    
	'''                                   
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator                 # 


ini = codecs.open("dataForTextSummary.txt", 'r', encoding='ISO-8859-1')
soup = BeautifulSoup(ini.read(),'lxml')
line = soup.get_text()
line = sent_tokenize(line)
#zen = TextBlob(line)
WORD = re.compile(r'\w+')
#for sentence in zen.sentences:
#	print(sentence)
union = set()
banna= open("summary.txt","w+")
s = ""
n=0
dp = list()
rt = list()
for item in line:
	rt.append(item)
	words = WORD.findall(item)
	words = [stemmer.stem(word) for word in words]
	stop_words = set(stopwords.words('english'))
	words = [w for w in words if not w in stop_words]
	#banna.write(str(Counter(words)))
	dp.append(words)
	union = union | set(Counter(words).keys())
	#banna.write(str(union))
	n+=1

union = list(union)

a = list()
for i in range(n):
	b=list()
	vec = Counter(dp[i])
	vecKeys = vec.keys()
	for word in union:
		if word in vecKeys:
			b.append(vec[word])
		else:
			b.append(0)
	a.append(b)
#banna.write(str(a))
df = list()
ans=0
for ti in union:
	for i in range(n):
		if ti in dp[i]:
			ans+=1
	df.append(ans)
	ans=0
#banna.write(str(df))

weight = list()
for i in range(n):
	j=0
	tmp = dict()
	for word in union:
		tmp[word] = a[i][j]*math.log(n/df[j])
		j+=1
	weight.append(tmp)

#banna.write(str(n))

ans = list()
i=0

for si in line:
	j=0
	b=list()
	for sj in line:
		#banna.write(get_cosine(weight[i],weight[j])
		b.append(get_cosine(weight[i],weight[j]))
		j+=1
	ans.append(b)
	i+=1

rating = dict()

for i in range(n):
	rating[sum(ans[i])]=i

k = list(rating.keys())
k = sorted(k)
k.reverse()
for item in k:
	banna.write(str(rt[rating[item]])+"\n")
