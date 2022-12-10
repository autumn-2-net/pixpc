import os



def make_path(ly=3,base='./data/t/'):
    pathl=[]
    if ly>5:
        ly=5
        with open('我觉得你有问题','w',encoding='utf-8') as f:
            f.write('就是你')
    if ly <= 0:
        ly = 1
        with open('我觉得你有问题', 'w', encoding='utf-8') as f:
            f.write('就是你')
    for _ in range(ly):
        pathl.append(0)


    while pathl[0] <11:
        # print(pathl)
        G=''
        for i in pathl:
            if i ==10:
                G=G+'#'
                break
            G=G+str(i)+'/'
        if not os.path.exists(base+G):
            os.makedirs(base+G)
        pathl=add_lc(pathl)

def add_lc(l):
    c=l.copy()
    c[-1]=c[-1] +1
    while 1:
        E=0
        for idx,i in enumerate(c):

            if i==11 and idx!=0:
                c[idx]=0
                c[idx-1] = c[idx-1]+1
                E=1
        if E!=1:
            break
    return c

def get_path(id:int,ly=3,):
    c=str(id)
    TSL=len(c)
    if TSL<ly:
        pc=True
    else:
        pc=False
    pa=''
    if pc:
        for ij in c:
            pa=pa+str(ij)+'/'
        pa =pa +'#/'

    else:
        for i in c[:ly]:
            pa = pa + str(i) + '/'

    return pa

def cheak_id_arie(id,ly,base):
    pat=get_path(id=id,ly=ly)
    path=base+pat
    fli=path+str(id)
    back=os.path.exists(fli)
    return back
def write_id_arie(id,ly,base):
    pat=get_path(id=id,ly=ly)
    path=base+pat
    fli=path+str(id)
    with open(fli,'wb'):
        pass

def write_id(id,base,y):
    if y==0:
        fli = base +'/0/'+ str(id)

    if y==1:
        fli = base +'/1/'+ str(id)

    # fli=base+str(id)

    if y==2:
        fli = base +'/2/'+ str(id)
    if y==3:
        fli = base +'/3/'+ str(id)
    with open(fli,'wb'):
        pass


def get_wait_id():
    I=os.listdir('./data/wait/1')
    II = os.listdir('./data/wait/2')
    III = os.listdir('./data/wait/3')

    ic=1
    iic=1
    iiic=1
    if I==[]:
        ic=0
    if II==[]:
        iic=0

    if III==[]:
        iiic=0
    if ic==1:
        os.remove('./data/wait/1/'+I[0])
        if cheak_id_arie(I[0],ly=3,base='./data/t/'):
            return None
        return I[0]
    if iic==1:
        os.remove('./data/wait/2/' + II[0])
        if cheak_id_arie(II[0],ly=3,base='./data/t/'):
            return None
        return II[0]
    if iiic==1:
        os.remove('./data/wait/3/' + III[0])
        if cheak_id_arie(III[0],ly=3,base='./data/t/'):
            return None
        return III[0]
    return None

def cheak_is_in(id):
    a =cheak_id_arie(id,ly=3,base='./data/t/')
    I = os.listdir('./data/wait/1')
    II = os.listdir('./data/wait/2')
    III = os.listdir('./data/wait/3')
    return a or str(id) in I or str(id) in II or str(id) in III