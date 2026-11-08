# Formulación de candidatos

Para todos los modelos nuevos: dh1/dt=qin−q12; dh2/dt=r(q12−qout), r=A1/A2.
Los caudales q=Q/A1 están en cm/s y r es adimensional. Por ello
d(h1+h2/r)/dt=qin−qout. No se suman alturas como volumen físico ni se inventan áreas.

Se parametriza por q*=qin(50,h*) y se normalizan cabezas con H12=16.2 cm y H2=31.2 cm.
E: q12=q*Δh/H12, qout=q*sqrt(h2/H2). F: q12=q*(Δh/H12)^m,
qout=q*(h2/H2)^n, m,n∈[0.5,1]. G/H: v=λz+(1−λ)z², z=q/q*,
λ∈[0,1]; se invierte esa relación para q12 y/o qout. D fija m=n=0.5.
L reemplaza H12 por H12−offset y Δh por Δh−offset. M usa sqrt(h1/47.4) en q12.

Bomba potencial: q*=q(50), q(u)=q*(u/50)^γ. Zona muerta K sustituye u por
max(u−d,0)/(50−d). O: q(u)=q*[1−exp(−βu/50)]/[1−exp(−β)].
Curva cúbica I/J/P/R/U: z=u/100, F(z)=z+(b−1)z²+(1−2b+c)z³/3;
q(u)=q*F(z)/F(0.5). F'(z)=(1−z)²+2bz(1−z)+cz²>0 para b,c>0 y 0≤u≤100.
Es una curva empírica suave de sólo dos parámetros, sin tabla de cada escalón experimental.

Q/R: q12=max(0,q*+k12[(h1−h2)−16.2]); qout=max(0,q*+kout(h2−31.2)).
k12,kout en s^-1. T/U: mismos caudales y qin=max(0,q(u)−kpump(h1−47.4)),
kpump en s^-1. Son aproximaciones locales: el recorte no garantiza leyes correctas de
vaciado ni comportamiento real con bomba apagada fuera del régimen observado.

S: q12=max(0,q*+a(h1−47.4)−b(h2−31.2)); qout lineal local.
Su transferencia a≠b no depende únicamente del desnivel. S y T pueden realizar algebraicamente
C dentro del dominio sin recorte, mediante relaciones dadas en el protocolo; eso no
valida caudales reales ni áreas. T atribuye una diferencia de pendientes a la bomba,
mientras S la atribuye a la conexión: ambos pueden ser observacionalmente equivalentes.

Actuador opcional: dq_a/dt=[q_command(u,h1)−q_a]/τ, qin=q_a. Es un estado de actuador,
no un tanque. q_a inicial=q* supone régimen previo a 50%; en arranque esta historia no
está documentada. Retardo: aplicar u(t−δ) causal, usando 50% antes del inicio local.
RK4 particiona también los eventos desplazados y limita subpaso a τ/4 si τ>0.
