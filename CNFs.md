Daniel Robayo 18-11086
Valeria Vera 16-11233

# Problema traducido a CNF

* Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales". Esto significa que, si hay 10 equipos, cada equipo jugará 18 veces.

_(¬Participante(x) ∨ ¬Participante(y) v (x = y) ∨ Juego(x, y, d, h)) ∧ (¬Participante(x) ∨ ¬Participante(y) ∨ (x = y) ∨ Juego(y, x, d, h))_


* Dos juegos no pueden ocurrir al mismo tiempo.

_¬Juego(x, y, d1, h1) ∨ ¬Juego(x, y, d2, h2) ∨ ¬MismoDia(d1, d2) ∨  ¬MismaHora(h1, h2)_

* Un participante puede jugar a lo sumo una vez por día.

_Dia(x, d1) ∨ ¬Dia(x, d2) v (d1 = d2) ∨ ¬MismoDia(d1, d2)_

* Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.

_¬Local(x, y, d1, h) ∨ ¬Local(x, y, d2, h) ∨  ¬MismoDia(d1, d2)_
_¬Visitante(x, y, d1, h) ∨ ¬Visitante(x, y, d2, h) ∨  ¬MismoDia(d1, d2)_

* Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
* Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
* Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
* A efectos prácticos, todos los juegos tienen una duración de dos horas.
