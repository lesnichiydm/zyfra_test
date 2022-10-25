from attr import dataclass

from extraction_point.models import ExtractionPoint


@dataclass
class MineralInfo:
    si_o_2_tons: float
    fe_tons: float
    total_tons: float

    @property
    def other_mineral_tons(self) -> float:
        return self.total_tons - self.si_o_2_tons - self.fe_tons

    def __add__(self, other):
        self.si_o_2_tons += other.si_o_2_tons
        self.fe_tons += other.fe_tons
        self.total_tons += other.total_tons
        return self

    @property
    def si_o_2_percent(self):
        return int(self.si_o_2_tons * 100 / self.total_tons)

    @property
    def fe_percent(self):
        return int(self.fe_tons * 100 / self.total_tons)

    @property
    def description(self):
        return f"{self.si_o_2_percent}% SiO2 {self.fe_percent}% Fe"


def add_extraction_point(name, percent_si_o_2, percent_fe):
    """Добавление точки загрузки руды"""
    return ExtractionPoint.objects.create(
        name=name,
        percent_si_o_2=percent_si_o_2,
        percent_fe=percent_fe,
    )


def calc_mineral_info(extraction_point, weight):
    """Рассчет датакласса информера для точки добычи"""
    si_o_2_tons = weight / 100 * extraction_point.percent_si_o_2
    fe_tons = weight / 100 * extraction_point.percent_fe
    return MineralInfo(
        si_o_2_tons=si_o_2_tons,
        fe_tons=fe_tons,
        total_tons=weight,
    )
