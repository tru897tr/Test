import random as _r, time as _t, os as _o, sys as _s, subprocess as _p
from datetime import datetime as _d
import platform as _pl, socket as _sk

def _c(): _o.system('cls' if _o.name == 'nt' else 'clear')
class _cl: C='\033[96m'; B='\033[94m'; G='\033[92m'; Y='\033[93m'; R='\033[91m'; M='\033[95m'; BR='\033[1m'; D='\033[2m'; RS='\033[0m'
def _ty(t, d=0.015, c=_cl.G):
    for x in t: _s.stdout.write(f"{c}{x}{_cl.RS}"); _s.stdout.flush(); _t.sleep(d)
    print()
def _lb(txt="Loading", dur=2, w=50):
    for i in range(w+1):
        p = i/w; f=int(w*p); bar="█"*f+"░"*(w-f); pct=int(p*100)
        col = _cl.R if pct<40 else _cl.Y if pct<75 else _cl.G
        _s.stdout.write(f"\r {col}[{bar}]{_cl.RS} {pct:3d}% {txt}"); _s.stdout.flush(); _t.sleep(dur/w)
    print(f"\r {_cl.G}[{'█'*w}]{_cl.RS} 100% {txt} {_cl.G}✓{_cl.RS}")
def _dep():
    _c(); print(f"""{_cl.C}{_cl.BR}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║ 🔍 DEPENDENCY VERIFICATION SYSTEM 🔍                    ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
{_cl.RS}"""); _t.sleep(0.5)
    req={'psutil':'System monitor','requests':'HTTP API'}
    print(f"{_cl.Y} ► Scanning...{_cl.RS}\n"); _t.sleep(0.8); miss=[]
    for pkg,desc in req.items():
        _s.stdout.write(f" {_cl.C}[SCAN]{_cl.RS} {pkg:<12} - "); _s.stdout.flush(); _t.sleep(0.4)
        try: __import__(pkg); print(f"{_cl.G}{_cl.BR}✓ OK{_cl.RS} ({desc})")
        except: print(f"{_cl.R}{_cl.BR}✗ ERROR{_cl.RS}"); miss.append(pkg); _t.sleep(0.3)
    print(f"\n{_cl.C}{'─'*60}{_cl.RS}\n")
    if not miss: print(f" {_cl.G}{_cl.BR}✓ ALL OK!{_cl.RS}\n"); _t.sleep(1.5); return True
    print(f" {_cl.R}{_cl.BR}⚠ MISSING: {len(miss)}{_cl.RS}\n")
    while 1:
        ch=input(f" {_cl.C}Install? [1/2]: {_cl.RS}").strip()
        if ch=='1':
            for pkg in miss:
                print(f" {_cl.C}Installing {pkg}...{_cl.RS}")
                try: _p.run([_s.executable,"-m","pip","install",pkg,"-q"],timeout=60,stdout=_p.DEVNULL,stderr=_p.DEVNULL)
                except: pass
            return _dep()
        if ch=='2': return False
def _ban():
    _c(); print(f"""{_cl.C}{_cl.BR}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║ ██╗ ██╗ █████╗ ██████╗██╗ ██╗███████╗██████╗              ║
    ║ ██║ ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗             ║
    ║ ███████║███████║██║ █████╔╝ █████╗ ██████╔╝              ║
    ║ ██╔══██║██╔══██║██║ ██╔═██╗ ██╔══╝ ██╔══██╗             ║
    ║ ██║ ██║██║ ██║╚██████╗██║ ██╗███████╗██║ ██║             ║
    ║ ╚═╝ ╚═╝╚═╝ ╚═╝ ╚═════╝╚═╝ ╚═╝╚══════╝╚═╝ ╚═╝             ║
    ║                                                           ║
    ║ ████████╗███████╗██████╗ ███╗ ███╗                     ║
    ║ ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║                     ║
    ║    ██║   █████╗  ██████╔╝██╔████╔██║                     ║
    ║    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║                     ║
    ║    ██║   ███████╗██║  ██║██║ ╚═╝ ██║                     ║
    ║    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{_cl.RS}"""); _lb("Booting",1.8); print(f"\n {_cl.G}{_cl.BR}>>> ONLINE <<<{_cl.RS}\n"); _t.sleep(0.8)
def _menu():
    opts=[("Matrix Digital Rain","m"),("Crypto Tracker","c"),("Password Gen","p"),("Rainbow Text","r"),("Rocket Launch","k"),("System Info","s"),("Exit","x")]
    while 1:
        _c(); print(f"\n{_cl.C}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}")
        print(f"{_cl.C}{_cl.BR} ║         🔥 CYBER CENTER V3 🔥        ║{_cl.RS}")
        print(f"{_cl.C}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
        for i,(d,_) in enumerate(opts,1): print(f" {_cl.G if i<7 else _cl.R}[{i}] {d}{_cl.RS}")
        try: return opts[int(input(f" {_cl.C}root@term:~# {_cl.RS}"))-1][1]
        except: _t.sleep(1)
def _crypto():
    _c(); print(f"\n{_cl.Y}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}\n ║     💰 CRYPTO TRACKER [LIVE] 💰    ║\n{_cl.Y}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
    try: import requests as _req; live=True
    except: live=False; print(f" {_cl.R}✗ requests missing → DEMO MODE{_cl.RS}\n")
    if live: _lb("API connect",1.5)
    coins=["BTC","ETH","BNB","SOL","ADA"]
    data={c:{"price":45000 if c=="BTC" else 3000 if c=="ETH" else 450 if c=="BNB" else 100 if c=="SOL" else 0.5,"change":_r.uniform(-2,3)} for c in coins}
    try:
        while 1:
            print(f" {_cl.C}╔════════════════════════════════════╗{_cl.RS}")
            print(f" {_cl.C}║ MARKET {(_cl.G+'[LIVE]'+_cl.RS) if live else (_cl.R+'[DEMO]'+_cl.RS)} {_cl.D}{_d.now().strftime('%H:%M:%S')}{_cl.RS} ║{_cl.RS}")
            print(f" {_cl.C}╠════════════════════════════════════╣{_cl.RS}")
            for c in coins:
                p=data[c]["price"]; ch=data[c]["change"]
                col=_cl.G if ch>0 else _cl.R; arr="▲" if ch>0 else "▼"
                print(f" {_cl.C}║{_cl.BR} {c:^6}{_cl.RS} │ ${p:,.2f} │ {col}{arr} {abs(ch):.2f}%{_cl.RS} ║")
            print(f" {_cl.C}╚════════════════════════════════════╝{_cl.RS}\n")
            _t.sleep(1)
            for _ in range(10): _s.stdout.write('\033[F\033[K')
            for c in coins: data[c]["price"] *= (1 + _r.uniform(-0.001,0.001)); data[c]["change"] += _r.uniform(-0.1,0.1)
    except KeyboardInterrupt: print(f"\n\n {_cl.G}✓ Stopped{_cl.RS}\n"); _t.sleep(1)
def _sys():
    _c(); print(f"\n{_cl.M}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}\n ║        🖥️ SYSTEM INFO 🖥️         ║\n{_cl.M}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
    try: import psutil as _ps; ok=True
    except: ok=False; print(f" {_cl.R}✗ psutil missing!{_cl.RS}\n"); input(); return
    _lb("Scanning",1.5); print()
    u=_pl.uname(); print(f" OS: {_cl.C}{u.system} {u.release}{_cl.RS}\n Host: {_cl.C}{u.node}{_cl.RS}\n")
    cpu=_ps.cpu_percent(1); col=_cl.R if cpu>80 else _cl.Y if cpu>50 else _cl.G
    print(f" CPU: [{col}{'█'*int(cpu//2)}{'░'*(50-int(cpu//2))}{_cl.RS}] {col}{cpu}%{_cl.RS}\n")
    input(f" {_cl.D}Enter...{_cl.RS}")
def _mat():
    _c(); print(f"\n{_cl.G}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}\n ║       🌧️ MATRIX RAIN 🌧️          ║\n{_cl.G}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
    _lb("Loading Matrix",1.5); chars="ｱｲｳ01ABC"; w=50; h=18
    try:
        while 1:
            for _ in range(h): print(" " + "".join([(_cl.BR if _r.random()>0.9 else "") + _cl.G + _r.choice(chars) + _cl.RS for _ in range(w)]))
            _s.stdout.write(f"\033[{h}A"); _t.sleep(0.05)
    except: print(f"\n\n {_cl.G}✓ Exit{_cl.RS}\n"); _t.sleep(1)
def _pass():
    _c(); print(f"\n{_cl.M}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}\n ║      🔐 PASSWORD GEN 🔐           ║\n{_cl.M}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
    import string as _str; chs=_str.ascii_letters+_str.digits+"!@#$%^&*"
    for i in range(5):
        pw=''.join(_r.choice(chs) for _ in range(16))
        print(f" [{i+1}] {pw}"); _t.sleep(0.3)
    input(f"\n {_cl.D}Enter...{_cl.RS}")
def _rain():
    _c(); txt=input(f" {_cl.C}Text: {_cl.RS}")
    cols=[_cl.R,_cl.Y,_cl.G,_cl.C,_cl.B,_cl.M]
    for _ in range(20):
        out=" "
        for i,c in enumerate(txt): out += f"{cols[(i+_)%6]}{_cl.BR}{c}{_cl.RS}"
        print(f"\r{out}",end=""); _t.sleep(0.08)
    input(f"\n\n {_cl.G}Done{_cl.RS}\n")
def _rock():
    _c(); print(f"\n{_cl.R}{_cl.BR} ╔════════════════════════════════════╗{_cl.RS}\n ║       🚀 ROCKET LAUNCH 🚀         ║\n{_cl.R}{_cl.BR} ╚════════════════════════════════════╝{_cl.RS}\n")
    for s in ["Check","Fuel","Engine","Nav","Prep"]: _lb(s,0.8)
    for i in range(10,0,-1): print(f"\r {_cl.R}{_cl.BR}T-{i:02d}{_cl.RS}",end=""); _t.sleep(0.5)
    print(f"\n\n {_cl.R}{_cl.BR}🚀 LIFTOFF! 🚀{_cl.RS}\n"); _t.sleep(1)
    input(f" {_cl.G}Success!{_cl.RS}\n")
def _main():
    _dep(); _ban()
    while 1:
        ch=_menu()
        if ch=='x': _c(); print(f"\n {_cl.C}Shutdown...{_cl.RS}\n"); _lb("Exit",1.2); print(f"\n {_cl.G}Bye!{_cl.RS}\n"); break
        elif ch=='m': _mat()
        elif ch=='c': _crypto()
        elif ch=='p': _pass()
        elif ch=='r': _rain()
        elif ch=='k': _rock()
        elif ch=='s': _sys()
if __name__=="__main__": _main()
