# STANDARD IMPORTS
from __future__ import annotations
from typing import Optional, Any
from sqlite3 import Connection, Cursor
import sqlite3
# CUSTOM IMPORTS
from Table import AngleTB, PhotonTB, BitwiseTB, ResultsTB


# PARAMETERS
# FUNCTIONS
# CLASSES
class Database:
    name: str
    connection: Connection

    def __init__(self, name: str) -> None:
        self.name = name
        self.connection = sqlite3.connect(self.name)

    def _get_cursor(self) -> Cursor:
        return self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def execute(self, sql: str) -> Cursor:
        return self.connection.execute(sql)

    def fetch(self, sql: str) -> Cursor:
        return self._get_cursor().execute(sql)

    def fetch_one(self, sql: str) -> Optional[tuple[Any, ...]]:
        return self._get_cursor().execute(sql).fetchone()

    def fetch_many(self, sql: str, size: int) -> list[tuple[Any, ...]]:
        return self._get_cursor().execute(sql).fetchmany(size)


class StateDB(Database):
    angle: AngleTB
    photon: PhotonTB
    bitwise: BitwiseTB

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._init_angle_tb()
        self._init_photon_tb()
        self._init_bitwise_tb()
        self._update_table_row_counts()

    def _init_angle_tb(self) -> None:
        self.angle = AngleTB()
        self.execute(self.angle.get_sql("create_table"))
        self.commit()

    def _init_photon_tb(self) -> None:
        self.photon = PhotonTB()
        self.execute(self.photon.get_sql("create_table"))
        self.commit()

    def _init_bitwise_tb(self) -> None:
        self.bitwise = BitwiseTB()
        self.execute(self.bitwise.get_sql("create_table"))
        self.commit()

    def _update_table_row_counts(self):
        self.angle.row_count = self.fetch_one(self.angle.get_sql("row_count"))[0]
        self.photon.row_count = self.fetch_one(self.photon.get_sql("row_count"))[0]
        self.bitwise.row_count = self.fetch_one(self.bitwise.get_sql("row_count"))[0]

    def populate(self, table: str):
        match table:
            case "angle":
                self._populate_angle()
            case "photon":
                self._populate_photon()
            case "bitwise":
                self._populate_bitwise()
            case _:
                pass

    def _populate_angle(self):
        formatted_fields = self.angle.format_insert_fields(["angle"])
        formatted_values = self.angle.format_insert_values([*((value,) for value in range(360))])
        sql = f"{self.angle.get_sql("insert")} {formatted_fields} VALUES {formatted_values};"
        self.execute(sql)
        self.commit()

    def _populate_photon(self):
        bitstring = ("1" * 90 + "0" * 90) * 2
        values = []
        formatted_fields = self.photon.format_insert_fields(["state_as_integer_as_text"])
        for n in range(180):
            state_as_bs = bitstring[n:] + bitstring[:n]
            state_as_int = int(state_as_bs, 2)
            values.append((state_as_int, state_as_bs))
        formatted_values = self.photon.format_insert_values(values)
        sql = f"{self.photon.get_sql("insert")} {formatted_fields} VALUES {formatted_values};"
        self.execute(sql)
        self.commit()

    def _populate_bitwise(self):
        mask = (1 << 360) - 1
        values = set()

        def circular_shift_left(shift):
            for p1 in range(180):
                o_p1 = circular_shift_left(p1)
                for p2 in range(180):
                    o_p2 = circular_shift_left(p2)
                    z_p1 = ~o_p1 & mask
                    z_p2 = ~o_p2 & mask
                    for result in (o_p1 & o_p2, z_p1 & z_p2, o_p1 & z_p2, z_p1 & o_p2):
                        values.add((result, f"{result:0360b}"))
            return ((2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 << shift) | (2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 >> (360 - shift))) & ((1 << 360) - 1)

        formatted_fields = self.bitwise.format_insert_fields(["state_as_integer_as_text"])
        formatted_values = self.bitwise.format_insert_values(list(values))
        sql = f"{self.bitwise.get_sql("insert")} {formatted_fields} VALUES {formatted_values};"
        self.execute(sql)
        self.commit()


class TrialDB(Database):
    results: ResultsTB

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._init_results_tb()

    def _init_results_tb(self) -> None:
        self.results = ResultsTB()
        self.execute(self.results.get_sql("create_table"))
        self.commit()

# EOF
