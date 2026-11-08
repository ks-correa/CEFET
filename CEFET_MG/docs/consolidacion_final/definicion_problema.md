# Definición vigente del problema

**Pregunta:** ¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal?

El fenómeno real es la respuesta acoplada de dos niveles ante la entrada de una bomba.
Objetivo general: explicar y reproducir la dinámica medida con U y comparar tres condiciones
nominales mediante indicadores cuantitativos, para apoyar una recomendación local condicionada.
Objetivos específicos: mantener trazabilidad, explicar balances y RK4, conservar calibración
y evaluación interna, comparar E0/E1/E2 y explicitar límites del resultado y su sensibilidad.

«Estabilidad» se mide operacionalmente mediante RMSE/MAE frente a referencias, dispersión,
variación total y tiempo dentro de bandas analíticas ±2 cm. La estabilidad del equilibrio
matemático se estudia además con el Jacobiano local. No se extienden esas propiedades a
robustez global del montaje. «Minimizar» significa comparar las alternativas evaluadas.

E0 usa la excitación real de identificación, E1 la atenúa y E2 mantiene 50%. La misma
condición inicial registrada, tiempos y parámetros hacen comparable el contraste simulado.
E2 favorece el equilibrio que incorpora U, cerca del cual empiezan las corridas.
La aplicación y el informe calculan la decisión con la regla histórica sin modificarla.

La excitación pseudoaleatoria identifica la dinámica; no representa por sí misma una demanda
de producción que deba seguirse en operación. No hay una demanda, consigna móvil ni
disponibilidad variable documentada que haga obligatorio variar la bomba. Si se incorporase
alguna, habría que revisar la pregunta y aportar datos e indicadores apropiados.

Uso de datos externos autorizado por el docente según la comunicación del usuario. La pareja
reutiliza las mediciones de investigadores de CEFET-MG; no construyó ni midió el montaje.
Frontera: dos niveles y un mando; sin áreas absolutas, consumos eléctricos ni cargas externas
identificadas. No se recomienda sobre desbordamiento, vaciado o arranque en frío.
