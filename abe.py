
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc
import numpy as np
group = PairingGroup('SS512')


H4 = lambda x: group.hash(x+str(group.random(ZR)) , ZR)

def f(x, AP):
        roots = []
        for i in xrange(1,len(AP)+1):
            roots.insert(i, H4(str(i)) )
        F = np.poly(roots)
        return F






def flattenAttributes(setOfAttributes):
	attributes, attributes_, k = [], [], 0
	N = len(numberOfAttributesAtAA_)
	for attributesForAA_k in setOfAttributes:
		assert len(attributesForAA_k) == numberOfAttributesAtAA_[k] , 'Incompatable setOfAttributes'
		attributes_k = []
		for j in xrange(k):
			attributes_k += [False for i in xrange(numberOfAttributesAtAA_[j])]
		for a in attributesForAA_k:
			attributes.append(a)
			attributes_k.append(a)
		for j in xrange(k+1,N):
			attributes_k += [False for i in xrange(numberOfAttributesAtAA_[j])]
		attributes_.insert(k,attributes_k)
		k +=1
	return attributes, attributes_



def xor( a, b, grp):
	a_ = grp.serialize(a,compression=False)
	b_ = grp.serialize(b,compression=False)
	c_ = ''.join(chr(ord(a_i)^ord(b_i)) for a_i,b_i in zip(a_,b_))
	return grp.deserialize(c_,compression=False)

xor = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc))


a0 = group.random(G1) 
a1 = group.random(G2)
a = pair(a0,a1) 

H2 = lambda x: group.hash(str(x)+str(group.random(ZR)) , ZR)

# b0 = group.random(G1) 
# b1 = group.random(G2)
# b = pair(b0,b1) 
b = group.random() 

a_s = group.serialize(a)
b_s = group.serialize(b)

c_s = xor(H2(a_s),b_s)




a
group.deserialize(xor(c_s,b_s)) # ==a

assert a ==  group.deserialize(xor(c_s,b_s)), 'nope'


# c = group.deserialize(c_s) # wrong
# c1 = group.deserialize(xor(a_s,b_s)) # wrong
# c_s1 = group.serialize(c) # wrong
# c1_s = group.serialize(c1) # wrong


# group.deserialize(xor(c1_s,b_s)) # wrong
# group.deserialize(xor(c_s1,b_s)) # wrong








# for i in var:
# 	print i
# for i in xrange(0,len(var)):
# 	for j in xrange(i+1,len(var)):				
# 			print var[i]+var[j]
# for i in xrange(0,len(var)):
# 	for j in xrange(i+1,len(var)):
# 		for k in xrange(j+1,len(var)):
# 			print var[i]+var[j]+var[k]

# for i in xrange(0,len(var)):
# 	for j in xrange(i+1,len(var)):
# 		for k in xrange(j+1,len(var)):
# 			for l in xrange(k+1,len(var)):
# 				print var[i]+var[j]+var[k]+var[l]


def loop(termsTogather, depth, j, arr, indices, POS_FORM):
	#print indices,depth,len(arr)
	if depth ==len(arr)-1-termsTogather:
		res = []
		rep = False
		for i in indices:
			res += arr[i]*1,
			rep = rep or arr[i]
		print res
		POS_FORM += [rep]
	
	for i in xrange(j+1,len(arr)):
		#print 'loop(', depth+1, ',',i,',',indices,'+',[i] ,')', depth		
		loop(termsTogather, depth+1, i, arr, indices+[i], POS_FORM) 

#import pdb; pdb.set_trace()


def expand_to_SOP(expression):
	POS_FORM = []
	for termsTogather in xrange(0,len(expression)):
		for i in xrange(0,len(expression)):
			#print 'loop(', 0, ',', i, ',',[0],')'
			
			loop(termsTogather, 0, i, expression, [i], POS_FORM)
	return POS_FORM



# attrib:
# age = [0,5] # <10, <18, <30, <50 ,<70 , >90
# qualificcation = [0,5] # {below XII, XII,  Bachelor Degree ,  Masters, Doctorate, Post Doc}
# specialization = [0,5] # {none, arts, science, commerce, inter-diciplenary, vovational}
# continent = [0,5] #Africa, Asia, Europe, N America, Oceania, S America


# condition 
##18<age<30  and (Bachelor or Masters ) and DontCARE not {3,5}

#attrib = ['<10', '<18', '<30', '<50' ,'<70' , '>90', 'below XII, XII',  'Bachelor' ,  'Masters', 'Doc', 'Post Doc', 'none', 'arts', 'science', 'commerce', 'inter-diciplenary', 'vovational', 'Africa', 'Asia', 'Europe', 'N America', 'Oceania', 'S America']

# attrib =[False, False, True, False]



# POS_FORM = []
# expand_to_SOP(attrib, POS_FORM)
# for term in POS_FORM:
# 	print (term)*1,
# #print len(POS_FORM)










