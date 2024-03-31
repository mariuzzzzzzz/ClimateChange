import{s as _t,n as dt,r as ft}from"../chunks/scheduler.zMJaRgub.js";import{S as ht,i as ct,e as a,s as _,t as W,c as o,g,a as f,b as h,d as l,f as X,h as Z,j as c,k as e,l as ut,m as mt,n as pt,o as $}from"../chunks/index.hLrIEu77.js";function vt(s){let d,x="Climate Change Temperature Prediction",R,r,L="Enter a year to predict the temperature anomalies using three different machine learning models.",T,i,v,N="Year:",U,u,m,j,C,tt="Predict",q,p,P,y,et="Linear Regression Prediction:",I,k,z,J,E,D,nt="Polynomial Regression Prediction:",K,S,A,M,b,F,lt="Random Forest Prediction:",Q,B,G,V,at;return{c(){d=a("h1"),d.textContent=x,R=_(),r=a("p"),r.textContent=L,T=_(),i=a("p"),v=a("strong"),v.textContent=N,U=_(),u=a("label"),m=a("input"),j=_(),C=a("button"),C.textContent=tt,q=_(),p=a("table"),P=a("tr"),y=a("td"),y.textContent=et,I=_(),k=a("td"),z=W(s[1]),J=_(),E=a("tr"),D=a("td"),D.textContent=nt,K=_(),S=a("td"),A=W(s[2]),M=_(),b=a("tr"),F=a("td"),F.textContent=lt,Q=_(),B=a("td"),G=W(s[3]),this.h()},l(t){d=o(t,"H1",{"data-svelte-h":!0}),g(d)!=="svelte-1gznw3m"&&(d.textContent=x),R=f(t),r=o(t,"P",{"data-svelte-h":!0}),g(r)!=="svelte-154a30o"&&(r.textContent=L),T=f(t),i=o(t,"P",{});var n=h(i);v=o(n,"STRONG",{"data-svelte-h":!0}),g(v)!=="svelte-1e3v1s1"&&(v.textContent=N),U=f(n),u=o(n,"LABEL",{});var ot=h(u);m=o(ot,"INPUT",{type:!0,min:!0,max:!0}),ot.forEach(l),n.forEach(l),j=f(t),C=o(t,"BUTTON",{"data-svelte-h":!0}),g(C)!=="svelte-7qel70"&&(C.textContent=tt),q=f(t),p=o(t,"TABLE",{});var w=h(p);P=o(w,"TR",{});var O=h(P);y=o(O,"TD",{"data-svelte-h":!0}),g(y)!=="svelte-4os5zv"&&(y.textContent=et),I=f(O),k=o(O,"TD",{});var rt=h(k);z=X(rt,s[1]),rt.forEach(l),O.forEach(l),J=f(w),E=o(w,"TR",{});var Y=h(E);D=o(Y,"TD",{"data-svelte-h":!0}),g(D)!=="svelte-18lcrk4"&&(D.textContent=nt),K=f(Y),S=o(Y,"TD",{});var st=h(S);A=X(st,s[2]),st.forEach(l),Y.forEach(l),M=f(w),b=o(w,"TR",{});var H=h(b);F=o(H,"TD",{"data-svelte-h":!0}),g(F)!=="svelte-1okprux"&&(F.textContent=lt),Q=f(H),B=o(H,"TD",{});var it=h(B);G=X(it,s[3]),it.forEach(l),H.forEach(l),w.forEach(l),this.h()},h(){Z(m,"type","number"),Z(m,"min","1880"),Z(m,"max","2100")},m(t,n){c(t,d,n),c(t,R,n),c(t,r,n),c(t,T,n),c(t,i,n),e(i,v),e(i,U),e(i,u),e(u,m),ut(m,s[0]),c(t,j,n),c(t,C,n),c(t,q,n),c(t,p,n),e(p,P),e(P,y),e(P,I),e(P,k),e(k,z),e(p,J),e(p,E),e(E,D),e(E,K),e(E,S),e(S,A),e(p,M),e(p,b),e(b,F),e(b,Q),e(b,B),e(B,G),V||(at=[mt(m,"input",s[5]),mt(C,"click",s[4])],V=!0)},p(t,[n]){n&1&&pt(m.value)!==t[0]&&ut(m,t[0]),n&2&&$(z,t[1]),n&4&&$(A,t[2]),n&8&&$(G,t[3])},i:dt,o:dt,d(t){t&&(l(d),l(R),l(r),l(T),l(i),l(j),l(C),l(q),l(p)),V=!1,ft(at)}}}function Ct(s,d,x){let R=location.protocol+"//"+location.host,r=new Date().getFullYear(),L="n.a.",T="n.a.",i="n.a.";async function v(){let u=await(await fetch(`${R}/api/predict?`+new URLSearchParams({year:r}),{method:"GET"})).json();console.log(u),x(1,L=u.linear_regression_model.toFixed(2)+"°C"),x(2,T=u.polynomial_regression_model.toFixed(2)+"°C"),x(3,i=u.random_forest_model.toFixed(2)+"°C")}function N(){r=pt(this.value),x(0,r)}return[r,L,T,i,v,N]}class Pt extends ht{constructor(d){super(),ct(this,d,Ct,vt,_t,{})}}export{Pt as component};