"""
a
"""


class Utilidades():
    """
    utilizades del proyecto
    """

    @staticmethod
    def formato_fecha(fecha):
        """
        Entrega la fecha en este formato 01-06-1992
        """
        dia = str(fecha.day)
        mes = str(fecha.month)
        f_dia = f'0{dia}' if len(dia) == 1 else dia
        f_mes = f'0{mes}' if len(mes) == 1 else mes
        return f'{f_dia}-{f_mes}-{fecha.year}'
