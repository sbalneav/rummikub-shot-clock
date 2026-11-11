import math
out=[]
def P(s): out.append(s)
def wire(*pts):
    P('<polyline class="w" points="%s"/>' % " ".join(f"{x},{y}" for x,y in pts))
def dot(x,y): P(f'<circle class="dot" cx="{x}" cy="{y}" r="4"/>')
def text(x,y,s,anchor="start",cls="t"):
    P(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>')
def lab(x,y,ref,val,anchor="start"):
    text(x,y,ref,anchor,"ref"); text(x,y+15,val,anchor,"val")
def zig_v(x,y1,y2,cls="c"):
    n=6;h=(y2-y1)/n;pts=[(x,y1)]
    for i in range(n): pts.append((x+(8 if i%2==0 else -8), y1+(i+0.5)*h))
    pts.append((x,y2))
    P('<polyline class="%s" points="%s"/>'%(cls," ".join(f"{a:.1f},{b:.1f}" for a,b in pts)))
def zig_h(y,x1,x2):
    n=6;h=(x2-x1)/n;pts=[(x1,y)]
    for i in range(n): pts.append((x1+(i+0.5)*h, y+(-8 if i%2==0 else 8)))
    pts.append((x2,y))
    P('<polyline class="c" points="%s"/>'%(" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)))
def arrow(x1,y1,x2,y2):
    P(f'<line class="c" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);dx/=L;dy/=L
    bx,by=x2-9*dx,y2-9*dy;nx,ny=-dy*4,dx*4
    P(f'<polygon class="fill" points="{x2},{y2} {bx+nx:.1f},{by+ny:.1f} {bx-nx:.1f},{by-ny:.1f}"/>')
def cap_v(x,yc):
    P(f'<line class="c" x1="{x-15}" y1="{yc-5}" x2="{x+15}" y2="{yc-5}"/><line class="c" x1="{x-15}" y1="{yc+5}" x2="{x+15}" y2="{yc+5}"/>')
def ecap_v(x,yc):
    P(f'<line class="c" x1="{x-15}" y1="{yc-5}" x2="{x+15}" y2="{yc-5}"/>')
    P(f'<path class="c" d="M{x-15} {yc+10} Q{x} {yc+2} {x+15} {yc+10}"/>')
    text(x-22,yc-9,"+","middle","plus")
def ic(x1,y1,x2,y2,name,part,pins):
    P(f'<rect class="ic" x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="3"/>')
    cx=(x1+x2)/2;cy=(y1+y2)/2
    text(cx,cy-4,name,"middle","icname");text(cx,cy+13,part,"middle","icpart")
    for side,pos,num,fn in pins:
        if side=="L": text(x1-6,pos-5,num,"end","pin");text(x1+7,pos+4,fn,"start","pfn")
        if side=="R": text(x2+6,pos-5,num,"start","pin");text(x2-7,pos+4,fn,"end","pfn")
        if side=="T": text(pos+5,y1-6,num,"start","pin");text(pos,y1+16,fn,"middle","pfn")
        if side=="B": text(pos+5,y2+15,num,"start","pin");text(pos,y2-8,fn,"middle","pfn")
def npn(cx,cy,ref,part,lx,ly):
    P(f'<circle class="ic" cx="{cx}" cy="{cy}" r="24"/>')
    P(f'<line class="c" x1="{cx-25}" y1="{cy}" x2="{cx-8}" y2="{cy}"/>')
    P(f'<line class="c thick" x1="{cx-8}" y1="{cy-14}" x2="{cx-8}" y2="{cy+14}"/>')
    P(f'<polyline class="c" points="{cx-8},{cy-6} {cx+15},{cy-18} {cx+15},{cy-30}"/>')
    P(f'<polyline class="c" points="{cx-8},{cy+6} {cx+15},{cy+18} {cx+15},{cy+30}"/>')
    dx,dy=23,12;L=math.hypot(dx,dy);dx/=L;dy/=L
    tx,ty=cx+13,cy+17;bx,by=tx-9*dx,ty-9*dy;nx,ny=-dy*4,dx*4
    P(f'<polygon class="fill" points="{tx:.1f},{ty:.1f} {bx+nx:.1f},{by+ny:.1f} {bx-nx:.1f},{by-ny:.1f}"/>')
    lab(lx,ly,ref,part)
def flag(x,y,s,anchor="start"):
    w=len(s)*7.4+16
    x0 = x if anchor=="start" else x-w
    P(f'<rect class="flag" x="{x0}" y="{y-11}" width="{w}" height="22" rx="11"/>')
    text(x0+w/2,y+4,s,"middle","flagt")

# ================= MAIN =================
RY,GY=70,700
# rails
wire((150,RY),(1140,RY),(1140,122))
wire((70,GY),(1140,GY))
text(170,RY-10,"+V","start","rail");text(170,GY-10,"0 V","start","rail")
# battery + switch
wire((70,340),(70,RY),(97,RY))
P(f'<circle class="ring" cx="100" cy="{RY}" r="3.5"/><circle class="ring" cx="150" cy="{RY}" r="3.5"/>')
P(f'<line class="c" x1="102" y1="{RY-2}" x2="146" y2="{RY-20}"/>')
lab(125,RY-42,"S1","on/off","middle")
for yy,w,th in [(340,32,False),(348,16,True),(360,32,False),(368,16,True)]:
    P(f'<line class="c{" thick" if th else ""}" x1="{70-w/2}" y1="{yy}" x2="{70+w/2}" y2="{yy}"/>')
text(48,338,"+","middle","plus")
wire((70,368),(70,GY))
lab(58,410,"B1","3–9 V","end")
# bulk cap
wire((150,RY),(150,365)); ecap_v(150,370); wire((150,376),(150,GY)); dot(150,RY); dot(150,GY)
lab(172,366,"C6","220µF")
# ---- timer U1
T=320
wire((T,RY),(T,110)); zig_v(T,110,170); wire((T,170),(T,200)); zig_v(T,200,260); arrow(300,272,340,190)
wire((T,260),(T,585)); dot(T,RY)
lab(306,138,"R1","150k","end"); lab(296,214,"VR1","250k trim","end")
wire((T,300),(400,300)); wire((T,340),(400,340)); dot(T,300); dot(T,340)
dot(T,480); wire((T,480),(250,480),(250,500)); zig_v(250,500,560); wire((250,560),(250,587))
P('<circle class="ring acc" cx="250" cy="590" r="3.5"/><circle class="ring acc" cx="250" cy="640" r="3.5"/>')
P('<line class="c acc thick" x1="238" y1="584" x2="238" y2="646"/><line class="c acc" x1="238" y1="615" x2="222" y2="615"/><line class="c acc" x1="222" y1="606" x2="222" y2="624"/>')
wire((250,643),(250,GY)); dot(250,GY)
lab(238,528,"R3","22Ω","end")
text(212,604,"S2","end","ref acct"); text(212,619,"EASY","end","val acct"); text(212,633,"BUTTON","end","val acct")
ecap_v(T,590); wire((T,596),(T,GY)); dot(T,GY); lab(342,588,"C1","220µF")
ic(400,240,520,440,"U1","555",[("T",430,"8","VCC"),("T",490,"4","RST"),("L",300,"6","THR"),("L",340,"2","TRIG"),("L",390,"7","DIS"),("R",340,"3","OUT"),("B",430,"1","GND"),("B",490,"5","CV")])
wire((380,390),(400,390)); P('<path class="c" d="M374 384 l12 12 M386 384 l-12 12"/>'); text(370,412,"n/c","end","pfn")
wire((430,RY),(430,240)); dot(430,RY); wire((490,RY),(490,240)); dot(490,RY)
wire((430,440),(430,GY)); dot(430,GY)
wire((490,440),(490,560)); cap_v(490,565); wire((490,570),(490,GY)); dot(490,GY); lab(514,563,"C2","10nF")
# ---- inverter
wire((520,340),(560,340)); zig_h(340,560,620); wire((620,340),(650,340)); lab(590,312,"R4","10k","middle")
wire((690,RY),(690,110)); zig_v(690,110,170); wire((690,170),(690,310)); dot(690,RY); lab(676,138,"R5","100k","end")
npn(675,340,"Q1","2N3904",702,420)
wire((690,370),(690,GY)); dot(690,GY)
dot(690,210)
P('<path class="w" d="M690 210 H782 A8 8 0 0 1 798 210 H890 V240"/>')
text(845,202,"ALARM","middle","net")
# ---- tone U2
X=790
wire((X,RY),(X,110)); zig_v(X,110,170); wire((X,170),(X,300)); dot(X,RY)
zig_v(X,300,345); wire((X,345),(X,560)); cap_v(X,565); wire((X,570),(X,GY)); dot(X,GY)
wire((X,280),(860,280)); dot(X,280); wire((X,360),(860,360)); dot(X,360); wire((X,395),(860,395)); dot(X,395)
lab(778,138,"R6","1k","end"); lab(778,318,"R7","10k","end"); lab(768,563,"C3","47nF","end")
ic(860,240,980,440,"U2","555",[("T",890,"4","RST"),("T",950,"8","VCC"),("L",280,"7","DIS"),("L",360,"6","THR"),("L",395,"2","TRIG"),("R",340,"3","OUT"),("B",890,"1","GND"),("B",950,"5","CV")])
wire((950,RY),(950,240)); dot(950,RY)
wire((890,440),(890,GY)); dot(890,GY)
wire((950,440),(950,560)); cap_v(950,565); wire((950,570),(950,GY)); dot(950,GY); lab(974,563,"C4","10nF")
# ---- driver
wire((980,340),(1010,340)); zig_h(340,1010,1070); wire((1070,340),(1100,340)); lab(1040,312,"R8","680Ω","middle")
npn(1125,340,"Q2","2N2222A",1152,420)
wire((1140,370),(1140,GY))
P('<rect class="ic" x="1132" y="122" width="16" height="36"/><polygon class="ic" points="1148,122 1172,102 1172,178 1148,158"/>')
wire((1140,158),(1140,200)); zig_v(1140,200,260); wire((1140,260),(1140,310))
dot(1140,95); dot(1140,185)
wire((1140,95),(1220,95),(1220,132)); wire((1220,150),(1220,185),(1140,185))
P('<polygon class="ic" points="1210,150 1230,150 1220,133"/><line class="c thick" x1="1209" y1="132" x2="1231" y2="132"/>')
lab(1236,138,"D1","1N4148")
lab(1120,136,"LS1","8Ω speaker","end"); lab(1128,226,"R9","10–47Ω","end")
# captions
for x,s in [(110,"POWER"),(380,"1 · 60-SECOND TIMER"),(660,"2 · INVERTER"),(880,"3 · TONE"),(1170,"4 · SPEAKER DRIVER")]:
    text(x,738,s,"middle","cap")
main="\n".join(out); out.clear()

# ================= PULSER =================
RY,GY=50,450
wire((40,RY),(400,RY)); wire((40,GY),(400,GY)); text(48,RY-10,"+V","start","rail"); text(48,GY-10,"0 V","start","rail")
X=150
wire((X,RY),(X,90)); zig_v(X,90,150); wire((X,150),(X,215)); dot(X,RY)
zig_v(X,215,275); wire((X,275),(X,375)); cap_v(X,380); wire((X,385),(X,GY)); dot(X,GY)
wire((X,190),(250,190)); dot(X,190); wire((X,290),(250,290)); dot(X,290); wire((X,320),(250,320)); dot(X,320)
lab(138,118,"R10","10k","end"); lab(138,243,"R11","330k","end"); lab(128,378,"C5","1µF film","end")
ic(250,150,370,360,"U3","555",[("T",280,"8","VCC"),("T",340,"4","RST"),("L",190,"7","DIS"),("L",290,"6","THR"),("L",320,"2","TRIG"),("R",250,"3","OUT"),("B",280,"1","GND"),("B",340,"5","CV")])
wire((280,RY),(280,150)); dot(280,RY)
wire((340,150),(340,110),(420,110)); flag(420,110,"from ALARM (Q1 collector)")
wire((370,250),(420,250)); flag(420,250,"to U2 pin 4")
wire((280,360),(280,GY)); dot(280,GY)
wire((340,360),(340,395)); cap_v(340,400); wire((340,405),(340,GY)); dot(340,GY); lab(362,398,"C7","10nF")
text(420,290,"≈ 2 Hz: ¼ s on, ¼ s off","start","cap")
pulser="\n".join(out)
open("./main.svgfrag","w").write(main)
open("./pulser.svgfrag","w").write(pulser)
