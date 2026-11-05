import React from 'react';
import type {Scene} from './schema';

// Fictional vector scenes for a serial story, not documentary footage.
export const StoryScenery:React.FC<{
  kind:Scene['environment'];
  beat:Scene['beat'];
  time:number;
  layer:'background'|'foreground';
}>=({kind,beat,time,layer})=>{
  if(!beat)return null;
  const wave=Math.sin(time*1.5)*10;
  const flash=beat==='flash'?Math.max(0,...[1.4,4.0,7.2].map(p=>1-Math.abs(time-p)/.55)):0;
  const glow=beat==='voice'?.65+Math.sin(time*4)*.25:beat==='blackout'?Math.max(0,1-time*2.8):.4;
  const dark=beat==='blackout'?Math.min(.82,time*.5):0;
  const coastal=kind==='lighthouse'||kind==='pier';
  const interior=kind==='cottage'||kind==='underfloor'||kind==='lantern';
  return <svg width="1080" height="1920" viewBox="0 0 1080 1920"
    style={{position:'absolute',inset:0,pointerEvents:'none'}}>
    <defs>
      <linearGradient id="tue-night" x1="0" y1="0" x2=".2" y2="1">
        <stop stopColor="#0b2031"/><stop offset=".6" stopColor="#224552"/>
        <stop offset="1" stopColor="#587273"/>
      </linearGradient>
      <linearGradient id="tue-floor" x1="0" y1="0" x2="0" y2="1">
        <stop stopColor="#615c50"/><stop offset="1" stopColor="#272e2f"/>
      </linearGradient>
      <radialGradient id="tue-glow">
        <stop stopColor="#ffeb9c" stopOpacity=".85"/>
        <stop offset="1" stopColor="#eec65a" stopOpacity="0"/>
      </radialGradient>
    </defs>
    {layer==='background'?<>
      <rect width="1080" height="1920" fill="#102c3a"/>
      {coastal&&<>
        <rect width="1080" height="1290" fill="url(#tue-night)"/>
        <circle cx="775" cy="280" r="83" fill="#f3e4b7" opacity=".7"/>
        {[0,1,2,3,4,5,6,7,8].map(i=>
          <circle key={i} cx={(i*183+75)%1080} cy={(i*99+85)%710}
            r={2+i%3} fill="#fffae9" opacity=".5"/>)}
        <path d="M0 960Q160 905 345 975T750 940T1080 960V1330H0Z" fill="#284750"/>
        <path d="M0 1200Q240 1150 480 1200T1080 1180V1920H0Z" fill="#102d3b"/>
        {[0,1,2,3,4,5].map(i=>
          <path key={i} d={'M'+(-120+i*240)+' '+(1350+wave+i*35)+'q120 -18 240 0'}
            stroke="#7aa5a4" strokeWidth="4" opacity=".27" fill="none"/>)}
      </>}
      {kind==='lighthouse'&&<>
        <path d="M110 1240L360 810L440 1240Z" fill="#192d34"/>
        <path d="M665 1220L710 400L910 400L960 1230Z" fill="#c7c5af"
          stroke="#284552" strokeWidth="12"/>
        {[0,1,2].map(i=><path key={i} d={'M'+(705+i*14)+' 590L'+(925+i*9)+' 590'} stroke="#627a78" strokeWidth="10"/>)}
        <rect x="715" y="400" width="210" height="150" rx="12" fill="#2c5963"
          stroke="#d2c5a2" strokeWidth="18"/>
        <path d="M690 393L830 302L958 393Z" fill="#b75542"/>
        <rect x="755" y="410" width="128" height="112" fill="#f9e0a0" opacity={.2+flash*.8}/>
        <path d="M820 465L0 160L0 790Z" fill="#ffe6a2" opacity={flash*.38}/>
        <path d="M820 465L1080 0L1080 925Z" fill="#ffe6a2" opacity={flash*.27}/>
        <ellipse cx="818" cy="460" rx="200" ry="200" fill="url(#tue-glow)" opacity={flash}/>
      </>}
      {kind==='pier'&&<>
        <path d="M0 1100L1080 900V1920H0Z" fill="#31444a"/>
        <path d="M0 1200L1080 1010L1080 1390L0 1630Z" fill="#897760"/>
        {[0,1,2,3,4].map(i=>
          <path key={i} d={'M0 '+(1220+i*92)+'L1080 '+(1030+i*92)}
            stroke="#4f514c" strokeWidth="10"/>)}
        <path d="M125 1090V1430M940 950V1300" stroke="#242e34" strokeWidth="45"/>
        <path d="M120 1090L940 950" stroke="#c6b99b" strokeWidth="20"/>
        {beat==='sign'&&<>
          <path d="M80 410V1120M515 410V1050" stroke="#203b42" strokeWidth="23"/>
          <rect x="70" y="425" width="500" height="310" rx="12"
            fill="#ad9877" stroke="#433d35" strokeWidth="14"/>
          <text x="112" y="548" fontFamily="sans-serif" fontWeight="bold"
            fontSize="45" fill="#2b2f2e">FAROL DESATIVADO</text>
          <text x="112" y="627" fontFamily="sans-serif" fontSize="37"
            fill="#2b2f2e">HÁ 30 ANOS</text>
          <path d="M130 1530q70 -38 110 0t110 0" stroke="#091f2d"
            strokeWidth="26" strokeLinecap="round" fill="none"/>
        </>}
      </>}
      {interior&&<>
        <rect width="1080" height="1920" fill="#283e43"/>
        <path d="M0 0H1080V1150L0 1310Z" fill="#455d5c"/>
        <rect x="105" y="210" width="870" height="850" fill="#2a444b"
          stroke="#7f7e6b" strokeWidth="35"/>
        <path d="M540 210V1060M105 640H975" stroke="#a6a188" strokeWidth="26"/>
        <path d="M0 1260L1080 1160V1920H0Z" fill="url(#tue-floor)"/>
        {[0,1,2,3,4].map(i=>
          <path key={i} d={'M0 '+(1350+i*125)+'L1080 '+(1240+i*130)}
            stroke="#161f22" strokeWidth="12" opacity=".4"/>)}
        <rect x="830" y="380" width="140" height="230" fill="#c0af8b" opacity=".3"/>
      </>}
      {kind==='cottage'&&<>
        <rect x="45" y="1050" width="950" height="115" rx="14" fill="#a47e57"/>
        <path d="M105 1160V1510M915 1160V1510" stroke="#49392e" strokeWidth="35"/>
        {beat==='tea'&&<>
          <ellipse cx="300" cy="1050" rx="76" ry="24" fill="#ddc3a0"/>
          <rect x="239" y="955" width="120" height="92" rx="12"
            fill="#c9d8d0" stroke="#405a5a" strokeWidth="7"/>
          <path d="M360 979q85 -12 47 48t-48 0" fill="none"
            stroke="#c9d8d0" strokeWidth="15"/>
          <rect x="575" y="962" width="120" height="86" rx="12"
            fill="#c9d8d0" stroke="#405a5a" strokeWidth="7"/>
          <path d="M590 915q-20 -35 0 -57t0 -51M637 910q-12 -35 7 -57"
            stroke="#e2e7df" strokeWidth="8" fill="none" opacity={.5+.2*Math.sin(time*2)}/>
        </>}
        {beat==='noise'&&<>
          <path d="M400 1440L725 1410M420 1480L750 1450" stroke="#d8ad78"
            strokeWidth="13" strokeDasharray="52 20"/>
          <circle cx="610" cy="1330" r={95+Math.sin(time*8)*6}
            stroke="#e9c36e" strokeWidth="5" opacity=".6" fill="none"/>
        </>}
      </>}
      {kind==='underfloor'&&<>
        <path d="M90 1120L990 1000L925 1570L160 1680Z" fill="#181e23"
          stroke="#917551" strokeWidth="25"/>
        <path d="M350 1250L690 1220L645 1470L385 1520Z" fill="#070f17"/>
        <path d="M405 1250L460 1080M670 1220L710 1050" stroke="#9c7951"
          strokeWidth="20"/>
        <ellipse cx="700" cy="1100" rx="70" ry="26" fill="none"
          stroke="#ba9b65" strokeWidth="20"/>
        {[0,1,2,3].map(i=>
          <path key={i} d={'M410 '+(1270+i*51)+'L655 '+(1240+i*51)}
            stroke="#67716b" strokeWidth="12"/>)}
      </>}
      {kind==='lantern'&&<>
        <circle cx="495" cy="895" r={260+Math.sin(time*3)*25}
          fill="url(#tue-glow)" opacity={glow}/>
        <path d="M160 440Q520 160 890 450" stroke="#a0aa92"
          strokeWidth="24" fill="none" opacity=".55"/>
        {beat==='voice'&&[0,1,2].map(i=><circle key={i} cx="540" cy="850"
          r={170+i*100+(time*15)%50} fill="none" stroke="#f7d785"
          strokeWidth="5" opacity={.5-i*.12}/>)}
      </>}
      {dark>0&&<rect width="1080" height="1920" fill="#07121b" opacity={dark}/>}
    </>:<>
      {coastal&&<>
        <path d="M0 1560Q400 1490 1080 1590V1920H0Z"
          fill="#122f38" opacity=".92"/>
        <path d="M0 1690Q460 1640 1080 1730" stroke="#67908a"
          opacity=".4" strokeWidth="9" fill="none"/>
      </>}
      {interior&&<>
        <path d="M0 1490L1080 1450V1920H0Z" fill="#253436" opacity=".48"/>
        <path d="M0 1710L1080 1610" stroke="#9b8363" strokeWidth="13"
          opacity=".34"/>
      </>}
    </>}
  </svg>;
};
