import json, re
src=open('portraits.js').read()
data=json.loads(src[src.index('{'):src.rindex('}')+1])
def rle(row):
    out=[]
    for m in re.finditer(r'(.)\1*',row):
        ch,n=m.group(1),len(m.group(0))
        out.append(ch+(str(n) if n>1 else ''))
    return ''.join(out)
packed={}
for k,v in data.items():
    t={i:rle(b) for i,(a,b) in enumerate(zip(v['closed'],v['talk'])) if a!=b}
    packed[k]={'n':v['name'],'p':v['pal'],'r':[rle(r) for r in v['closed']],'t':t}
s=json.dumps(packed,separators=(',',':'))
open('packed.json','w').write(s)
print(len(s))
