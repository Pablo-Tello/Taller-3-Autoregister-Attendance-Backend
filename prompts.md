1. Quiero que en los nombres de las columnas de los models usen prefijos:
string: str_
integer: int_
boolean: bool_
datetime: dt_
2. La tabla ciclo_academico esta relacionada con las tablas alumno_seccion, docente_seccion y sesion_clase, porque cada año puede haber dos o tres ciclos. Por ejemplo: ciclo 2024-1 inicia cierto lunes de marzo del 2024 y finaliza 20 semanas despues. ciclo 2024-2 inicia cierto lunes de agosto del 2024 y termina 20 semanas despues, y puede haber un ciclo verano 2024-3 que inicia cierto lunes de enero del 2025 y termina 9 semanas.
3. En la tabla calendario, quiero agregar todas las fechas del año, agregando una columna que describa si es un dia feriado o un dia laboral. Estas fecha se van a usar en la tabla sesión de clase.
4. En la tabla sesion de clase, es la tabla donde se va a programar todas las sesiones de clase del ciclo academico presente. Donde una columna debe decir si ya se realizó dicha sesion de clase o esta pendiente.
5. Quiero crear un tabla horario, que va a tener una clave foranea de la tabla docente_seccion. Y la tabla sesion_clase va a usar los horarios semanales para programar todas las sesiones de clase del presente ciclo academico.



Django SuperUser:
email: admin@example.com
password: test1 