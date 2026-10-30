import flet as ft
import flet_charts as fch
import seaborn as sns

def main(page: ft.Page):

    df = sns.load_dataset("tips")
    promedios_por_dia = df.groupby("day", observed=True)["total_bill"].mean()
    promedios = promedios_por_dia.tolist()
    # El índice del groupby mantiene promedios y días alineados (unique() no).
    dias = promedios_por_dia.index.tolist()

    chart = fch.BarChart(
        groups=[
            fch.BarChartGroup(
                x=i,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=promedio,
                        width=60,
                        color=ft.Colors.BLUE_600,
                        border_radius=4,
                        tooltip=f"{dia}: {promedio:.2f}",
                    )
                ],
            )
            for i, (dia, promedio) in enumerate(zip(dias, promedios))
        ],
        bottom_axis=fch.ChartAxis(
            labels=[
                fch.ChartAxisLabel(value=i, label=ft.Text(str(dia)))
                for i, dia in enumerate(dias)
            ],
        ),
        left_axis=fch.ChartAxis(label_size=40, title=ft.Text("Cuenta promedio")),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.GREY_300, width=1),
        min_y=0,
        expand=True,
    )

    page.add(
        ft.Text("Evolución de ventas"),
        ft.Container(
            content=chart,
            height=350
        )
    )

ft.run(main)
