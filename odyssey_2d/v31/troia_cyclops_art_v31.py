"""Cyclops silhouette matching canonical Trojan Horse 2D cartoon drawing grammar.
Anatomical 5.5m giant with one central eye, real knee/shoulder joints and rock grip.
"""
import math

def cyclops(d,x,feet,h,t,action='hold',progress=.5):
    s=h/420
    P=lambda xy:[(x+xx*s,feet+yy*s) for xx,yy in xy]
    skin='#b59b7f'; shadow='#856e5b';INK='#382d2b';hair='#473a35'
    def polygon(coords,c,w=4):
        pts=P(coords);d.polygon(pts,fill=c);d.line(pts+[pts[0]],fill=INK,width=max(1,int(w*s)),joint='curve')
    def ell(box,c,w=4):
        a,b,cx,dy=box
        d.ellipse((x+a*s,feet+b*s,x+cx*s,feet+dy*s),fill=c,outline=INK,width=max(1,int(w*s)))
    def stroke(coords,c,w):d.line(P(coords),fill=c,width=max(1,int(w*s)),joint='curve')
    # Contact with floor: wide anchored stance, asymmetric bent knees while pushing.
    stride=18*math.sin(t*3.7) if action=='walk' else 0
    polygon([(-57,-165),(-18,-165),(-38,-92),(-63,-14),(-83,-3),(-102,-12),(-73,-103)],skin,6)
    polygon([(6,-164),(52,-166),(63,-98),(81,-20),(93,-5),(52,-4),(37,-87)],skin,6)
    polygon([(-116,-9),(-72,-26),(-38,-8),(-31,3),(-108,4)],'#665546',5)
    polygon([(41,-16),(89,-29),(111,-7),(108,5),(34,4)],'#665546',5)
    # A massive curved torso, chest contours and long arms: no rectangular body.
    polygon([(-98,-304),(-117,-238),(-89,-170),(-56,-143),(54,-142),(97,-185),(120,-235),(96,-303),(46,-338),(-60,-333)],skin,7)
    ell((-90,-306,92,-168),'#a99175',5)
    stroke([(-71,-268),(-20,-259),(0,-238)],'#d0b79a',5)
    stroke([(71,-272),(22,-260),(0,-242)],'#d0b79a',5)
    ell((-32,-252,-5,-220),'#ad9378',2)
    ell((13,-252,40,-220),'#ad9378',2)
    # Knee-length animal hide makes silhouette unmistakably different from humans.
    polygon([(-95,-187),(-60,-208),(-28,-193),(5,-212),(41,-193),(88,-203),(95,-123),(66,-137),(42,-115),(15,-138),(-12,-118),(-46,-142),(-71,-117),(-102,-137)],'#6d6251',6)
    for xx in (-73,-45,-10,28,64):
        stroke([(xx,-180),(xx-2,-134)],'#a39478',3)
    # Shoulder joint + arm with elbow / fist world-space anchored by action.
    # Push acts on rock to LEFT: arms move together toward same physical surface.
    for side in (-1,1):
        shoulder=(side*92,-295)
        if action=='push':
            elbow=(-125+side*9,-244+side*32)
            hand=(-173+side*4,-207+side*47)
        elif action in ('drink','offer'):
            elbow=(side*143,-231)
            hand=(side*165,-305)
        elif action in ('fight','fall'):
            elbow=(side*154,-310-18*math.sin(t*3+side))
            hand=(side*158,-377-22*math.sin(t*3+side))
        else:
            elbow=(side*138,-229+9*math.sin(t*.8+side))
            hand=(side*151,-184+12*math.sin(t*.8+side))
        stroke([shoulder,elbow,hand],INK,50)
        stroke([shoulder,elbow,hand],skin,40)
        ell((hand[0]-23,hand[1]-24,hand[0]+24,hand[1]+21),skin,5)
        ell((shoulder[0]-33,shoulder[1]-29,shoulder[0]+30,shoulder[1]+28),shadow,5)
        ell((shoulder[0]-22,shoulder[1]-22,shoulder[0]+22,shoulder[1]+20),skin,2)
    # Hair as one thick dark Bronze-Age rope-like silhouette around head.
    ell((-92,-438,84,-294),skin,7)
    polygon([(-94,-366),(-99,-419),(-76,-454),(-41,-464),(-9,-454),(22,-465),(59,-450),(89,-419),(81,-369),(61,-405),(33,-427),(-13,-434),(-54,-420),(-73,-388)],hair,4)
    # ONLY one eye in the center of the brow, not a human pair.
    ell((-28,-400,30,-344),'#e6d9bf',5)
    ell((-15,-391,15,-358),'#7e7967',3)
    ell((-7,-385,7,-365),INK,1)
    stroke([(-31,-408),(0,-414),(31,-407)],INK,8)
    # Nose and mouth positioned BELOW eye, no second eye silhouettes.
    polygon([(-8,-350),(-16,-326),(9,-325)],'#997d68',2)
    stroke([(-27,-315),(0,-309),(29,-318)],INK,6)
    polygon([(-64,-322),(-47,-293),(-22,-274),(18,-276),(45,-301),(57,-320),(35,-293),(0,-287),(-34,-295)],'#51423d',3)
    # Hair sideburns and tattered locks.
    for xx in (-75,-55,62,79):
        polygon([(xx,-406),(xx+16,-364),(xx-3,-341)],hair,2)
    return {'center':(x,feet-h*.52),'feet':feet,'height':h,'eye':(x,feet-379*s)}