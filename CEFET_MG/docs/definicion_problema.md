# Definición del problema

El fenómeno observado es la respuesta acoplada de niveles a una bomba variable en un
montaje físico de CEFET-MG. Los estudiantes reutilizan registros publicados; no realizaron
mediciones, fotografías ni construcción. La aceptación docente de esta modalidad está pendiente.

Pregunta: ¿con qué precisión se pueden predecir libremente ambos niveles durante la excitación
y recuperación registradas y, sólo si esa precisión es suficiente, qué modificación de la bomba
reduciría sus desviaciones respecto a 47.4 y 31.2 cm dentro del régimen estudiado?

El objetivo general es identificar y evaluar un modelo continuo reproducible para apoyar una
decisión local de operación. Los objetivos específicos son auditar registros y unidades,
formular balances condicionales a la topología, comparar estructuras parsimoniosas,
calibrar conjuntamente h1 y h2, comprobar integración, cuantificar errores y establecer alcance.

Límite: dos niveles y una entrada de bomba; sin tuberías, presión, temperatura ni dinámica
eléctrica medidas. Observables: t (s), h1,h2 (cm), u (%). No hay caudalímetros ni geometría
documentados. La capacidad nominal de 200 L no permite calcular el área transversal.
No estudiar desbordamiento, vaciado o llenado desde cero como decisiones operativas.

El experimento usa una entrada forzada, no un escalón aislado ni un controlador nuevo.
MAE/RMSE/NRMSE contra mediciones evalúan reproducción; no son lo mismo que error contra
referencia de regulación. Sobreimpulso y establecimiento sólo tienen interpretación por cambio
de referencia o tramo constante suficientemente largo. La señal repetida no prueba adaptación
a otras entradas. Esfuerzo se puede expresar como desviación porcentual y variación total de u,
no como energía eléctrica ni caudal real.

Decisión inmediata: aceptar o rechazar el modelo para continuar a escenarios. Si se supera
el umbral en ambos tanques, diseñar después E0 señal observada, E1 atenuación de desviación
de u y E2 realimentación simulada saturada al rango registrado. Fijar antes de ejecutarlos:
RMSE respecto a referencia, MAE de desviación, máximo, variación total de niveles y bomba,
integral de (u-50)^2 dt. Mismas condiciones iniciales, duración y RK4. No se afirma que una
política contrafactual funcione en el montaje sin probarla experimentalmente.

## Actualización de fase 3

El docente aceptó usar las mediciones externas, según comunicación del usuario. La pregunta se concreta en comparar E0, E1 y E2 para reducir desviaciones locales respecto a 47.4/31.2 cm. La regla, indicadores y bandas analíticas se fijaron antes de ejecutar; ver protocolo_escenarios.md. El resultado calculado y sus compensaciones están en reports/simulador/resultados_y_decision.md. Las mediciones siguen siendo de los investigadores de CEFET-MG.
