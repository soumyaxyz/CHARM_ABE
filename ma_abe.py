from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc
import numpy as np

debug = False
class CPabe09(ABEnc): #MAabe001
    """
    >>> from charm.toolbox.pairinggroup import PairingGroup,GT
    >>> group = PairingGroup('SS512')
    >>> abe = a.CPabe09(group)
    >>> msg = group.random(GT)
    >>> (sk,pk)= abe.setup(3,[2,2,1]) 
    >>> usr_key = abe.keygen(pk, sk, [[True,True],[True,False],[True]])
    >>> policy = '((ONE or THREE) and (TWO or FOUR))'
    >>> attr_list = ['THREE', 'ONE', 'TWO']
    >>> secret_key = cpabe.keygen(master_public_key, master_secret_key, attr_list)
    >>> cipher_text = cpabe.encrypt(master_public_key, msg, policy)
    >>> decrypted_msg = cpabe.decrypt(master_public_key, secret_key, cipher_text)
    >>> decrypted_msg == msg
    True
    """

    
    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group, numberOfAttributesAtAA_, attributeAuthorityComponentKey
        util = SecretUtil(groupObj, debug)        
        group = groupObj 
        numberOfAttributesAtAA_ = []
        attributeAuthorityComponentKey = []

    def coefecientsOf_f(self, H4,  x, A, P=None):
        #print A
        if P is not None:
            # print P
            assert len(A)==len(P), 'Incompatable setOfAttributes'
        roots = []
        for i in xrange(1,len(A)+1):
            if P is None:
                # print 1 - A[i-1], 
                if (1 - A[i-1]) != 0:
                    roots.insert(i, H4(i) )
            else:
                # print A[i-1]-P[i-1],
                if (A[i-1] -P[i-1]) != 0:
                    roots.insert(i, H4(i) ) 
        F = np.poly(roots)[::-1]
        # print '\n\n\n'
        return F#, roots)

    def f(self, H4, x, A, P=None):
        result = 1
        #print 'A', A, len(A)
        if P is not None:
            assert len(A)==len(P), 'Incompatable setOfAttributes'
        for i in xrange(1,len(A)+1):
            if P is None:
                result *= (x + H4(i))**(1-A[i-1])
            else:
                result *= (x + H4(i))**(A[i-1] -P[i-1])            
        return result
   
    def xor(self, a, b):
        # a_ = group.serialize(a,compression=False)
        # b_ = group.serialize(b,compression=False)
        c = ''.join(chr(ord(a_i)^ord(b_i)) for a_i,b_i in zip(a,b))
        return c

    # def prf(self, Y_j, delta, x_, s_jk, u):
    #     if delta >0:
    #         print 'delta', delta
    #         return Y_j**( x_ / (s_jk+ u) )
    #     else:
    #         print 'delta', delta
    #         return 1/(Y_j**( x_ / (s_jk+ u) ))



    
    
        # N = no Of Attribute Authority
        # n = total number of attributes


    def getAttributeAuthorityComponentKey(self, H4,  attributes_k, alpha, g_s_u_k):# r_u,k,x_k, Y_, s_k, s_j):        
        # piPRF = 1
        # N = len(self.numberOfAttributesAtAA_)
        # for j in xrange(N):
        #     if j<k:                   
        #         s_jk = s_k[j] * s_j[k]
        #         piPRF *= self.prf(Y_[j], 1, x_k, s_jk, r_u)
        #     elif j>k:
        #         s_jk = s_k[j] * s_j[k]
        #         piPRF *= self.prf(Y_[j], -1, x_k, s_jk, r_u)         
        # #import pdb; pdb.set_trace()    * self.f(H4, alpha, attributes_k)     
        return g_s_u_k**(   1/(self.f(H4, alpha, attributes_k) )   )

    def setupAA(self, H4,  alpha): #, k,x_k, Y_, s_k, s_j):   
        return lambda attributes_k, g_s_u_k: self.getAttributeAuthorityComponentKey(H4,  attributes_k, alpha, g_s_u_k )#   r_u,k, x_k, Y_, s_k, s_j)
    


    def setup(self, N, listOfNumberOfAttributes ):
        n = sum(listOfNumberOfAttributes)
        self.numberOfAttributesAtAA_ = listOfNumberOfAttributes
        g, h = group.random(G1), group.random(G2) 

        H1 = lambda x: group.hash(str(x)+str(group.random(ZR)) , ZR)
        H2 = lambda x: group.hash(str(x)+str(group.random(ZR)) , ZR)
        H3 = lambda x: group.hash(str(x)+str(group.random(ZR)) , ZR)       
        H4 = lambda x: group.hash(str(x)+str(group.random(ZR)) , ZR)

        alpha_k, x_, Y_ , s_= [], [], [], []
        for k in xrange(N):
            alpha_k.insert(k, group.random())
            # x_.insert(k, group.random())
            # Y_.insert(k, g**x_[k])
            # s_k_ = []
            # for j in xrange(N):
            #     if j!= k:
            #         s_k_.insert(j, group.random())
            #     else :
            #         s_k_.insert(j, 0)
            # s_.insert(k, s_k_)


        alpha = H1(pair(g,h) ** sum(alpha_k))
        g_alpha = g**alpha

        for k in xrange(N):
            # s_j = []
            # for j in xrange(N):                
            #     #if j== k:
            #     #    continue
            #     s_j.insert(j, s_[j][k]) 
            attributeAuthorityComponentKey.insert(k, self.setupAA(H4,  alpha))#  , k, x_[k] , Y_, s_[k], s_j) )

        K_1, K_2 = group.random(), group.random()
        h_i, u_i, v_i =[], [] ,[]
        for i in xrange(1,n+1):
            h_i.append( h**(alpha**i) )
            u_i.append( h**(K_1) * alpha**i )
            v_i.append( h**(K_2) * alpha**i )
        
        # sk = {'alpha':alpha, 'K_1':K_1, 'K_2': K_2}        
        # pk = {'g':g, 'h':h, 'g^alpha':g_alpha, 'h_':h_i, 'u_':u_i, 'v_':v_i, 'H1': H1,'H2': H2,'H3': H3,'H4': H4}
        sk = (alpha, K_1, K_2)       
        pk = (g, h,  pair(g,h),  g_alpha, h_i, u_i, v_i,  H1, H2, H3, H4)
        return (sk, pk)
    
   

    

    def flattenAttributes(self, setOfAttributes):
        attributes, attributes_, k = [], [], 0
        N = len(self.numberOfAttributesAtAA_)
        for attributesForAA_k in setOfAttributes:
            assert len(attributesForAA_k) == self.numberOfAttributesAtAA_[k] , 'Incompatable setOfAttributes'
            attributes_k = []
            for j in xrange(k):
                attributes_k += [False for i in xrange(self.numberOfAttributesAtAA_[j])]
            for a in attributesForAA_k:
                attributes.append(a)
                attributes_k.append(a)
            for j in xrange(k+1,N):
                attributes_k += [False for i in xrange(self.numberOfAttributesAtAA_[j])]
            attributes_.insert(k,attributes_k)
            k +=1
        return attributes, attributes_


    def keygen(self, pk, sk, setOfAttributes):
        attributes, attributes_ = self.flattenAttributes(setOfAttributes)   
        N = len(self.numberOfAttributesAtAA_) 
        (g, _, _, _, _, _, _, _, _, _, _)  = pk
        (_, K_1, K_2) = sk    
        r_u = group.random()
        g_s_u_k =  g
        for k in xrange(N):
            g_s_u_k = attributeAuthorityComponentKey[k]( attributes_[k], g_s_u_k)
        gS_u = g_s_u_k** (1/K_1) /  g** (  (r_u *K_2) /K_1 )
        key = ( g**r_u,  gS_u, attributes )
        return key




    def encryptPrime(self, pk, sigma_k, P):
        (g, h, _, g_alpha, h_, u_, v_,  H1, H2, H3, H4)  = pk 
        #(alpha, _, _) = sk  
        f = self.coefecientsOf_f(H4, H1(g_alpha), P)
        EP = P #xor(P , H1(alpha+sigma_k))
        K_1Prime, K_2Prime = 1, 1
        n = len(P)
        #import pdb; pdb.set_trace()
        print 'enc',f
        for i in xrange(n):
            try:
                fi = f[i]
            except : 
                fi = 0
            K_1Prime *= u_[i]**fi
            K_2Prime *= v_[i]**fi
        return (EP, sigma_k, K_1Prime, K_2Prime)



    def encrypt(self, pk, M, P):
        (g, h, e_g_h, g_alpha, h_i, u_i, v_i,  H1, H2, H3, H4)  = pk 
        sigma_m, sigma_k =  group.random(), group.random()
        (EP, _, K_1Prime, K_2Prime) =  self.encryptPrime(pk, sigma_k, P)
        # ciphertext
        r_m = H1(str(P)+str(M)+str(sigma_m))
        R_m = g_alpha ** r_m
        K_1m = K_1Prime ** r_m
        K_2m = K_2Prime ** r_m

        C_sigma_m =   self.xor ( group.serialize( H2(e_g_h ** r_m))  , group.serialize(sigma_m) ) 
        C_m =   self.xor ( group.serialize(H3(sigma_m) ) , group.serialize(M) ) 
        return  (EP, sigma_k, R_m, K_1m, K_2m, C_sigma_m, C_m,     e_g_h ** r_m, r_m)
    







    def decryptPrime(self, A , pk, EP, sigma_k, K_1m, K_2m, g_su_d, g_ru_d , sigma_d1):
        (g, h, _, g_alpha, h_, u_, v_,  H1, H2, H3, H4)  = pk 
        #(alpha, _, _) = sk  
        P = EP #xor(P , H1(alpha+sigma_k))
        f = self.coefecientsOf_f(H4, H1(g_alpha), A, P)
        hF_ap = 1
        n = len(P)
        print 'enc',f
        for i in xrange(1,n+1):
            try:
                fi = f[i]
            except : 
                fi = 0
            hF_ap *= h_[i-1]**fi

        U = pair(g_su_d, K_1m**sigma_d1)
        V = pair(g_ru_d, K_2m**sigma_d1)

        return (hF_ap, U*V, f[0])


#done till here 
#(g, h, e_g_h, g_alpha, h_i, u_i, v_i,  H1, H2, H3, H4)  = pk 

    def decrypt(self, usr_key, pk, C):
        (EP, sigma_k, R_m, K_1m, K_2m, C_sigma_m, C_m, _,_) = C
        (g, h, e_g_h, g_alpha, h_i, u_i, v_i,  H1, H2, H3, H4)  = pk 
        ( gR_u,  gS_u, A ) = usr_key
        
        sigma_d =  group.random()
        sigma_d1 = 1/sigma_d
        (hF_ap, UV, f0) = self.decryptPrime( A , pk, EP, sigma_k, K_1m, K_2m, gS_u**sigma_d, gR_u**sigma_d , sigma_d1)

        W = pair(R_m, hF_ap)
        e_g_h_rm = (W/UV)**(1/f0)

        sigma_m =   group.deserialize( self.xor ( group.serialize(H2(e_g_h_rm) ) ,  C_sigma_m) )
        M =   group.deserialize( self.xor ( group.serialize( H3(sigma_m) )  , C_m ) )

         
        return (M,e_g_h_rm)



    def test(self):
        #abe = a.CPabe09(group)
        (sk,pk)= self.setup(3,[2,2,1])
        usr_key = self.keygen(pk, sk, [[True,True],[True,False],[True]])
        P = [True, True, False, False, True]
        M = group.random()
        C = self.encrypt(pk, M, P)
        (_, _, _, _, _, _, _,    e_g_h_rm, _) = C
        (M1, e_g_h_rm1) = self.decrypt(usr_key, pk, C)

        try:
            assert e_g_h_rm == e_g_h_rm1 , 'ABE FAILED!!!'
            print e_g_h_rm, e_g_h_rm1

            assert M == M1 , 'FAILED Decryption!!!'
        except :
            (EP, sigma_k, R_m, K_1m, K_2m, C_sigma_m, C_m, e_g_h_rm, r_m) = C
            (g, h, e_g_h, g_alpha, h_i, u_i, v_i,  H1, H2, H3, H4)  = pk 
            ( gR_u,  gS_u, A ) = usr_key
            (alpha, K_1, K_2) = sk
            e = pair(g,h)
            import pdb; pdb.set_trace()
        



def main():
    #Get the eliptic curve with the bilinear mapping feature needed.
    groupObj = PairingGroup('SS512')

    cpabe = CPabe09(groupObj)
    (msk, pk) = cpabe.setup()
    pol = '((ONE or THREE) and (TWO or FOUR))'
    attr_list = ['THREE', 'ONE', 'TWO']

    if debug: print('Acces Policy: %s' % pol)
    if debug: print('User credential list: %s' % attr_list)
    m = groupObj.random(GT)

    cpkey = cpabe.keygen(pk, msk, attr_list)
    if debug: print("\nSecret key: %s" % attr_list)
    if debug:groupObj.debug(cpkey)
    cipher = cpabe.encrypt(pk, m, pol)

    if debug: print("\nCiphertext...")
    if debug:groupObj.debug(cipher)
    orig_m = cpabe.decrypt(pk, cpkey, cipher)

    assert m == orig_m, 'FAILED Decryption!!!'
    if debug: print('Successful Decryption!')
    del groupObj



if __name__ == '__main__':
    debug = True
    main()