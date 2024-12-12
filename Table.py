# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS


# PARAMETERS
# FUNCTIONS
# CLASSES
class DBTable:
    name: str
    tb_fields: list[tuple[str, str, str]]
    tb_constraints: list[str]
    row_count: int = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self.tb_fields = []
        self.tb_constraints = []

    def _add_tb_field(self, field_name: str, field_type: str, field_constraints: str) -> None:
        self.tb_fields.append((field_name, field_type, field_constraints))

    def _add_tb_constraint(self, tb_constraint: str) -> None:
        self.tb_constraints.append(tb_constraint)

    def get_sql(self, template: str) -> str:
        match template:
            case "create_table":
                return self._create_table()
            case "row_count":
                return self._row_count()
            case "insert":
                return self._insert_into()
            case _:
                pass

    def _create_table(self) -> str:
        components = [", ".join(f"{n} {t} {c}".strip() for n, t, c in self.tb_fields)]
        if self.tb_constraints:
            components.append(", ".join(self.tb_constraints))
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join(components)})"

    def _row_count(self) -> str:
        return f"SELECT COUNT(*) FROM {self.name};"

    def _insert_into(self) -> str:
        return f"INSERT OR IGNORE INTO {self.name} "

    @staticmethod
    def format_insert_fields(fields: list[str]) -> str:
        return f"({', '.join(fields)})"

    @staticmethod
    def format_insert_values(values: list[tuple]) -> str:
        return ", ".join("(" + ", ".join(f"'{v}'" for v in value) + ")" for value in values)


class AngleTB(DBTable):
    def __init__(self) -> None:
        super().__init__("angle")
        self._add_tb_field("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
        self._add_tb_field("angle", "INTEGER", "NOT NULL UNIQUE")


class PhotonTB(DBTable):
    def __init__(self, name: str = "photon") -> None:
        super().__init__(name)
        self._add_tb_field("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
        self._add_tb_field("state_as_integer_as_text", "TEXT", "NOT NULL UNIQUE")


class BitwiseTB(PhotonTB):
    def __init__(self) -> None:
        super().__init__("bitwise")


class ResultsTB(DBTable):
    def __init__(self) -> None:
        super().__init__("results")
        self._add_tb_field("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
        self._add_tb_field("entanglement_state", "INTEGER", "NOT NULL")
        self._add_tb_field("photon1_entanglement_state", "INTEGER", "NOT NULL")
        self._add_tb_field("photon2_entanglement_state", "INTEGER", "NOT NULL")
        self._add_tb_field("photon1_measurement_angle", "INTEGER", "NOT NULL")
        self._add_tb_field("photon2_measurement_angle", "INTEGER", "NOT NULL")
        self._add_tb_field("photon1_measurement_state", "INTEGER", "NOT NULL")
        self._add_tb_field("photon2_measurement_state", "INTEGER", "NOT NULL")
        self._add_tb_field("measurement_angle_difference", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2es_oo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2es_zz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2es_oz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2es_zo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2ms_oo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2ms_zz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2ms_oz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2ms_zo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2es_oo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2es_zz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2es_oz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1ms_p2es_zo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2ms_oo", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2ms_zz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2ms_oz", "INTEGER", "NOT NULL")
        self._add_tb_field("p1es_p2ms_zo", "INTEGER", "NOT NULL")
        self._add_tb_constraint("UNIQUE(entanglement_state, photon1_measurement_angle, photon2_measurement_angle)")


# EOF
