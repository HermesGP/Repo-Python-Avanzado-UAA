import asyncio
from concurrent.futures import ThreadPoolExecutor

import flet as ft

from services import graficos
from services.dashboard_service import DashboardService


class DashboardView(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        self.service = DashboardService()
        self.pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="dashboard")
        self._generacion = 0

        # clave -> (título, tarea que consulta con SQLAlchemy y dibuja con seaborn)
        self.tareas = {
            "top": ("Top 5 productos por ganancia", self._top_productos),
            "clientes": ("Clientes acumulados por mes", self._clientes),
            "histograma": ("Ventas por volumen", self._histograma),
            "mensual": ("Ganancias mes a mes", self._mensual),
        }
        # Un contenedor vacío por gráfico, con la misma clave que en self.tareas.
        # Esa clave es el vínculo entre tarea y tarjeta: el resultado de cada
        # tarea se coloca después en el .content de su contenedor.
        self.cuerpos = {
            clave: ft.Container(height=380, alignment=ft.Alignment.CENTER)
            for clave in self.tareas
        }

        self.btn_actualizar = ft.OutlinedButton(
            "Actualizar", icon=ft.Icons.REFRESH, on_click=self.actualizar
        )
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text("Dashboard de ventas", size=24, weight=ft.FontWeight.BOLD),
                    self.btn_actualizar,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            # Se crea una tarjeta por cada entrada de self.tareas (mismo orden).
            # Cada tarjeta lleva el título de su tarea y el contenedor
            # self.cuerpos[clave], que al principio está vacío y luego recibe
            # el ProgressRing y, al terminar la tarea, la imagen del gráfico.
            ft.ResponsiveRow(
                [
                    ft.Card(
                        col={"xs": 12, "lg": 6},
                        content=ft.Container(
                            padding=12,
                            content=ft.Column(
                                controls=[
                                    ft.Text(titulo, size=16, weight=ft.FontWeight.W_600),
                                    self.cuerpos[clave],
                                ],
                            ),
                        ),
                    )
                    for clave, (titulo, _) in self.tareas.items()
                ],
            ),
        ]

    def _top_productos(self):
        return graficos.grafico_top_productos(self.service.top_productos_ganancia(5))

    def _clientes(self):
        return graficos.grafico_clientes_acumulados(
            self.service.clientes_acumulados_por_mes()
        )

    def _histograma(self):
        return graficos.grafico_histograma_ventas(self.service.ventas_por_volumen())

    def _mensual(self):
        return graficos.grafico_ganancias_mensuales(self.service.ganancias_por_mes())

    async def actualizar(self, e=None):
        # Cada llamada recibe un número de "generación". Si el usuario vuelve a abrir
        # la pestaña o pulsa Actualizar antes de que termine la corrida anterior,
        # esa corrida detecta que ya no es la vigente y descarta sus resultados.
        self._generacion += 1
        generacion = self._generacion

        # Estado inicial: cada tarjeta muestra un indicador de carga y el botón
        # se deshabilita para evitar actualizaciones superpuestas.
        for cuerpo in self.cuerpos.values():
            cuerpo.content = ft.ProgressRing()
        self.btn_actualizar.disabled = True
        self.update()

        # Los 4 gráficos se lanzan a la vez como corrutinas; cada una delega el
        # trabajo pesado (consulta SQL + pandas + seaborn) a un hilo del pool.
        # Así la interfaz no se bloquea y las consultas corren en paralelo.
        loop = asyncio.get_running_loop()
        pendientes = [
            asyncio.ensure_future(self._generar(loop, clave, tarea))
            for clave, (_, tarea) in self.tareas.items()
        ]
        # as_completed entrega cada resultado apenas está listo, sin esperar al
        # resto: los gráficos aparecen de a uno, en el orden en que terminan.
        # La interfaz solo se modifica aquí, dentro del event loop (nunca desde
        # los hilos del pool), que es lo que hace segura la actualización.
        for terminado in asyncio.as_completed(pendientes):
            # La clave devuelta por _generar identifica a qué tarjeta pertenece el
            # gráfico, sin importar en qué orden terminen las tareas.
            clave, contenido = await terminado
            if generacion != self._generacion:
                return  # una actualización más reciente tomó el control
            self.cuerpos[clave].content = contenido
            self.cuerpos[clave].update()

        # Fin de la corrida: se rehabilita el botón solo si sigue siendo la vigente.
        if generacion == self._generacion:
            self.btn_actualizar.disabled = False
            self.btn_actualizar.update()

    async def _generar(self, loop, clave, tarea):
        # Devuelve siempre (clave, control): si el gráfico falla se devuelve un
        # mensaje de error, para que un fallo no deje su tarjeta cargando ni
        # impida mostrar los otros gráficos.
        try:
            png = await loop.run_in_executor(self.pool, tarea)
            return clave, ft.Image(src=png, fit=ft.BoxFit.CONTAIN)
        except Exception as error:
            return clave, ft.Text(
                f"No se pudo generar el gráfico: {error}", color=ft.Colors.RED_600
            )

