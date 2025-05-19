import pytest

from src.parser.parser_objects import CallExpr, AccessExpr, Identifier, IntExpr

from src.interpreter.interpreter_objects import StringValue


def test_int(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        CallExpr(
            AccessExpr(
                IntExpr(5, pos=(1, 1)), Identifier("toString", pos=(1, 3)), pos=(1, 5)
            ),
            args=[],
            pos=(1, 2),
        ),
        interpreter.global_env,
    ) == StringValue("5")


def test_all(make_parser, make_interpreter, mocked_error_handler):
    parser = make_parser("""alphabetical_sort = function(item1, item2) {
    if (item1.key() < item2.key()) {
        return -1;
    } elif (item1.key() > item2.key()) {
        return 1;
    } else {
        return 0;
    }
};

// Funkcja sprawdzaj ˛aca, czy populacja miasta przekracza 5 milionów
is_large = function(value) {
    return value > 5000000;
};

// Tworzenie słownika miast z populacj ˛a
cities = Dict(alphabetical_sort);
cities.addNew("Warszawa", 2000000);
cities.addNew("Tokio", 37000000);
cities.addNew("Delhi", 30000000);
cities.addNew("Szczecinek", 40000);
cities.addNew("Buenos Aires", 15000000);

// Wydruk wszystkich miast i ich populacji
print("Miasta i populacja:");
for city in cities {
    print("- ", city.key(), ":", city.value());
}

// Filtrowanie małych miast do nowej listy za pomoc ˛a zapytania LINQ
small_cities = from city in cities
select city.key(), city.value() / 1000
where city.value() < 5000000
order by city.key() descending;

// Wydruk przefiltrowanej listy
print("Małe miasta (< 5 mln):");
for entry in small_cities {
    print("- ", entry.get(0), " (", entry.get(1), " tys.)");
}

""", err=mocked_error_handler)
    interpreter = make_interpreter(err=mocked_error_handler)
    program = parser.parse_program()

    interpreter.eval(program)