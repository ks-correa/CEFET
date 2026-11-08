# Consolidación científica final

**Conclusión defendible:** E2, mando constante al 50%, es la mejor alternativa nominal
evaluada entre E0/E1/E2 bajo U, condiciones iniciales próximas al equilibrio y ausencia
de demanda externa documentada. La revisión es posterior a conocer el diagnóstico.
Los protocolos, comparaciones históricas y calibración permanecen intactos.

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | TV_u_pp |
|---|---|---|---|---|
| E0 | 9.1026 | 5.0073 | 48.748 | 1454.9 |
| E1 | 7.0168 | 3.7754 | 48.998 | 1163.9 |
| E2 | 0.19707 | 0.19702 | 50 | 0 |

RMSE en esta tabla: desviación de regulación, cm, corrida 8 ~800 s. Precisión predictiva
original de U, medias por corrida, separada:

| tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|
| h1 | 0.62896 | 0.87253 | 0.14581 | -0.28446 |
| h2 | 0.18748 | 0.24169 | 0.079027 | 0.12545 |

Se ejecutaron 19 comparaciones nominales y 90 sensibilidades exploratorias. E2 fue elegido
en todas, sin modificar la regla. El sesgo permanente desplazó el equilibrio, por lo que
no se acredita rechazo de perturbaciones. Se conservan excursiones de E0/E1 fuera del
rectángulo de estados observado y no se proclama cobertura experimental total.

Documentos vigentes: docs/consolidacion_final/. Esquema de 13 diapositivas con objetivos,
contenido, cifras, figuras, fuentes, explicación oral y límites: esquema_definitivo_13.md.
El informe_cumplimiento.md registra únicamente comprobaciones efectivamente ejecutadas.
No se creó PowerPoint. Nombres, fecha y ensayo de sustentación siguen pendientes.
